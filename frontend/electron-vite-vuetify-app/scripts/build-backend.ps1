Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$electronDir = Resolve-Path (Join-Path $scriptDir "..")
$repoDir = Resolve-Path (Join-Path $electronDir "..\..")
$backendDir = Resolve-Path (Join-Path $repoDir "app")
$backendOutputDir = Join-Path $electronDir "resources\backend"

Write-Host "[build-backend] Cleaning backend output folder..."
if (Test-Path $backendOutputDir) {
  attrib -R (Join-Path $backendOutputDir "*") /S /D 2>$null
  try {
    Remove-Item -Path $backendOutputDir -Recurse -Force -ErrorAction Stop
  } catch {
    cmd /c "rmdir /s /q `"$backendOutputDir`""
  }
}
New-Item -Path $backendOutputDir -ItemType Directory | Out-Null

Write-Host "[build-backend] Building FastAPI executable with PyInstaller..."
Push-Location $backendDir
try {
  pyinstaller --noconfirm --clean --onedir --name villa-api `
    --paths . `
    --collect-submodules database `
    --collect-submodules routers `
    main.py
} finally {
  Pop-Location
}

$builtBackendDir = Join-Path $backendDir "dist\villa-api"
if (-not (Test-Path $builtBackendDir)) {
  throw "Backend build output not found at '$builtBackendDir'."
}

Write-Host "[build-backend] Copying backend files to Electron resources..."
Copy-Item -Path (Join-Path $builtBackendDir "*") -Destination $backendOutputDir -Recurse -Force

Write-Host "[build-backend] Writing production .env (SQLite desktop mode)..."
$adminPassword = "123"
$rootEnvPath = Join-Path $repoDir ".env"
if (Test-Path $rootEnvPath) {
  $adminLine = Select-String -Path $rootEnvPath -Pattern "^\s*ADMIN_PASSWORD\s*=" | Select-Object -First 1
  if ($adminLine) {
    $adminPassword = ($adminLine.Line -replace "^\s*ADMIN_PASSWORD\s*=\s*", "").Trim().Trim('"').Trim("'")
  }
}

$prodEnv = @(
  'DB_ENGINE="sqlite"',
  'DB_SQLITE_PATH=""',
  'TEST="OFF"',
  ('ADMIN_PASSWORD="' + $adminPassword + '"'),
  'ENV="production"',
  'SYNC_REMOTE_ENABLED="OFF"',
  'SYNC_REMOTE_BASE_URL=""',
  'SYNC_REMOTE_API_KEY=""'
)

Set-Content -Path (Join-Path $backendOutputDir ".env") -Value $prodEnv -Encoding ASCII

Write-Host "[build-backend] Done."
