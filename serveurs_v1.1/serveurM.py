import socket
import os
import time

class Server_M:

    def __init__(self, port_M=1234, server_M_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        # Partie serveur maître
        self.port_M = port_M
        self.server_M_socket = server_M_socket

    def servermaitre(self):
        self.server_M_socket.bind(('0.0.0.0', self.port_M))
        self.server_M_socket.listen(5)
        print(f"Serveur maître en écoute sur le port {self.port_M}...")

        while True:
            # Affiche les statistiques de la RAM à chaque itération
            os_detect = os.name

            if os_detect == 'posix':
                print('os linux')
                ram_stats = os.popen("free -m | awk '/Mem:/ {print \"RAM utilisée : \" $3 \" MB sur \" $2 \" MB\"}'").read().strip()
            elif os_detect == 'nt' :
                print('os windows')
                ram_stats = ram_stats = os.popen("wmic OS get FreePhysicalMemory,TotalVisibleMemorySize /Value").read().strip()
            else : 
                print('OS inconnus')

            print(ram_stats)
            time.sleep(1)  # Actualisation toutes les secondes

if __name__ == "__main__":
    server = Server_M()
    server.servermaitre()



"""

class Server_E():
    def __init__(self, port_E,server_E_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        #Partie server maitre
        self.port_E = port_E
        self.server_E_socket = server_E_socket
        
    

    def serveresclave(self):
        self.server_E_socket.bind(('0.0.0.0', self.port_E))
        self.server__E_socket.listen(5)
        print(f"Serveur esclave en écoute sur le port {self.port}...")



        """