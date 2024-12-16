import time
import threading

def consume_ram(target_ram_mb=1000):
    """
    Consomme une quantité définie de RAM en Mo et la maintient jusqu'à la fermeture.
    
    :param target_ram_mb: Quantité de RAM à consommer en Mo (par défaut 1000 Mo).
    """
    print(f"Allocation de {target_ram_mb} Mo de RAM...")
    
    try:
        # Créer une liste pour consommer la RAM
        large_data = [bytearray(1024 * 1024) for _ in range(target_ram_mb)]
        
        print(f"RAM consommée : {target_ram_mb} Mo")
        print("La mémoire est maintenue. Appuyez sur Ctrl+C pour terminer.")
        
        # Maintenir le programme actif
        while True:
            time.sleep(1)
            
    except MemoryError:
        print("Mémoire insuffisante ! Impossible d'allouer la quantité demandée.")
    finally:
        print("Libération de la mémoire...")
        del large_data  # Libérer la mémoire après utilisation

def stop_script():
    print("Temps écoulé. Arrêt du script.")
    sys.exit(0)

if __name__ == "__main__":
    import sys
    
    # Vérifier si l'utilisateur a fourni une valeur en argument
    if len(sys.argv) > 1:
        try:
            target_ram_mb = int(sys.argv[1])
        except ValueError:
            print("Veuillez fournir une valeur entière pour la quantité de RAM à consommer.")
            sys.exit(1)
    else:
        # Par défaut, consomme 1000 Mo
        target_ram_mb = 1000
    
    # Démarrer un timer pour arrêter le script après 2 minutes (120 secondes)
    timer = threading.Timer(120, stop_script)
    timer.start()
    
    consume_ram(target_ram_mb)
