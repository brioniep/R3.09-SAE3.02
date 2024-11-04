def lire_fichier(nom_fichier: str):
    try:
        with open(nom_fichier, 'r') as f:
            for ligne in f:
                ligne = ligne.rstrip("\n\r")
                print(ligne)
    except FileNotFoundError:
        print("Erreur : Le fichier spécifié est introuvable.")
    except IOError:
        print("Erreur : Une erreur d'entrée/sortie s'est produite.")
    except FileExistsError:
        print("Erreur : Le fichier existe déjà.")
    except PermissionError:
        print("Erreur : Vous n'avez pas la permission d'accéder à ce fichier.")



        
nom_fichier = "test.txt"
lire_fichier(nom_fichier)


