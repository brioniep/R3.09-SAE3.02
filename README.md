# PROJET SAE-3.02 : Conception et Développement d’une Architecture Multi-Serveurs pour Compilation et Exécution de Programmes

## Présentation du projet

Ce projet permet d'envoyer à un serveur maître des fichiers de type C, C++, Java et Python depuis un client avec une interface graphique. Une fois les fichiers envoyés, le serveur maître répartit les charges vers différents serveurs esclaves pour qu'ils les exécutent et renvoient le résultat de l'exécution. Les serveurs esclaves sont dans des conteneurs Docker pour mieux les gérer et sécuriser la machine hôte.

Ce dépôt contient deux dossiers principaux : un pour le client et un pour le serveur. Il y a également deux branches dans ce dépôt :
- Une branche pour la ressource qui a permis d'avoir une première approche de socket et thread. [branche R3.09](https://github.com/brioniep/R3.09-SAE3.02/tree/R3.09)
- Une deuxième branche qui montre l'avancement de ce projet. [branche SAE3.02](https://github.com/brioniep/R3.09-SAE3.02/tree/SAE3.02)
- Voici une vidéo de démonstration du projet
(mettre la vidéo de 3 min en mettant l'accent sur la répartition de charge)


<video width="640" height="360" controls>
    <source src="./v2.mp4" type="video/mp4">
    Your browser does not support the video tag.
</video>




Ce README est divisé en trois grandes parties :

1. [Documentation d'installation](#documentation-dinstallation)
2. [Documentation Utilisateur](#documentation-utilisateur)
3. [Documentation Programmeur](#documentation-programmeur)


# Documentation d'installation

### Table des matières

- [Installation des dépendances 🚀](#installation-des-dépendances-🚀)
- [Mise en place des fichiers sur le serveur Linux 📂](#mise-en-place-des-fichiers-sur-le-serveur-linux-📂)
- [Construction des conteneurs 🛠️](#construction-des-conteneurs-🛠️)
- [Lancement des serveurs 🚀](#lancement-des-serveurs-🚀)
- [Lancement du client](#lancement-du-client)

## Installation des dépendances 🚀

### Docker 🐳

Docker est une plateforme permettant de développer, livrer et exécuter des applications dans des conteneurs. Pour installer Docker sur le serveur Linux, suivez les étapes suivantes :

1. Mettez à jour votre liste de paquets :
    ```bash
    sudo apt update -y && sudo apt upgrade -y
    ```

2. Installez Docker :
    ```bash
    sudo apt install docker.io
    ```

### Docker Compose 📦

Docker Compose est un outil pour définir et gérer des applications multi-conteneurs Docker.

Téléchargez la version stable de Docker Compose sur le serveur :
```bash
sudo apt install docker-compose
```




### Python et librairies nécessaires 🐍

Cette partie est à faire chez le client. Pour installer Python et les librairies nécessaires au projet, suivez ces étapes :

1. Installez Python :
    ```bash
    sudo apt-get install python3 python3-pip
    ```

2. Installez les librairies nécessaires :
    ```bash
    pip3 install pyqt6
    ```

## Mise en place des fichiers sur le serveur Linux 📂

- Pour transférer les fichiers sur le serveur Linux, vous pouvez utiliser FileZilla. Téléchargez FileZilla depuis leur [site officiel](https://filezilla-project.org/).

1. Installez ssh sur le serveur :
    ```bash
    sudo apt install openssh-server
    ```

2. Vérifiez l'état du service ssh :
    ```bash
    sudo systemctl status ssh
    ```

À la fin de ces installations, vous pouvez enfin utiliser FileZilla pour transférer les fichiers nécessaires sur le serveur Linux.

## Construction des conteneurs 🛠️

Pour construire et démarrer les conteneurs, utilisez la commande suivante dans le répertoire `SERVER-FILE` 
```bash
docker-compose up --build
```
> ⚠️ **Avertissement** : cette commande peut mettre quelques minutes à s'exécuter dû à l'installation de 16 paquets. Si un problème survient pendant l'installation (par exemple, si vous avez interrompu le processus avec `Ctrl+C`), il est recommandé de supprimer les conteneurs avant de relancer la commande ci-dessus. Utilisez les commandes suivantes pour nettoyer votre environnement Docker :

```bash
docker-compose down
docker-compose down --volumes
docker-compose down --rmi all
docker system prune -a --volumes
```
## Lancement des serveurs 🚀

Pour lancer les serveurs esclaves, utilisez la commande suivante dans le répertoire `SERVER-FILE` :

> **Note** : Si vous avez déjà exécuté la commande `docker-compose up --build` juste avant, il n'est pas nécessaire de relancer cette commande.
```bash
docker-compose up
```



Pour lancer le serveur maître, utilisez la commande suivante dans le répertoire `SERVER-FILE/server-maitre/` :
```bash
python3 server.py
```

## Lancement du client
Pour lancer l'application client, utilisez la commande suivante adns le répertoire  `CLIENT-GUI` :
```bash
python3 connexion.py
```

> **Note** : Le nom d'utilisateur par défaut est "toto" et le mot de passe par défaut est également "toto". Si vous avez besoin de changer ces identifiants, veuillez consulter la documentation développeur.








# Documentation Utilisateur

### Table des matières

- [Introduction](#introduction)
- [Options de l'Application](#options-de-lapplication)
    - [🔒 Sécurité](#-sécurité)
    - [📊 Surveillance](#-surveillance)
    - [🔗 Connexion au Serveur](#-connexion-au-serveur)
    - [📁 Transfert de Fichiers](#-transfert-de-fichiers)
    - [📄 Affichage des Résultats](#-affichage-des-résultats)
- [Options des Serveurs Maître / Esclaves](#options-des-serveurs-maître--esclaves)
    - [🔒 Sécurité](#-sécurité-1)
    - [🆔 Identification Client](#-identification-client)
    - [⚖️ Répartition des Charges](#-répartition-des-charges)
    - [🔄 Multitâches](#-multitâches)

---

## Introduction

Cette application client se connecte à un **serveur maître** pour envoyer des fichiers à traiter et recevoir les résultats. Elle propose une interface graphique conviviale et simple d’utilisation. 

Ce guide présente les fonctionnalités principales et le fonctionnement de l'application. Si vous souhaitez une analyse technique plus approfondie, consultez la [documentation développeur](#documentation-développeur).

---

## Options de l'Application

### 🔒 Sécurité
L'accès à la fonctionnalité de transfert de fichiers (via `index.py`) est protégé par un système d'authentification. Vous devez vous connecter avant de pouvoir envoyer des fichiers aux serveurs.

### 📊 Surveillance
L'application dispose d'une fonctionnalité de journalisation (logs) permettant :
- De suivre vos actions dans l'application.
- De vérifier l'état de la connexion avec le serveur maître.
- De recevoir des notifications en cas de déconnexion ou d'échec d'envoi des fichiers.

### 🔗 Connexion au Serveur
L'application effectue une vérification continue de la connexion avec le serveur maître toutes les 5 secondes. Si la connexion est rompue, un message d'erreur s'affichera dans les logs.

### 📁 Transfert de Fichiers
- Cette fonctionnalité ne s'active que si la connexion avec le serveur maître est établie.
- Seuls les fichiers au format C, C++, Java ou Python sont acceptés. Un message d'erreur s'affiche si un fichier non conforme est sélectionné.

### 📄 Affichage des Résultats
Une fois le traitement terminé, les résultats s’affichent dans la partie droite de l’interface avec :
- Le nom du fichier.
- Les résultats d'exécution, même en cas d'erreur dans le code, pour permettre une correction.

---

## Options des Serveurs Maître / Esclaves

### 🔒 Sécurité
- Les serveurs esclaves sont isolés dans des conteneurs, tandis que le serveur maître ne l’est pas.
- Les serveurs esclaves exécutent le code sans accès à la machine hôte, ce qui réduit les risques en cas de fichiers malveillants.

### 🆔 Identification Client
Lorsqu'un client se connecte, le serveur maître lui attribue un identifiant unique. Cela permet :
- Une meilleure traçabilité des fichiers.
- Un retour rapide et fiable des résultats.

### ⚖️ Répartition des Charges
Le serveur maître répartit les fichiers vers les serveurs esclaves selon deux critères :
1. **Type de fichier** :
   - **Serveur-esclave-1** : Fichiers Python.
   - **Serveur-esclave-2** : Fichiers C.
   - **Serveur-esclave-3** : Fichiers C++.
   - **Serveur-esclave-4** : Fichiers Java.
   
2. **Utilisation de la RAM** :
   - Si la RAM d'un serveur esclave dépasse 60%, le serveur maître redirige le fichier vers un autre serveur disponible.
   - Si tous les serveurs sont surchargés, le fichier est envoyé selon la priorité de langage.

Cette double répartition optimise la charge des serveurs et évite les surcharges inutiles.

### 🔄 Multitâches
Le serveur maître est divisé en deux fonctions principales :
1. Réception des fichiers des clients et envoi vers les serveurs esclaves.
2. Réception des résultats des serveurs esclaves et renvoi vers les clients.

Les serveurs esclaves peuvent traiter et retourner plusieurs fichiers simultanément, garantissant un fonctionnement fluide et rapide.

---













# Documentation Développeur 📚

### Table des matières 📑

- [Structure du Projet 🏗️](#structure-du-projet-)
- [Fonctionnalités Principales 🌟](#fonctionnalités-principales-)
    - [Connexion au Serveur 🔗](#connexion-au-serveur-🔗)
    - [Transfert de Fichiers 📁](#transfert-de-fichiers-📁)
    - [Réception de Données 📥](#réception-de-données-📥)
    - [Affichage des Résultats 📄](#affichage-des-résultats-📄)
- [Serveur Maître 🖥️](#serveur-maître-🖥️)
    - [Gestion des Clients 👥](#gestion-des-clients-👥)
    - [Répartition des Charges ⚖️](#répartition-des-charges-⚖️)
- [Serveurs Esclaves 🛠️](#serveurs-esclaves-🛠️)
- [Sécurité 🔒](#sécurité-🔒)

---

## Structure du Projet 🏗️

Le projet est divisé en plusieurs dossiers et fichiers principaux :

- `CLIENT-GUI/` : Contient le code source de l'application client avec l'interface graphique.
- `SERVER-FILE/` : Contient le code source du serveur maître et des serveurs esclaves.
- `README.md` : Documentation du projet.

---

## Fonctionnalités Principales 🌟

### Connexion au Serveur 🔗

La connexion au serveur est gérée par la méthode `connexion_au_serveur` dans `CLIENT-GUI/index.py` :

```py
def connexion_au_serveur(self):
        ip = self.ip_input.text()
        port = self.port_input.text()

        ip_regex = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
        if not ip_regex.match(ip):
                QMessageBox.warning(self, "Erreur de syntaxe", "L'adresse IP est incorrecte.")
                return

        if not port.isdigit() or not (0 <= int(port) <= 65535):
                QMessageBox.warning(self, "Erreur de syntaxe", "Le port est incorrect.")
                return

        port = int(port)

        if self.est_connecte:
                self.historique_logs.append("<span style='color: red;'>[-]</span> Déjà connecté au serveur.")
                return

        try:
                self.socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket_client.connect((ip, port))
                self.est_connecte = True
                self.selection_fichier.setEnabled(True)
                self.telecharger.setEnabled(True)

                self.recepteur_thread = QThread(self)
                self.recepteur_thread.run = self.recevoir_donnees
                self.recepteur_thread.start()

                self.historique_logs.append(f"<span style='color: green;'>[+]</span>Connexion réussie à {ip}:{port}")

        except Exception as e:
                self.historique_logs.append(f"<span style='color: red;'>[-]</span> Erreur lors de la connexion : {e}")
                print(f"[-] Erreur lors de la connexion : {e}")
```

### Transfert de Fichiers 📁

Le transfert de fichiers est géré par la méthode `envoyer_fichier` dans `CLIENT-GUI/index.py` :

```py
def envoyer_fichier(self):
        if not self.est_connecte:
                self.historique_logs.append("<span style='color: red;'>[-] Erreur : </span>Pas de connexion au serveur.")
                return
        chemin_fichier = self.chemin.text()

        if not chemin_fichier ou not os.path.isfile(chemin_fichier):
                self.historique_logs.append("<span style='color: red;'>[-] Erreur : </span>Aucun fichier valide sélectionné.")
                return

        try:
                with open(chemin_fichier, 'rb') as f:
                        fichier_nom = os.path.basename(chemin_fichier)
                        self.socket_client.sendall(fichier_nom.encode('utf-8') + b"\n")
                        contenu_fichier = f.read()
                        try:
                                self.socket_client.sendall(contenu_fichier)
                                self.socket_client.sendall(b"\0")
                        except Exception as e:
                                print(f"Erreur lors de l'envoi du fichier : {e}")
                                return

                fichier_nom = os.path.basename(chemin_fichier)
                self.historique_logs.append(f"<span style='color: green;'>[+]</span> Fichier '{fichier_nom}' envoyé avec succès.")
                self.chemin.clear()

        except Exception as e:
                self.historique_logs.append(f"<span style='color: red;'>Erreur</span> : lors de l'envoi du fichier : {e}")
```

### Réception de Données 📥

La réception des données est gérée par la méthode `recevoir_donnees` dans `CLIENT-GUI/index.py` :

```py
def recevoir_donnees(self):
        while self.est_connecte:
                try:
                        donnees = self.socket_client.recv(4096).decode('utf-8')
                        if donnees:
                                nom_fichier, contenu_fichier = donnees.split('|||', 1)
                                self.afficher_message(nom_fichier, contenu_fichier)
                        else:
                                break
                except Exception as e:
                        print(f"Erreur de réception : {e}")
                        break
```

### Affichage des Résultats 📄

L'affichage des résultats est géré par la méthode `afficher_message` dans `CLIENT-GUI/index.py` :

```py
def afficher_message(self, nom_fichier, contenu_fichier):
        extention = os.path.splitext(nom_fichier)[1]

        prompt = ""
        if extention == ".py":
                prompt = f"<span style='color: blue;'>╔═[</span>user@client:~/workspace]<br><span style='color: blue;'>╚═══> $</span> {nom_fichier}"
        elif extention == ".c":
                prompt = f"<span style='color: green;'>╔═[</span>user@client:~/workspace]<br><span style='color: green;'>╚═══> $</span> {nom_fichier}"
        elif extention == ".cpp":
                prompt = f"<span style='color: orange;'>╔═[</span>user@client:~/workspace]<br><span style='color: orange;'>╚═══> $</span> {nom_fichier}"
        elif extention == ".java":
                prompt = f"<span style='color: red;'>╔═[</span>user@client:~/workspace]<br><span style='color: red;'>╚═══> $</span> {nom_fichier}"

        self.fichiers_recus.append(prompt)
        self.fichiers_recus.append(contenu_fichier)
        self.historique_logs.append(f"<span style='color: green;'>[+]</span> Fichier '{nom_fichier}' reçu avec succès : {nom_fichier}")
```

---

## Serveur Maître 🖥️

### Gestion des Clients 👥

La gestion des clients est gérée par la méthode `gestion_client` dans `SERVER-FILE/server-maitre/server.py` :

```py
def gestion_client(self, socket_client, adresse_client):
        id_client = threading.get_ident()
        self.clients[id_client] = socket_client 
        print(f"[+] Client {adresse_client} connecté avec ID {id_client}.")

        try:
                while True:
                        nom_fichier = socket_client.recv(1024).decode('utf-8').strip()
                        if not nom_fichier:
                                break

                        contenu_fichier = b""
                        while True:
                                donnees = socket_client.recv(1024)
                                if not donnees:
                                        break
                                contenu_fichier += donnees
                                if b"\x00" in donnees:
                                        break

                        if contenu_fichier.endswith(b'\x00'):
                                contenu_fichier = contenu_fichier[:-1]

                        contenu_fichier_str = contenu_fichier.decode('utf-8', errors='replace')

                        fichier_info = [id_client, nom_fichier, contenu_fichier_str]
                        print(f"[Client-{id_client}] Liste créée : {fichier_info}")

                        self.choix_esclave(fichier_info)

        except Exception as e:
                print(f"[-] Erreur avec le client-{id_client}: {e}")
        finally:
                del self.clients[id_client]
                socket_client.close()
                print(f"[-] Client {id_client} déconnecté.")
```

### Répartition des Charges ⚖️

La répartition des charges est gérée par la méthode `choix_esclave` dans `SERVER-FILE/server-maitre/server.py` :

```py
def choix_esclave(self, fichier_info):
        # Logique de répartition des charges basée sur le type de fichier et l'utilisation de la RAM
        pass 
```

---

## Serveurs Esclaves 🛠️

Les serveurs esclaves sont responsables de l'exécution des fichiers reçus du serveur maître. Chaque serveur esclave est isolé dans un conteneur Docker pour des raisons de sécurité et de gestion des ressources.

---

## Sécurité 🔒

- Les serveurs esclaves sont isolés dans des conteneurs Docker pour éviter tout accès non autorisé à la machine hôte.

---

