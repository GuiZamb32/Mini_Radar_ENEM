# Mini Radar ENEM

Projeto acadêmico desenvolvido na disciplina de **Computação em Nuvem**, com foco na construção, containerização, teste de carga, análise de custos e operação de uma API relacionada ao contexto do ENEM.

O repositório acompanha a evolução do **Mini Radar ENEM** ao longo das atividades práticas, partindo de uma aplicação Flask local e avançando para um serviço containerizado com Docker, monitoramento de recursos, simulação de carga e práticas básicas de operação em ambiente produtivo.

---

## Sobre o projeto

O **Mini Radar ENEM** é uma API REST desenvolvida em **Python + Flask** que simula consultas relacionadas ao desempenho de estudantes.

A aplicação disponibiliza endpoints para:

- Verificar a saúde do serviço;
- Consultar uma nota simulada;
- Classificar uma nota em relação ao valor de 600 pontos;
- Consultar um estudante pelo nome;
- Consultar estatísticas simuladas;
- Identificar ambiente, instância e versão da aplicação;
- Registrar as requisições realizadas no serviço.

O objetivo principal do projeto não é representar um sistema real de consulta de resultados do ENEM, mas servir como aplicação de laboratório para estudar conceitos de **Computação em Nuvem, Docker, IaaS, monitoramento, testes de carga, custos e operação de serviços**.

---

## Evolução do projeto

O projeto foi desenvolvido de forma incremental durante as atividades da disciplina.

| Etapa | Tema | Principais conceitos |
| :--- | :--- | :--- |
| **Aula 03** | Containerização | Flask, Python, Docker, variáveis de ambiente, IaaS, PaaS e SaaS |
| **Aula 04** | Cloud Cost Challenge | Teste de carga, `docker stats`, consumo de CPU/memória, dimensionamento e estimativa de custos |
| **Aula 07** | Operação em ambiente produtivo simulado | Health check, logs, monitoramento, configuração por ambiente, recuperação, atualização e rollback |

A versão operacional trabalhada na **Aula 07** representa a evolução do serviço para uma execução mais próxima de um cenário de produção, utilizando Docker e práticas básicas de operação.

---

## Tecnologias utilizadas

### Aplicação

- Python
- Flask

### Cloud e infraestrutura

- Docker
- Docker Compose
- Container Linux baseado em `python:3.12-slim`
- Modelo de serviço estudado: IaaS

### Testes e monitoramento

- Python
- Docker Stats
- Health Check
- Logs estruturados
- Simulação de carga HTTP

---

## Arquitetura atual

```text
                    Usuário / Cliente
                           |
                           v
                  127.0.0.1:5000
                           |
                           v
              +------------------------+
              |    Container Docker    |
              |      radar-enem:v3     |
              |                        |
              |       Flask API        |
              |                        |
              |  GET /                 |
              |  GET /health           |
              |  GET /aluno/<nome>     |
              |  GET /nota/<nota>      |
              |  GET /estatisticas     |
              +------------------------+
                    |             |
                    v             v
              Health Check    Docker Logs
                    |
                    v
              Docker Stats
