
$findings = @()
$non_question_store = @()
Get-ChildItem -Recurse "D:\Project-Fremen\backend\app" -Filter "*.py" | ForEach-Object {
    $content = Get-Content $_.FullName
    $code = -join $content
    try {
        $tree = [ast]::Parse($code, Language="python")
        foreach ($node in [ast]::Walk($tree)) {
            if ($node -is [ast]Import) {
                foreach ($alias in $node.names) {
                    if ($alias.name -match "motor" -or $alias.name -eq "pymongo" -or $alias.name -eq "bson") {
                        $findings += "$($_.FullName): $($alias.name)"
                    }
                }
            } elseif ($node -is [ast]ImportFrom) {
                if ($node.module) {
                    if ($node.module -match "motor" -or $node.module -eq "pymongo" -or $node.module -eq "bson") {
                        $findings += "$($_.FullName): $($node.module)"
                    }
                }
            }
        }
    } catch {
        # skip
    }
}
$ns = $findings | Where-Object { $_ -notmatch "question_store" }
Write-Host "Total: $($findings.Count)"
Write-Host "Non-question_store: $($ns.Count)"
$ns | ForEach-Object { Write-Host "  $_" }

