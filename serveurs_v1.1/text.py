import time

def consume_ram(duration=120):
    print(f"Consommation intensive de RAM pendant {duration} secondes...")
    
    try:
        large_data = []  # Initialisation de la liste principale
        
        start_time = time.time()
        while time.time() - start_time < duration:
            # Chaque itération ajoute environ 100 Mo à la RAM
            large_data.append(bytearray(100 * 1024 * 1024))  # 100 Mo par itération
            time.sleep(1)  # Pause d'une seconde entre les ajouts
            
            print(f"RAM consommée : {len(large_data) * 100} Mo")
        
    except MemoryError:
        print("Mémoire insuffisante ! Le processus s'est arrêté à cause d'une surcharge.")
    finally:
        print("Libération de la mémoire...")
        del large_data  # Libérer la mémoire après utilisation

if __name__ == "__main__":
    consume_ram()
