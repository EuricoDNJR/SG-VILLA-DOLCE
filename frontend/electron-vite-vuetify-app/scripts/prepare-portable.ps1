Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectDir = Resolve-Path (Join-Path $scriptDir "..")
$distDir = Join-Path $projectDir "dist"
$winUnpackedDir = Join-Path $distDir "win-unpacked"
$portableDir = Join-Path $distDir "portable"
$packageJsonPath = Join-Path $projectDir "package.json"

if (-not (Test-Path $winUnpackedDir)) {
  throw "Folder '$winUnpackedDir' not found. Run 'npm run build:win' first."
}

$packageJson = Get-Content $packageJsonPath | ConvertFrom-Json
$version = $packageJson.version
$zipPath = Join-Path $distDir "sg-villa-dolce-acai-$version-portable.zip"

Write-Host "[portable] Preparing portable directory..."
if (Test-Path $portableDir) {
  attrib -R (Join-Path $portableDir "*") /S /D 2>$null
  try {
    Remove-Item -Path $portableDir -Recurse -Force -ErrorAction Stop
  } catch {
    cmd /c "rmdir /s /q `"$portableDir`""
  }
}
New-Item -Path $portableDir -ItemType Directory | Out-Null

Copy-Item -Path (Join-Path $winUnpackedDir "*") -Destination $portableDir -Recurse -Force

$launcherPath = Join-Path $portableDir "Iniciar-SG-Villa-Dolce.bat"
$launcherContent = "@echo off`r`ncd /d %~dp0`r`nstart `"`" `"`"electron-vue-app.exe`"`"`r`n"
Set-Content -Path $launcherPath -Value $launcherContent -Encoding ASCII

$readmePath = Join-Path $portableDir "README-PORTABLE.txt"
$readmeContent = @"
1) Execute Iniciar-SG-Villa-Dolce.bat para abrir o sistema.
2) O PostgreSQL precisa estar ativo com as credenciais do .env.
3) Nao mova arquivos internos da pasta portable.
"@
Set-Content -Path $readmePath -Value $readmeContent -Encoding ASCII

if (Test-Path $zipPath) {
  Remove-Item -Path $zipPath -Force
}

Write-Host "[portable] Creating zip package..."
$maxAttempts = 5
$zipCreated = $false
for ($i = 1; $i -le $maxAttempts; $i++) {
  try {
    Compress-Archive -Path (Join-Path $portableDir "*") -DestinationPath $zipPath -CompressionLevel Optimal
    $zipCreated = $true
    break
  } catch {
    Write-Warning "[portable] Zip attempt $i failed due to file lock. Retrying..."
    Start-Sleep -Seconds 2
  }
}

if ($zipCreated) {
  Write-Host "[portable] Done: $zipPath"
} else {
  Write-Warning "[portable] Zip could not be created, but the portable folder is ready at '$portableDir'."
}
