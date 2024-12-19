FROM python:3.9-slim

# Définir le répertoire de travail
WORKDIR /app

# Installer les dépendances nécessaires pour c / c++ et java
RUN apt-get update && apt-get install -y \
    gcc g++ openjdk-17-jdk && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Créer les répertoires nécessaires dans le conteneur
RUN mkdir -p /app/file-attente /app/liste-envoie

# Copie le fichier du serveur dans le conteneur
COPY server.py .

# Changer les permissions pour permettre l'écriture
RUN chmod -R 777 /app/file-attente /app/liste-envoie

# Dès que le conteneur est lancé, cette commande s'execute
CMD ["python3", "server.py"]
