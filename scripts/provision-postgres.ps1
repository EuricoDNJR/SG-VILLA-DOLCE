param(
  [switch]$UseDocker,
  [string]$AdminUser = "postgres",
  [string]$AdminPassword = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-EnvValue {
  param(
    [string]$EnvPath,
    [string]$Key
  )

  $line = Select-String -Path $EnvPath -Pattern "^\s*$Key\s*=" | Select-Object -First 1
  if (-not $line) {
    return $null
  }

  $value = $line.Line -replace "^\s*$Key\s*=\s*", ""
  $value = $value.Trim().Trim('"').Trim("'")
  return $value
}

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoDir = Resolve-Path (Join-Path $scriptDir "..")
$envPath = Join-Path $repoDir ".env"

if (-not (Test-Path $envPath)) {
  throw ".env not found at '$envPath'."
}

$dbName = Get-EnvValue -EnvPath $envPath -Key "DB_NAME"
$dbUser = Get-EnvValue -EnvPath $envPath -Key "DB_USER"
$dbPassword = Get-EnvValue -EnvPath $envPath -Key "DB_PASSWORD"
$dbHost = Get-EnvValue -EnvPath $envPath -Key "DB_HOST"
$dbPort = Get-EnvValue -EnvPath $envPath -Key "DB_PORT"

if (-not $dbName -or -not $dbUser -or -not $dbPassword) {
  throw "DB_NAME, DB_USER and DB_PASSWORD must be set in .env."
}

if (-not $PSBoundParameters.ContainsKey('UseDocker')) {
  $UseDocker = $true
}

if ($UseDocker) {
  Write-Host "[postgres] Starting Docker database service..."
  Push-Location $repoDir
  try {
    docker compose up -d db
  } finally {
    Pop-Location
  }

  Write-Host "[postgres] Waiting for container to be ready..."
  $maxAttempts = 30
  for ($i = 1; $i -le $maxAttempts; $i++) {
    $isReady = $false
    try {
      $readyCommand = "pg_isready -U `"$dbUser`" -d `"$dbName`""
      docker exec db sh -lc $readyCommand *> $null
      if ($LASTEXITCODE -eq 0) {
        $isReady = $true
      }
    } catch {
      $isReady = $false
    }

    if ($isReady) {
      Write-Host "[postgres] Ready on localhost:5432 (container: db)."
      exit 0
    }

    Start-Sleep -Seconds 2
  }

  Write-Warning "[postgres] Container started but readiness check did not confirm within timeout."
  Write-Warning "[postgres] Check status with: docker ps --filter `"name=db`" and logs with: docker logs db"
  exit 0
}

if ([string]::IsNullOrWhiteSpace($AdminPassword)) {
  throw "For local provisioning without Docker, pass -AdminPassword."
}

if (-not (Get-Command psql -ErrorAction SilentlyContinue)) {
  throw "psql command not found. Install PostgreSQL client tools or use -UseDocker."
}

Write-Host "[postgres] Provisioning local PostgreSQL..."
$env:PGPASSWORD = $AdminPassword
$targetHost = if ([string]::IsNullOrWhiteSpace($dbHost)) { "localhost" } else { $dbHost }
$targetPort = if ([string]::IsNullOrWhiteSpace($dbPort)) { "5432" } else { $dbPort }

$sqlCreateRole = "DO `$`$ BEGIN IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = '$dbUser') THEN CREATE ROLE $dbUser LOGIN PASSWORD '$dbPassword'; ELSE ALTER ROLE $dbUser WITH LOGIN PASSWORD '$dbPassword'; END IF; END `$`$;"

psql -h $targetHost -p $targetPort -U $AdminUser -d postgres -v ON_ERROR_STOP=1 -c $sqlCreateRole

$dbExists = psql -h $targetHost -p $targetPort -U $AdminUser -d postgres -tAc "SELECT 1 FROM pg_database WHERE datname = '$dbName'" 2>$null
if ($dbExists -ne "1") {
  createdb -h $targetHost -p $targetPort -U $AdminUser -O $dbUser $dbName
}

Remove-Item Env:PGPASSWORD -ErrorAction SilentlyContinue
Write-Host "[postgres] Local PostgreSQL provisioned successfully."
