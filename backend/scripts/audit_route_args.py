"""Audit route handlers for argument-count mismatches vs service signatures."""
import ast
import os

ROUTES_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "routes")
SERVICES_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "services")

def collect_service_modules():
    modules = {}
    for fn in os.listdir(SERVICES_DIR):
        if fn.endswith(".py") and not fn.startswith("_") and fn != "__init__.py":
            mod = fn[:-3]
            modules[mod] = os.path.join(SERVICES_DIR, fn)
    return modules

def parse_signatures(path):
    sigs = {}
    try:
        tree = ast.parse(open(path, encoding="utf-8").read())
    except Exception as e:
        return sigs, f"PARSE_ERR: {e}"
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            args = [a.arg for a in node.args.args if a.arg not in ("self", "cls")]
            ndef = len(node.args.defaults)
            optional_start = len(args) - ndef if ndef else len(args)
            sigs[node.name] = {
                "args": args,
                "required": optional_start,
                "max": len(args),
            }
    return sigs, None

def analyze_route(route_path):
    """Return (imports, calls, parse_err)."""
    try:
        src = open(route_path, encoding="utf-8").read()
        tree = ast.parse(src)
    except Exception as e:
        return None, None, f"PARSE_ERR: {e}"
    imports = {}  # local_name -> module_key (last component)
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if mod.startswith("app.services"):
                for alias in node.names:
                    local = alias.asname or alias.name
                    imports[local] = (mod, alias.name)
    calls = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                name = node.func.id
                if name in imports:
                    calls.append((node.lineno, name, len(node.args), node))
            elif isinstance(node.func, ast.Attribute):
                base = node.func.value
                if isinstance(base, ast.Name) and base.id in imports:
                    mod, orig = imports[base.id]
                    modkey = mod.split(".")[-1]
                    calls.append((node.lineno, f"{base.id}.{node.func.attr}", len(node.args), node, modkey))
    return imports, calls, None

def main():
    service_mods = collect_service_modules()
    sig_index = {}
    for mod, path in service_mods.items():
        sigs, err = parse_signatures(path)
        for fn, info in sigs.items():
            sig_index[(mod, fn)] = info
            sig_index[(None, fn)] = info  # bare-name fallback

    route_files = sorted(
        os.path.join(ROUTES_DIR, f) for f in os.listdir(ROUTES_DIR)
        if f.endswith(".py") and not f.startswith("_") and f != "__init__.py"
    )

    mismatches = []
    unresolved = []
    for rf in route_files:
        rname = os.path.basename(rf)
        imports, calls, err = analyze_route(rf)
        if err:
            mismatches.append((rname, 0, "ROUTE_PARSE_ERR", err))
            continue
        for c in calls:
            if len(c) == 5:
                lineno, callname, nargs, node, modkey = c
            else:
                lineno, callname, nargs, node = c
                modkey = None
            sig = sig_index.get((modkey, callname.split(".")[-1])) if modkey else sig_index.get((None, callname))
            if sig is None:
                unresolved.append((rname, lineno, callname, nargs, modkey))
                continue
            required = sig["required"]
            maxn = sig["max"]
            if nargs < required:
                mismatches.append((rname, lineno, callname, f"TOO FEW: got {nargs}, need >= {required}. sig args={sig['args']}"))
            elif nargs > maxn:
                mismatches.append((rname, lineno, callname, f"TOO MANY: got {nargs}, max {maxn}. sig args={sig['args']}"))

    print("=== ARG MISMATCHES ===")
    for m in mismatches:
        print(f"{m[0]}:{m[1]}: {m[2]} -> {m[3]}")
    print(f"\nTotal mismatches: {len(mismatches)}")
    print(f"\n=== UNRESOLVED CALLS (no signature found) ===")
    for u in unresolved:
        print(f"{u[0]}:{u[1]}: {u[2]} (nargs={u[3]}, modkey={u[4]})")
    print(f"Total unresolved: {len(unresolved)}")

if __name__ == "__main__":
    main()