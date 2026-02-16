Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$electronDir = Resolve-Path (Join-Path $scriptDir "..")
$repoDir = Resolve-Path (Join-Path $electronDir "..\..")
$backendDir = Resolve-Path (Join-Path $repoDir "app")
$backendOutputDir = Join-Path $electronDir "resources\backend"
$builderEnvPath = Join-Path $repoDir "builder-local.env"

function Get-EnvMapFromFile {
  param([string]$Path)

  $map = @{}
  if (-not (Test-Path $Path)) {
    return $map
  }

  Get-Content $Path | ForEach-Object {
    $line = $_.Trim()
    if ([string]::IsNullOrWhiteSpace($line) -or $line.StartsWith('#')) {
      return
    }

    if ($line -match '^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$') {
      $key = $matches[1]
      $value = $matches[2].Trim().Trim('"').Trim("'")
      $map[$key] = $value
    }
  }

  return $map
}

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

Write-Host "[build-backend] Writing production .env from builder-local.env..."
$envMap = Get-EnvMapFromFile -Path $builderEnvPath
if ($envMap.Count -eq 0) {
  Write-Warning "[build-backend] builder-local.env not found or empty. Using safe defaults."
}

$defaults = @{
  DB_ENGINE = "sqlite"
  DB_SQLITE_PATH = ""
  TEST = "OFF"
  ADMIN_PASSWORD = "123"
  ENV = "production"
  SYNC_REMOTE_ENABLED = "OFF"
  SYNC_REMOTE_BASE_URL = ""
  SYNC_REMOTE_API_KEY = ""
}

$final = @{}
$defaults.Keys | ForEach-Object {
  $final[$_] = if ($envMap.ContainsKey($_)) { $envMap[$_] } else { $defaults[$_] }
}

$prodEnv = @(
  ('DB_ENGINE="' + $final.DB_ENGINE + '"'),
  ('DB_SQLITE_PATH="' + $final.DB_SQLITE_PATH + '"'),
  ('TEST="' + $final.TEST + '"'),
  ('ADMIN_PASSWORD="' + $final.ADMIN_PASSWORD + '"'),
  ('ENV="' + $final.ENV + '"'),
  ('SYNC_REMOTE_ENABLED="' + $final.SYNC_REMOTE_ENABLED + '"'),
  ('SYNC_REMOTE_BASE_URL="' + $final.SYNC_REMOTE_BASE_URL + '"'),
  ('SYNC_REMOTE_API_KEY="' + $final.SYNC_REMOTE_API_KEY + '"')
)

Set-Content -Path (Join-Path $backendOutputDir ".env") -Value $prodEnv -Encoding ASCII

Write-Host "[build-backend] Done."
