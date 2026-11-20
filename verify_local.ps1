param([switch]$InstallDependencies, [string]$PythonPath = '')
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:PYTHONUTF8 = '1'
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
if ($PythonPath) {
    $python = (Resolve-Path -LiteralPath $PythonPath).Path
} else {
    $python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
}
if (-not (Test-Path -LiteralPath $python)) {
    python -m venv (Join-Path $PSScriptRoot '.venv')
    if ($LASTEXITCODE -ne 0) { throw 'venv creation failed' }
    $InstallDependencies = $true
}
if ($InstallDependencies) {
    & $python -m pip install -r (Join-Path $PSScriptRoot 'requirements-local.txt')
    if ($LASTEXITCODE -ne 0) { throw 'dependency installation failed' }
    & $python -m pip install -e $PSScriptRoot
    if ($LASTEXITCODE -ne 0) { throw 'project installation failed' }

}
& $python local_demo.py
if ($LASTEXITCODE -ne 0) { throw 'demo failed' }
# A unique new temp path avoids touching pre-existing test directories.
$scratch = Join-Path $PSScriptRoot 'verification\.scratch'
New-Item -ItemType Directory -Force -Path $scratch | Out-Null
$tempRoot = Join-Path $scratch ('ai-verify-' + [guid]::NewGuid().ToString('N'))
& $python -m pytest test -q --basetemp=$tempRoot
if ($LASTEXITCODE -ne 0) { throw 'tests failed' }
