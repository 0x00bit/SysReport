# run-docker-project.ps1

# Caminho do projeto (ajuste para onde está o docker-compose.yml)
$ProjectPath = "C:\Temp"

function Install-Docker {
    $InstallerPath = "$env:TEMP\DockerDesktopInstaller.exe"
    $DockerUrl = "https://desktop.docker.com/win/main/amd64/Docker%20Desktop%20Installer.exe"

    Write-Host "Baixando Docker Desktop..."
    Invoke-WebRequest -Uri $DockerUrl -OutFile $InstallerPath

    Write-Host "Instalando Docker Desktop (modo silencioso)..."
    Start-Process -FilePath $InstallerPath -ArgumentList "install", "--quiet" -Wait -NoNewWindow

    Write-Host "Docker Desktop instalado!"
    Write-Host "Iniciando Docker Desktop..."
    Start-Process "C:\Program Files\Docker\Docker\Docker Desktop.exe"

    # Aguarda o Docker inicializar
    Write-Host "Aguardando Docker iniciar..."
    Start-Sleep -Seconds 30
}

# --- MAIN ---
Write-Host "Verificando se o Docker já está instalado..."

try {
    $dockerVersion = docker --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Docker já está instalado: $dockerVersion"
    } else {
        Write-Host "Docker não encontrado, instalando..."
        Install-Docker
    }
}
catch {
    Write-Host "Docker não encontrado, instalando..."
    Install-Docker
}

# Entrar no diretório do projeto
Set-Location $ProjectPath

Write-Host "Rodando docker compose up..."
docker compose up -d

Write-Host "Projeto iniciado com sucesso!"