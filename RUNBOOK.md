# Runbook operacional - Radar ENEM

## 1. Descrição

O Mini Radar ENEM é uma API Flask para consultas simuladas de notas e estatísticas. A versão operacional desta atividade é a `v3`; ela identifica versão, ambiente e instância na resposta de `/` e registra requisições em logs estruturados simples.

## 2. Pré-requisitos

- Docker Desktop/Engine em execução;
- `curl` para os testes locais;
- Porta `5000` livre no computador hospedeiro.

## 3. Configuração

Crie o arquivo local de configuração a partir do exemplo:

```powershell
Copy-Item .env.example .env
```

| Variável | Finalidade | Exemplo |
| --- | --- | --- |
| `AMBIENTE` | Identifica o ambiente de execução | `producao` |
| `INSTANCIA_NOME` | Identifica a instância nos retornos e logs | `radar-enem-prod-01` |
| `APP_VERSION` | Identifica a versão implantada | `v3` |
| `LOG_LEVEL` | Nível de detalhamento dos logs | `INFO` |

Não há credenciais na aplicação. Credenciais futuras devem ser fornecidas por um cofre de segredos ou variável de ambiente no ambiente de execução; nunca no código, em imagens ou no Git.

## 4. Inicialização

```powershell
docker compose up -d --build
docker compose ps
curl http://localhost:5000/health
```

Resposta esperada: JSON com `"status":"healthy"`, versão e ambiente. Para executar sem Compose:

```powershell
docker build -t radar-enem:v3 .
docker run -d --name radar-enem -p 127.0.0.1:5000:5000 --env-file .env radar-enem:v3
```

## 5. Health check, logs e monitoramento

```powershell
curl http://localhost:5000/health
docker inspect --format='{{.State.Health.Status}}' radar-enem
docker logs --tail 100 radar-enem
docker stats --no-stream radar-enem
```

O `HEALTHCHECK` interno consulta `http://127.0.0.1:5000/health` a cada 30 segundos. Registre na entrega a resposta do health check, os logs relevantes e os valores de CPU/memória observados.

## 6. Portas e segurança

- `5000/TCP`: API HTTP; é a única porta que precisa ser acessível ao usuário.
- A publicação usa `127.0.0.1:5000:5000`, portanto o serviço fica disponível apenas no host local. Em uma VM, libere no firewall somente a origem necessária ou coloque a API atrás de proxy/reverse proxy HTTPS.
- Não existem banco de dados, fila ou painel administrativo neste laboratório. Se existirem, devem ficar em rede interna, sem publicação de porta ao usuário.
- O `.dockerignore` reduz arquivos desnecessários enviados para a imagem. O arquivo `.env` é ignorado pelo Docker e não deve ser versionado.

Em IaaS, a equipe é responsável pela VM, sistema operacional, firewall, Docker, aplicação, logs e patches; o provedor responde pela infraestrutura física e virtualização.

## 7. Incidente e recuperação

1. Detectar, sem reiniciar imediatamente:

   ```powershell
   docker ps
   curl http://localhost:5000/health
   ```

2. Investigar:

   ```powershell
   docker ps -a
   docker logs radar-enem
   docker inspect radar-enem
   docker stats --no-stream radar-enem
   ```

3. Registrar causa e evidência. Exemplo de simulação: pare o container com `docker stop radar-enem`; a evidência será o estado `Exited` e a falha de conexão no health check.
4. Recuperar e validar:

   ```powershell
   docker start radar-enem
   curl http://localhost:5000/health
   ```

Registro da simulação: detecção por health check sem resposta; causa simulada: container parado; ação: `docker start`; resultado esperado: endpoint retorna HTTP 200 e `healthy`.

## 8. Atualização e rollback

Mudança v2 -> v3: a resposta principal passou a identificar `versao` e `ambiente`; logs de requisições foram adicionados e o container ganhou health check.

```powershell
docker build -t radar-enem:v3 .
docker stop radar-enem
docker rm radar-enem
docker run -d --name radar-enem -p 127.0.0.1:5000:5000 --env-file .env radar-enem:v3
curl http://localhost:5000/
curl http://localhost:5000/health
```

Para rollback, preserve a imagem anterior e recrie o container com ela:

```powershell
docker stop radar-enem
docker rm radar-enem
docker run -d --name radar-enem -p 127.0.0.1:5000:5000 --env-file .env radar-enem:v2
```

Em produção, registre data/hora, responsável, tags de imagem, saída dos health checks, logs, métricas, motivo da alteração e resultado/rollback.
