# Arquitetura atual

```text
Usuário local
     |
     v
127.0.0.1:5000/TCP (única porta publicada)
     |
     v
[ Container radar-enem:v3 ]
     |-- GET /health  -> Docker HEALTHCHECK
     |-- stdout/stderr -> docker logs
     `-- recursos      -> docker stats (CPU/memória)
```

Serviços de dados, filas e administração não fazem parte deste laboratório. Caso sejam adicionados, devem permanecer em rede interna e sem portas publicadas diretamente ao usuário.
