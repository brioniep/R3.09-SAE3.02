# Documentation d'installation

## Table des matières
- [Installation des dépendances](#installation-des-dépendances)
- [Mise en place des fichiers sur le serveur Linux](#mise-en-place-des-fichiers-sur-le-serveur-linux)
- [Construction des conteneurs](#construction-des-conteneurs)
- [Démarrage du client](#démarrage-du-client)

## Installation des dépendances 🚀

### Docker 🐳

Docker est une plateforme permettant de développer, livrer et exécuter des applications dans des conteneurs. Pour installer Docker sur Linux, suivez les étapes suivantes :

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

Téléchargez la version stable de Docker Compose :
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

Pour transférer les fichiers sur le serveur Linux, vous pouvez utiliser FileZilla. Téléchargez FileZilla depuis leur [site officiel](https://filezilla-project.org/).

Assurez-vous que le serveur dispose de SSH pour pouvoir déposer les fichiers. Vous pouvez vérifier cela en essayant de vous connecter via SSH :
```bash
ssh user@server_ip
```

## Construction des conteneurs 🛠️

Pour construire et démarrer les conteneurs, utilisez la commande suivante :
```bash
docker-compose up --build
```

## Démarrage du client 🚀

Pour lancer l'application client, exécutez la commande suivante dans le répertoire du projet :
```bash
python3 client.py
```

