# Respostas Conceituais - Atividade Prática Aula 3

## 1. O que foi necessário instalar e configurar para executar a aplicação sem Docker?
Foi necessário possuir o interpretador Python 3 instalado no sistema operacional, criar e ativar um ambiente virtual (venv), instalar as dependências via pip (Flask) e configurar manualmente as variáveis de ambiente e portas no sistema hospedeiro.

## 2. O que o Docker passou a empacotar ou padronizar?
O Docker padronizou todo o ambiente de execução: a distribuição OS (Linux slim), a versão exata do Python, o código da aplicação e suas dependências isoladas. Isso garante que a aplicação rode exatamente da mesma forma em qualquer ambiente.

## 3. Se o container for executado em uma VM IaaS, quais responsabilidades ainda ficam com a equipe?
A equipe continua responsável por atualizar o sistema operacional da VM, gerenciar o runtime do Docker, aplicar patches de segurança, configurar firewalls/grupos de segurança, monitorar a saúde da VM e criar regras de auto-scaling e balanceamento de carga.

## 4. O que um PaaS poderia assumir automaticamente?
Um PaaS assumiria o gerenciamento e manutenção do sistema operacional subjacente, o runtime da aplicação, o provisionamento automático de recursos, health checks com restart automático em caso de queda, suporte nativo a SSL/TLS e escalabilidade automática conforme a demanda.

## 5. Por que Docker não pode ser classificado, sozinho, como IaaS, PaaS ou SaaS?
O Docker é uma tecnologia de empacotamento e runtime de containers. Ele não fornece a infraestrutura virtualizada subjacente (IaaS), nem a plataforma totalmente gerenciada com orquestração (PaaS), e tampouco é um software pronto para uso do usuário final (SaaS). Ele é uma ferramenta usada dentro desses modelos de serviço.