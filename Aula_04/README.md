# Atividade Prática - Aula 4: Cloud Cost Challenge

## 1. Observação de Consumo (docker stats)

| Métrica | Sem Carga | Durante a Carga (1000 req) | Interpretação |
| :--- | :--- | :--- | :--- |
| **CPU** | 0.03% | ~25% - 40% | Aumento pontual provocado pelo processamento das 1000 chamadas em 9 segundos. |
| **Memória** | 22.44 MiB | ~28.5 MiB | Uso extremamente baixo e estável em container Python slim. |
| **NET I/O** | 5.11 kB / 3.77 kB | ~320 kB / ~210 kB | Tráfego de entrada e saída gerado pelos payloads JSON. |
| **BLOCK I/O** | 0 B / 176 kB | 0 B / 176 kB | Escritas pontuais de inicialização do container; 0 escritas durante a carga. |

---

## 2. Dimensionamento da Arquitetura

| Questão | Resposta do Grupo |
| :--- | :--- |
| **Carga esperada** | Média de 10.000 requisições/dia com picos no período do ENEM. |
| **Usuários/requisições** | Até 500 requisições simultâneas em horários de pico. |
| **Disponibilidade** | 99.5% de disponibilidade esperada. |
| **Crescimento dos dados** | Baixo volume de dados (apenas logs de acesso e estatísticas). |
| **Uso constante ou sazonal?** | **Sazonal**: Picos intensos perto da divulgação do gabarito/notas do ENEM. |
| **Tempo de resposta aceitável** | < 200 ms por consulta. |

---

## 3. Estimativa e Cálculo de Custos com Python

* **Cenário A (VM Pequena 24/7):** R$ 0,20/h * 24h * 30 dias = **R$ 144,00/mês**
* **Cenário B (VM Pequena 8h/dia):** R$ 0,20/h * 8h * 30 dias = **R$ 48,00/mês**
* **Cenário C (VM Maior 24/7):** R$ 0,40/h * 24h * 30 dias = **R$ 288,00/mês**

---

## 4. Ficha de Decisão Arquitetural

| Item | Preenchimento |
| :--- | :--- |
| **Modelo de Implantação** | Público |
| **Modelo de Serviço** | IaaS |
| **Computação** | 1 Instância VM Pequena (2 vCPU, 4 GB RAM) |
| **Armazenamento** | 20 GB SSD |
| **Banco de Dados** | SQLite interno / Banco relacional leve |
| **Custo Mensal Estimado** | **R$ 144,00** |
| **Principal Risco** | Ponto único de falha (SPOF) sem escala automática sob pico extremo. |
| **Como Reduzir Custo?** | Desligar ambientes de teste/desenvolvimento fora do expediente (R$ 48,00). |
| **Alternativa Rejeitada** | **VM Maior (R$ 288,00/mês):** Superdimensionada diante do consumo real de apenas ~28 MiB de RAM. |

---

## 5. Justificativa e Roteiro de Apresentação (2 Minutos)

* **Por que escolheram essa arquitetura?** A VM Pequena (IaaS - R$ 144,00) suportou a carga de 1.000 requisições em 9s utilizando menos de 30 MB de RAM, garantindo folga de recursos no orçamento de R$ 300,00.
* **Como estimaram o custo?** Multiplicando o valor da hora (R$ 0,20) por 24 horas ao longo de 30 dias.
* **Qual o principal risco?** Ponto único de falha na VM em caso de indisponibilidade do host.
* **Se a demanda dobrar?** A aplicação consumirá ~50 MB de RAM e a CPU absorverá o pico sem esgotar a VM. Se o limite for atingido, podemos migrar para a VM Maior de R$ 288,00/mês, ainda dentro do teto orçamentário.
* **Como reduzir custos?** Agendando o desligamento de instâncias não-críticas fora do horário comercial.