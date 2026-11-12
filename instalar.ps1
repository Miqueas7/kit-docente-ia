# Kit docente IA: instalación de la carpeta Mi curso
# Uso (en PowerShell):  irm https://raw.githubusercontent.com/Miqueas7/kit-docente-ia/main/instalar.ps1 | iex
# Instala Python y Antigravity si faltan, descarga el material y lo deja listo. No borra nada tuyo.

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
$repo = 'https://github.com/Miqueas7/kit-docente-ia/archive/refs/heads/main.zip'

function Paso($t) { Write-Host "`n>> $t" -ForegroundColor Yellow }
function Recargar-Path {
    $env:Path = [Environment]::GetEnvironmentVariable('Path', 'Machine') + ';' + [Environment]::GetEnvironmentVariable('Path', 'User')
}
function Instalar-Winget($id, $nombre) {
    if (-not (Get-Command winget -ErrorAction SilentlyContinue)) {
        throw "No se encontró winget. Instala $nombre a mano (ver el instructivo) y vuelve a ejecutar."
    }
    winget install -e --id $id --scope user --silent --accept-package-agreements --accept-source-agreements | Out-Null
    if ($LASTEXITCODE -ne 0) {  # algunos paquetes no se instalan solo para el usuario
        winget install -e --id $id --silent --accept-package-agreements --accept-source-agreements | Out-Null
    }
    if ($LASTEXITCODE -ne 0) { throw "No se pudo instalar $nombre. Toma una captura y envíasela al facilitador." }
    Recargar-Path
}

Write-Host 'Kit docente IA · instalación de Mi curso' -ForegroundColor Cyan

Paso 'Python'
$py = Get-Command py -ErrorAction SilentlyContinue
if (-not $py) {
    Write-Host '   No está instalado: instalando Python 3.12 (unos minutos)...'
    Instalar-Winget 'Python.Python.3.12' 'Python'
    $py = Get-Command py -ErrorAction SilentlyContinue
    if (-not $py) { throw 'Python se instaló, pero esta ventana aún no lo ve. Ciérrala, abre otra y vuelve a pegar el comando.' }
}
Write-Host "   Listo: $(& py -3 --version)"

Paso 'Antigravity'
$ag = winget list -e --id Google.AntigravityIDE --accept-source-agreements | Select-String 'Antigravity'
if ($ag) { Write-Host '   Ya está instalado.' }
else {
    Write-Host '   No está instalado: instalando Antigravity (unos minutos)...'
    Instalar-Winget 'Google.AntigravityIDE' 'Antigravity'
    Write-Host '   Listo. Al abrirlo, entra con tu Gmail personal (no con tu correo institucional).'
}

Paso 'Descargando el material'
$tmp = Join-Path $env:TEMP ('kit-docente-ia-' + [guid]::NewGuid().ToString('N').Substring(0, 8))
New-Item -ItemType Directory -Path $tmp | Out-Null
Invoke-WebRequest $repo -OutFile "$tmp\kit.zip" -UseBasicParsing
Expand-Archive "$tmp\kit.zip" -DestinationPath $tmp
$kit = Get-ChildItem $tmp -Directory | Select-Object -First 1
Write-Host '   Descargado.'

& py -3 "$($kit.FullName)\instalar.py" --sin-pausa
$codigo = $LASTEXITCODE
Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue
if ($codigo -eq 0) {
    $docs = [Environment]::GetFolderPath('MyDocuments')
    Start-Process explorer.exe (Join-Path $docs 'Kit docente IA')
}
