# monitoramento_integrado.py
import subprocess
import json
import urllib.request
import time
from datetime import datetime
import threading
import os
import re

class MonitoramentoIntegrado:
    def __init__(self, container="radar-v2", arquivo_stats="stats.json", 
                 arquivo_reqs="requisicoes.json"):
        self.container = container
        self.arquivo_stats = arquivo_stats
        self.arquivo_reqs = arquivo_reqs
        self.stats = []
        self.requisicoes = []
        self.rodando = True
        self.total_requisicoes = 0
        
    def capturar_stats(self):
        while self.rodando:
            try:
                cmd = f"docker stats {self.container} --no-stream"
                resultado = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.DEVNULL)
                
                lines = resultado.strip().split('\n')
                if len(lines) >= 2:
                    data_line = lines[1]
                    parts = re.split(r'\s{2,}', data_line.strip())
                    
                    if len(parts) >= 7:
                        container = parts[0].replace('/', '').strip()
                        cpu = parts[1].strip()
                        mem_usage = parts[2].strip()
                        mem_perc = parts[3].strip()
                        net_io = parts[4].strip()
                        block_io = parts[5].strip()
                        pids = parts[6].strip()
                        
                        stats = {
                            'Container': container,
                            'CPUPerc': cpu,
                            'MemUsage': mem_usage,
                            'MemPerc': mem_perc,
                            'NetIO': net_io,
                            'BlockIO': block_io,
                            'PIDs': pids,
                            'timestamp': datetime.now().isoformat(),
                            'timestamp_ms': int(time.time() * 1000)
                        }
                        
                        self.stats.append(stats)
                        
                        with open(self.arquivo_stats, 'a', encoding='utf-8') as f:
                            f.write(json.dumps(stats) + '\n')
                
                time.sleep(2)
                
            except Exception:
                time.sleep(1)
    
    def fazer_requisicao(self, url="http://localhost:8080/nota/650"):
        inicio = time.time()
        timestamp = int(inicio * 1000)
        
        try:
            req_obj = urllib.request.Request(url)
            with urllib.request.urlopen(req_obj, timeout=2) as response:
                tempo = int((time.time() - inicio) * 1000)
                status_code = response.status
                
                req = {
                    'numero': self.total_requisicoes + 1,
                    'status': status_code,
                    'tempo_ms': tempo,
                    'timestamp': datetime.now().isoformat(),
                    'timestamp_ms': timestamp,
                    'sucesso': status_code == 200
                }
        except Exception as e:
            req = {
                'numero': self.total_requisicoes + 1,
                'status': 'ERROR',
                'tempo_ms': int((time.time() - inicio) * 1000),
                'timestamp': datetime.now().isoformat(),
                'timestamp_ms': timestamp,
                'sucesso': False,
                'erro': str(e)
            }
        
        self.total_requisicoes += 1
        self.requisicoes.append(req)
        
        with open(self.arquivo_reqs, 'a', encoding='utf-8') as f:
            f.write(json.dumps(req) + '\n')
        
        return req
    
    def executar_carga(self, total_requisicoes=100, delay=0.1):
        print(f"INICIANDO CARGA DE {total_requisicoes} REQUISIÇÕES")
        print(f"DELAY ENTRE REQUISIÇÕES: {delay}s")
        print("=" * 60)
        
        for i in range(total_requisicoes):
            req = self.fazer_requisicao()
            status_icon = "[OK]" if req['sucesso'] else "[ERRO]"
            print(f"{status_icon} Req {req['numero']:4d} | Status: {req['status']:>5} | {req['tempo_ms']:>4}ms")
            time.sleep(delay)
        
        print("=" * 60)
        print("CARGA FINALIZADA!")
    
    def executar(self, total_requisicoes=100, intervalo_stats=2, delay_requisicoes=0.1):
        for arquivo in [self.arquivo_stats, self.arquivo_reqs]:
            with open(arquivo, 'w', encoding='utf-8') as f:
                f.write('')
        
        thread_stats = threading.Thread(target=self.capturar_stats)
        thread_stats.daemon = True
        thread_stats.start()
        
        print("=" * 60)
        print("MONITORAMENTO INTEGRADO INICIADO")
        print("=" * 60)
        
        time.sleep(1)
        self.executar_carga(total_requisicoes, delay_requisicoes)
        
        self.rodando = False
        thread_stats.join(timeout=5)
        self.gerar_relatorio_final()
    
    def gerar_relatorio_final(self):
        print("\n" + "=" * 60)
        print("RELATÓRIO FINAL")
        print("=" * 60)
        
        total = len(self.requisicoes)
        sucessos = sum(1 for r in self.requisicoes if r['sucesso'])
        erros = total - sucessos
        tempos = [r['tempo_ms'] for r in self.requisicoes if r['tempo_ms'] > 0]
        
        print(f"\nREQUISIÇÕES:")
        print(f"   Total: {total}")
        print(f"   Sucessos: {sucessos} ({sucessos/total*100:.1f}%)" if total > 0 else "   Sucessos: 0")
        print(f"   Erros: {erros} ({erros/total*100:.1f}%)" if total > 0 else "   Erros: 0")
        if tempos:
            print(f"   Tempo médio: {sum(tempos)/len(tempos):.2f}ms")
            print(f"   Tempo mínimo: {min(tempos):.2f}ms")
            print(f"   Tempo máximo: {max(tempos):.2f}ms")
        
        cpus = []
        for s in self.stats:
            try:
                cpu = float(s['CPUPerc'].replace('%', ''))
                cpus.append(cpu)
            except:
                continue
        
        if cpus:
            print(f"\nCPU:")
            print(f"   Mínimo: {min(cpus):.2f}%")
            print(f"   Máximo: {max(cpus):.2f}%")
            print(f"   Média: {sum(cpus)/len(cpus):.2f}%")
        
        mems = []
        for s in self.stats:
            try:
                mem_usage = s['MemUsage']
                parts = mem_usage.split()
                if len(parts) >= 1:
                    mem_num = float(parts[0])
                    if len(parts) >= 2 and 'G' in parts[1]:
                        mem_num = mem_num * 1024
                    mems.append(mem_num)
            except:
                continue
        
        if mems:
            print(f"\nMEMÓRIA:")
            print(f"   Mínimo: {min(mems):.2f} MB")
            print(f"   Máximo: {max(mems):.2f} MB")
            print(f"   Média: {sum(mems)/len(mems):.2f} MB")

if __name__ == "__main__":
    monitor = MonitoramentoIntegrado()
    monitor.executar(total_requisicoes=100, intervalo_stats=2, delay_requisicoes=0.1)
