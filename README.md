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
    sudo apt-get update
    ```

2. Installez les paquets nécessaires pour permettre à `apt` d'utiliser un dépôt via HTTPS :
    ```bash
    sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
    ```

3. Ajoutez la clé GPG officielle de Docker :
    ```bash
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    ```

4. Ajoutez le dépôt Docker à vos sources APT :
    ```bash
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    ```

5. Mettez à jour la base de données des paquets avec les paquets Docker du dépôt ajouté :
    ```bash
    sudo apt-get update
    ```

6. Installez Docker :
    ```bash
    sudo apt-get install docker-ce
    ```

### Docker Compose 📦
Docker Compose est un outil pour définir et gérer des applications multi-conteneurs Docker. Pour l'installer, exécutez les commandes suivantes :

1. Téléchargez la version stable de Docker Compose :
    ```bash
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    ```

2. Appliquez des permissions d'exécution au binaire :
    ```bash
    sudo chmod +x /usr/local/bin/docker-compose
    ```

### Python et librairies nécessaires 🐍
Pour installer Python et les librairies nécessaires au projet, suivez ces étapes :

1. Installez Python :
    ```bash
    sudo apt-get install python3 python3-pip
    ```

2. Installez les librairies nécessaires :
    ```bash
    pip3 install -r requirements.txt
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
