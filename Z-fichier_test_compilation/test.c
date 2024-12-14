#include <stdio.h>

#define N 100 // Nombre de Fibonacci à calculer

// Fonction pour calculer les N premiers nombres de Fibonacci
void calcul_fibonacci() {
    unsigned long long fib[N]; // Tableau pour stocker les nombres de Fibonacci
    fib[0] = 0;  // Premier nombre de Fibonacci
    fib[1] = 1;  // Deuxième nombre de Fibonacci

    // Calculer les nombres de Fibonacci suivants
    for (int i = 2; i < N; i++) {
        fib[i] = fib[i - 1] + fib[i - 2];
    }

    // Afficher les résultats
    printf("Les %d premiers nombres de Fibonacci sont :\n", N);
    for (int i = 0; i < N; i++) {
        printf("%llu ", fib[i]);
    }
    printf("\n");
}

int main() {
    calcul_fibonacci();  // Appel de la fonction pour calculer les nombres de Fibonacci
    return 0;  // Fin du programme
}
