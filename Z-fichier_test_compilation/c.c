#include <stdio.h>
#include <stdlib.h>

int main() {
    printf("Début du programme. Allocation massive de mémoire...\n");

    // Tableau de pointeurs pour allouer de la mémoire
    char *memory_blocks[1000000];  // Tableau pour 1 million de pointeurs
    int i;

    // Allouer 100 Ko pour chaque bloc de mémoire
    for (i = 0; i < 1000000; i++) {
        memory_blocks[i] = (char *)malloc(1024 * 100); // 100 Ko par bloc
        if (memory_blocks[i] == NULL) {
            printf("Erreur d'allocation mémoire à l'index %d\n", i);
            return 1;
        }
    }

    printf("Mémoire allouée. Appuyez sur Ctrl+C pour terminer...\n");

    // Attendre indéfiniment pour observer l'utilisation de la mémoire
    while (1) {
        // La boucle ne fait rien, mais elle permet de maintenir le programme en cours d'exécution
    }

    // Libérer la mémoire (ce qui ne se produit jamais en raison de la boucle infinie)
    for (i = 0; i < 1000000; i++) {
        free(memory_blocks[i]);
    }

    return 0;
}

