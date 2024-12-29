# PROJET SAE-3.02 : Conception et Développement d’une Architecture Multi-Serveurs pour Compilation et Exécution de Programmes

## Présentation du projet

Ce projet permet d'envoyer à un serveur maître des fichiers de type C, C++, Java et Python depuis un client avec une interface graphique. Une fois les fichiers envoyés, le serveur maître répartit les charges vers différents serveurs esclaves pour qu'ils les exécutent et renvoient le résultat de l'exécution. Les serveurs esclaves sont dans des conteneurs Docker pour mieux les gérer et sécuriser la machine hôte.

Ce dépôt contient deux dossiers principaux : un pour le client et un pour le serveur. Il y a également deux branches dans ce dépôt :
- Une branche pour la ressource qui a permis d'avoir une première approche de socket et thread. [branche R3.09](https://github.com/brioniep/R3.09-SAE3.02/tree/R3.09)
- Une deuxième branche qui montre l'avancement de ce projet. [branche SAE3.02](https://github.com/brioniep/R3.09-SAE3.02/tree/SAE3.02)
- Voici une vidéo de démonstration du projet
(mettre la vidéo de 3 min en mettant l'accent sur la répartition de charge)




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
sudo python3 server.py
```
> ⚠️ **Avertissement** : Il est impératif de lancer le serveur maître en tant qu'administrateur car il utilise la commande `docker stats`, qui n'est disponible qu'avec les privilèges administratifs.

## Lancement du client
Pour lancer l'application client, utilisez la commande suivante adns le répertoire  `CLIENT-GUI` :
```bash
python3 connexion.py
```

> **Note** : Le nom d'utilisateur par défaut est "toto" et le mot de passe par défaut est également "toto". Si vous avez besoin de changer ces identifiants, veuillez consulter la documentation développeur.














