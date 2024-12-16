import subprocess
import time

while True:
    try:
        result = subprocess.run(['docker', 'stats', '--no-stream', '--format', '{{.Name}}\t{{.MemPerc}}'], stdout=subprocess.PIPE)
        containers_stats = result.stdout.decode('utf-8').strip().split('\n')
        
        mem_usage = {}
        for line in containers_stats:
            name, mem_perc = line.split('\t')
            # Supprimer le symbole % à la fin
            mem_usage[name] = mem_perc.rstrip('%')
        
        sae_server_esclave1_1 = mem_usage.get('sae-server-esclave1-1', 'N/A')
        sae_server_esclave2_1 = mem_usage.get('sae-server-esclave2-1', 'N/A')
        sae_server_esclave3_1 = mem_usage.get('sae-server-esclave3-1', 'N/A')
        sae_server_esclave4_1 = mem_usage.get('sae-server-esclave4-1', 'N/A')
        
        print(f"sae-server-esclave1-1: {sae_server_esclave1_1}")
        print(f"sae-server-esclave2-1: {sae_server_esclave2_1}")
        print(f"sae-server-esclave3-1: {sae_server_esclave3_1}")
        print(f"sae-server-esclave4-1: {sae_server_esclave4_1}")
        
    except Exception as e:
        print(f"An error occurred: {e}")
    time.sleep(5)
