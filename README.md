# SysReport

SysReport é uma aplicação composta por três serviços principais: **App**, **Redis** e **Grafana**, orquestrados via Docker Compose. O objetivo é fornecer um ambiente integrado para coleta, armazenamento e visualização de dados de relatórios do sistema.

## Estrutura do Projeto

```
SysReport/
├── app/           # Código-fonte principal da aplicação Python
│   ├── app.py
│   ├── settings.py
│   ├── settings.yaml
│   ├── requirements.txt
│   └── Dockerfile
├── redis/         # Serviço Redis customizado
│   ├── redis.conf
│   └── Dockerfile
├── grafana/       # Serviço Grafana customizado
│   ├── provisioning/
│   └── Dockerfile
├── compose.yaml   # Orquestração dos serviços via Docker Compose
└── run.ps1        # Script PowerShell para inicialização em Windows
```

## Serviços

### 1. App (Python)
- Localização: `app/`
- Função: Executa a lógica principal do SysReport, lê configurações do arquivo `settings.yaml`, conecta-se ao Redis e pode ser integrado ao Grafana.
- Configuração: Variáveis de ambiente para conexão com o Redis.

### 2. Redis
- Localização: `redis/`
- Função: Armazena dados temporários e persistentes para a aplicação.
- Configuração: Customizada via `redis.conf`.

### 3. Grafana
- Localização: `grafana/`
- Função: Visualização dos dados coletados pela aplicação.
- Configuração: Provisionamento automático e variáveis de ambiente para autenticação e permissões.

## Como Executar

### Pré-requisitos
- [Docker](https://www.docker.com/) e [Docker Compose](https://docs.docker.com/compose/)
- (Opcional) PowerShell para execução do script `run.ps1` no Windows

### Passos

#### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd SysReport
```

#### 2. Execute os serviços com Docker Compose
```bash
docker compose up -d
```

#### 3. (Opcional) Execute via PowerShell no Windows
Edite o caminho do projeto em `run.ps1` se necessário e execute:
```powershell
.\run.ps1
```

#### 4. Acesse os serviços
- **App:** Executado internamente, consulte logs ou endpoints conforme implementação.
- **Redis:** Porta `6379`
- **Grafana:** [http://localhost:3000](http://localhost:3000)  
  - Usuário: `admin`
  - Senha: `admin`

## Configuração

### settings.yaml
O arquivo `app/settings.yaml` contém as configurações da aplicação, como timeout e hosts.  
Exemplo:
```yaml
timeout: 30
hosts:
  - host1.example.com
  - host2.example.com
```

## Personalização

- Modifique `app/settings.yaml` para ajustar parâmetros da aplicação.
- Edite `redis/redis.conf` para configurações avançadas do Redis.
- Personalize dashboards e provisionamento em `grafana/provisioning/`.

---