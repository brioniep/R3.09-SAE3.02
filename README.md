# PROJET SAE-3.02 : Conception et Développement d’une Architecture Multi-Serveurs pour Compilation et Exécution de Programmes

## Présentation du projet

Ce projet consiste en une application client-serveur utilisant Docker pour la gestion des conteneurs. Le dossier `SERVER-FILE` contient tous les fichiers nécessaires pour le serveur, tandis que le dossier `CLIENT-GUI` contient les fichiers pour l'application client.

## Documentation d'installation

### Table des matières

- [Installation des dépendances 🚀](#installation-des-dépendances-)
- [Mise en place des fichiers sur le serveur Linux 📂](#mise-en-place-des-fichiers-sur-le-serveur-linux-)
- [Construction des conteneurs 🛠️](#construction-des-conteneurs-)

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

Pour construire et démarrer les conteneurs, rendez-vous à la racine du dossier `SERVER-FILE` avec la commande suivante :
```bash
cd /chemin/vers/SERVER-FILE
```

Ensuite, exécutez la commande suivante dans le serveur :
```bash
docker-compose up --build
```

