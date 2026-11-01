# install-user.ps1 - copy the kit's skills into your user skill folders on Windows,
# for a desktop where symlinked skills in a checkout show up as text files.
#
#   powershell -ExecutionPolicy Bypass -File .gtd\kit\install\install-user.ps1
#
# Copies (does not link) into %USERPROFILE%\.claude\skills and %USERPROFILE%\.codex\skills.
# Run it again after moving the submodule pin.
$ErrorActionPreference = "Stop"
$src = Join-Path $PSScriptRoot "..\skills"
foreach ($tool in @(".claude", ".codex")) {
  $dest = Join-Path $env:USERPROFILE "$tool\skills"
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Get-ChildItem -Directory $src | ForEach-Object {
    $to = Join-Path $dest $_.Name
    if (Test-Path $to) { Remove-Item -Recurse -Force $to }
    Copy-Item -Recurse $_.FullName $to
    Write-Host "copied $($_.Name) -> $to"
  }
}
