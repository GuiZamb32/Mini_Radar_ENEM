import urllib.request
from datetime import datetime

url = "http://localhost:8080/nota/650"
total_requests = 1000
success = 0
errors = 0

print(f"Iniciando {total_requests} requisições em {datetime.now().strftime('%H:%M:%S')}")
print("-" * 50)

for i in range(total_requests):
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=2) as response:
            if response.status == 200:
                success += 1
            else:
                errors += 1
    except Exception as e:
        errors += 1

    if (i + 1) % 100 == 0:
        print(f"Progresso: {i+1}/{total_requests} requisições")

print("-" * 50)
print(f"Concluído em {datetime.now().strftime('%H:%M:%S')}")
print(f" Sucessos: {success}")
print(f" Erros: {errors}")
