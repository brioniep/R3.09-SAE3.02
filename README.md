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
- [Lancement des serveurs 🚀](#lancement-des-serveurs-)
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
> ⚠️ **Avertissement** : cette commande peut mettre quelques minutes à s'exécuter dû à l'installation de 16 paquets.


## Lancement des serveurs 🚀

Pour lancer les serveurs esclaves, utilisez la commande suivante dans le répertoire `SERVER-FILE` :
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
python3 index.py
```


# Documentation Utilisateur

## 

### Table des matières

- [Introduction](#introduction)
- [Options de l'Application](#options-de-lapplication)


## Introduction
Cette application client permet de se connecter à un serveur maître, d'envoyer des fichiers pour traitement et de recevoir les résultats. Elle est conçue pour être simple à utiliser et offre une interface graphique conviviale.
Dans cette documentation utilisateur vous aurez une explication simple du projet, de ses fonctionnalités et fonctionnement. Si vous souhaitez avoir une analyse plus poussée du projet, je vous invite à vous rendre sur la [documentation développeur](#documentation-Développeur).


## Options de l'Application

- **Sécurité** : L'accès a la page pour envoyer des fichiers aux servers ne s'ouvre qu'après s'etre authentifier.

- **Surveillance** : L'application est doté d'une partie de log pour permettre a l'utilisateur de controler ses actions dans l'application, savoir si la connexion avec le server maitre est établie, si la connexion est rompue a n'importe quel moment, savoir si son fichier a bien été envoyé etc...

- **Connexion au serveur** : L'application dispose d'une connexion renforcé avec le serveur permetant de vérifier la connexion avec le server maitre toutes les 5 secondes. Si la connexion est rompue un message d'erreur s'afficheras dans les logs.

- **Transfert de fichier** : Cette fonctionnalité ne s'active que quand la connexion est établie avec le server maitre. Si l'utilisateur selectionn eun fichier autre que c, c++, java ou python, alors un message s'affiche en indiquant que le fichier n'est pas conforme.

- **Affichage résultat** : Une fois le résultat reçus il s'afficheras dans la partie droite de l'application avec le nom du fichier ainsi que le résultat d'execution. Un résultat s'afficheras toujours meme en cas d'erreur dans le code afin de permettre a l'utilisateur de corrigé son code.

## Option des serveur maitre / esclaves

- **Identification client** : Dès qu'une connexion est établie avec un client, le serveur maitre lui attribue immédiatement un identifiant unique permetant une meilleur tracabilité des fichiers. Ce qui permet donc de renvoyer le résultat d'un fichier de manière rapide et fiable.

- **Répartition des charges** : Le server maiter est chargé de répartir les fichiers vers les 4 servers esclaves, a savoir que chaques esclave a la capacité de compiler et executer les 4 languages pour permettre une meilleur disponibilité. Le server maitre répartie la charge en deux temp : 

    1. Premièrement il vérifie le type de fichier. Si c'est un fichier python il va priorisé l'envoie vers le server 1, sinon si le fichier est un fichier c alors il va priorisé l'envoie vers le server 2 etc... Voici les priorités de language des servers esclaves : 
        - Server-esclave-1 : Fichier Python
        - Server-esclave-2 : Fichier C
        - Server-esclave-3 : Fichier C++
        - Server-esclave-4 : Fichier Java

    2. Deuxièmement il vérifie la ram en temp réel des conteneurs. C'est a dire que le server maitre va regarder le type de fichier, si c'est un fichier python il va regarder la ram du conteneur esclave 1, si elle dépasse 60% alors il regarde si le conteneur esclave 2 ne dépasse pas les 60% de ram et ainsi de suite. Si tout les conteneurs esclaves sont tous surcharger alors il envoie le fichier par la priorité de language.

    Cette méthode permet de répartir efficacement les charges en deux temps permettant de répartir une première fois de manière générale par le type de fichier puis de manière plus précise avec la ram permetant aux serveurs surcharger de ne pas l'etre d'avantage.

- **Multie taches** : Le serveur maitre se décompose en deux partie, une partie qui reçoit les fichiers des clients et qui les envoies aux servers selon la répartission de charge détailler ci-dessus. Puis une deuxième partie qui va receptionner les fichiers executer des servers et les renvoyer aux clients. Les serveurs esclaves peuvent eux aussi executer et renvoyer des fichiers en simultanés.



# Documentation Développeur

