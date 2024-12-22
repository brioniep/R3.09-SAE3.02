# PROJET SAE-3.02 : Conception et Développement d’une Architecture Multi-Serveurs pour Compilation et Exécution de Programmes

## Présentation du projet

Ce projet permet d'envoyer à un serveur maître des fichiers de type C, C++, Java et Python depuis un client avec une interface graphique. Une fois les fichiers envoyés, le serveur maître répartit les charges vers différents serveurs esclaves pour qu'ils les exécutent et renvoient le résultat de l'exécution. Les serveurs esclaves sont dans des conteneurs Docker pour mieux les gérer et sécuriser la machine hôte.

Ce dépôt contient deux dossiers principaux : un pour le client et un pour le serveur. Il y a également deux branches dans ce dépôt :
- Une branche pour la ressource qui a permis d'avoir une première approche de socket et thread. [branche R3.09](https://github.com/brioniep/R3.09-SAE3.02/tree/R3.09)
- Une deuxième branche qui montre l'avancement de ce projet. [branche SAE3.02](https://github.com/brioniep/R3.09-SAE3.02/tree/SAE3.02)
- Voici une vidéo de démonstration du projet
(mettre la vidéo de 3 min en mettant l'accent sur la répartition de charge)


## Structure du README

Ce README est divisé en trois grandes parties :

1. [Documentation d'installation](#documentation-dinstallation)
2. [Documentation Utilisateur](#documentation-utilisateur)
3. [Documentation Programmeur](#documentation-programmeur)


# Documentation d'installation

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

## Lancement des serveurs 🚀

Pour lancer les serveurs esclaves, utilisez la commande suivante dans le répertoire `SERVER-FILE` :
```bash
docker-compose up
```

Pour lancer le serveur maître, naviguez vers le répertoire approprié et exécutez la commande suivante :
```bash
cd /chemin/vers/SERVER-FILE/server-maitre
```
```bash
python3 server.py
```

## Lancement du client

Pour lancer l'application client, naviguez vers le répertoire `CLIENT-GUI` et exécutez la commande suivante :
```bash
cd /chemin/vers/CLIENT-GUI
```
```bash
python3 index.py
```
## Lancement du client
Pour lancer l'application client, suivez les étapes ci-dessous :

1. Naviguez vers le répertoire `CLIENT-GUI` :
    ```bash
    cd /chemin/vers/CLIENT-GUI
    ```
2. Exécutez la commande suivante pour démarrer l'application client :
    ```bash
    python3 index.py
    ```


# Documentation Utilisateur
# Documentation du Client

## Introduction
Cette application client permet de se connecter à un serveur maître, d'envoyer des fichiers pour traitement et de recevoir les résultats. Elle est conçue pour être simple à utiliser et offre une interface graphique conviviale.


### Options de l'Application

- **Connexion au Serveur** : Vous devez d'abord vous connecter au serveur maître en entrant l'adresse IP et le port du serveur, puis en cliquant sur le bouton de connexion.
- **Envoi de Fichiers** : Une fois connecté au serveur maître, vous pouvez sélectionner un fichier sur votre ordinateur et l'envoyer au serveur pour traitement.
- **Réception des Résultats** : Les résultats du traitement des fichiers seront affichés dans l'historique des logs.
- **Déconnexion** : Vous pouvez vous déconnecter du serveur maître à tout moment en cliquant sur le bouton de déconnexion.

Note : Tant que vous n'êtes pas connecté au serveur maître, vous ne pouvez pas envoyer de fichiers.

## Fonctionnement des Serveurs
- **Serveur Maître** : Gère les connexions des clients et distribue les tâches aux serveurs esclaves.
- **Serveurs Esclaves** : Reçoivent les fichiers du serveur maître, les traitent et renvoient les résultats.

Cette application permet une interaction fluide avec le serveur maître et les serveurs esclaves pour le traitement de fichiers, offrant une expérience utilisateur simple et efficace.




# Documentation Programmeur