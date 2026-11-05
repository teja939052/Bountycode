import importlib.util
spec = importlib.util.spec_from_file_location("python", "D:/Project-Fremen/backend/app/services/lessons/python.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
print("Total Python lessons:", len(mod.PYTHON_LESSONS))
for l in mod.PYTHON_LESSONS:
    print("  " + l["id"] + ": " + l["title"] + " (" + l["difficulty"] + ") - " + str(len(l["steps"])) + " steps")