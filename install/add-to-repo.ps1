# add-to-repo.ps1 - pull gtd-board-kit into the current work repo as a pinned submodule.
#
#   powershell -ExecutionPolicy Bypass -File add-to-repo.ps1 [-Pin <full-40-hex-commit>]
#
# Same steps as add-to-repo.sh, for Windows PowerShell 5.1 or PowerShell 7. Run from the
# work repo's root, on a branch. Commits nothing: review `git status`, commit, open a PR.
param([string]$Pin = "")
$ErrorActionPreference = "Stop"

$KitUrl = "https://github.com/dandelion-love/gtd-board-kit"
$KitDir = ".gtd/kit"
$Skills = @("board-onboard", "board-pickup", "board-claim", "board-report", "board-needs-person", "okf-knowledge")

# Not named "Git": PowerShell names are case-insensitive and functions beat executables,
# so a function called Git would call itself instead of git.exe.
function Invoke-Git { & git @args; if ($LASTEXITCODE -ne 0) { throw "git $args failed" } }

if (-not (Test-Path .git)) { throw "Run this from the work repo's root." }
$branch = (& git rev-parse --abbrev-ref HEAD).Trim()
$default = ""
try { $default = ((& git symbolic-ref --quiet --short refs/remotes/origin/HEAD 2>$null) -replace '^origin/', '') } catch { }
if ($branch -in @("main", "master", $default)) { throw "On $branch - switch to a branch first." }

if (-not (Test-Path "$KitDir/.git")) { Invoke-Git submodule add $KitUrl $KitDir }
Invoke-Git -C $KitDir fetch --quiet origin
if (-not $Pin) { $Pin = (& git -C $KitDir rev-parse origin/main).Trim() }
if ($Pin -notmatch '^[0-9a-f]{40}$') { throw "Pin must be a full 40-hex commit." }
Invoke-Git -C $KitDir checkout --quiet --detach $Pin
Invoke-Git add .gitmodules $KitDir

# Symlinks written straight into the index (mode 120000), so no Developer Mode is needed.
# Without core.symlinks the working copy shows small text files; the commit is still right.
$tmp = [System.IO.Path]::GetTempFileName()
foreach ($tool in @(".claude", ".codex")) {
  foreach ($s in $Skills) {
    $path = "$tool/skills/$s"
    if ((Test-Path $path) -and -not ((Get-Item $path -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) -and (Test-Path $path -PathType Container)) {
      Write-Host "keep    $path (the repo's own skill overrides the kit's)"; continue
    }
    $target = "../../$KitDir/skills/$s"
    [System.IO.File]::WriteAllText($tmp, $target)          # no newline, no BOM
    $blob = (& git hash-object -w $tmp).Trim()
    & git rm -r --cached --quiet --ignore-unmatch $path | Out-Null
    if (Test-Path $path) { Remove-Item -Recurse -Force $path }
    Invoke-Git update-index --add --cacheinfo "120000,$blob,$path"
    Invoke-Git checkout -- $path
  }
}
Remove-Item $tmp

if (-not (Test-Path .claude/settings.json)) {
  Copy-Item "$KitDir/install/settings.snippet.json" .claude/settings.json
  Invoke-Git add .claude/settings.json
} else {
  Write-Host "NOTE: .claude/settings.json exists; merge $KitDir/install/settings.snippet.json into it by hand."
}

if (-not (Test-Path .gtd/BOARD.local.md)) {
  Copy-Item "$KitDir/install/BOARD.local.template.md" .gtd/BOARD.local.md
  Invoke-Git add .gtd/BOARD.local.md
  Write-Host "NOTE: fill in .gtd/BOARD.local.md with this repo's labels, fields and rules."
}

function Add-Line([string]$File, [string]$Line) {
  if ((Test-Path $File) -and (Select-String -Path $File -SimpleMatch ".gtd/kit/BOARD.md" -Quiet)) { return }
  $prefix = ""
  if ((Test-Path $File) -and ((Get-Item $File).Length -gt 0)) { $prefix = "`n" }
  [System.IO.File]::AppendAllText((Join-Path (Get-Location) $File), "$prefix$Line`n")
  Invoke-Git add $File
}
Add-Line "CLAUDE.md" "Board work (gtd-board-kit): @.gtd/kit/BOARD.md then @.gtd/BOARD.local.md"
Add-Line "AGENTS.md" "Board work (gtd-board-kit): read .gtd/kit/BOARD.md, then .gtd/BOARD.local.md, before touching the board."

Write-Host "gtd-board-kit pinned at $Pin. Review, commit and open a PR:"
& git status --short
