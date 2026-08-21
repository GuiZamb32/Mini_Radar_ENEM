#  Computação em Nuvem - Projetos & Atividades Práticas

Repositório voltado ao armazenamento e versionamento das atividades práticas, microsserviços e estudos de arquitetura desenvolvidos na disciplina de **Computação em Nuvem**.

---



##  Contexto da Aplicação: Mini Radar ENEM

A aplicação principal trabalhada ao longo do curso é o **Mini Radar ENEM**, uma API desenvolvida em Python (Flask) projetada para simular consultas, estatísticas e classificações de desempenho de estudantes no exame. O projeto evolui progressivamente de uma aplicação local até seu empacotamento, monitoramento de consumo e dimensionamento para nuvem.

---



##  Estrutura do Repositório

```text
.
├── Aula_03/                      # Containerização e Microsserviço v2
│   ├── app.py                    # Aplicação Flask com endpoints (/nota, /estatisticas)
│   ├── Dockerfile                # Configuração do build da imagem Docker (python:3.12-slim)
│   ├── requirements.txt          # Dependências do projeto
│   └── aula03.md                 # Questões conceituais sobre IaaS, PaaS e Docker
│
├── Aula_04/                      # Cloud Cost Challenge & Testes de Carga
│   ├── gerar_carga.py            # Script nativo em Python para teste de carga (1000 req)
│   └── aula04.md                 # Métricas do docker stats, custos e Ficha de Decisão
│
└── README.md                     # Documentação geral do repositório