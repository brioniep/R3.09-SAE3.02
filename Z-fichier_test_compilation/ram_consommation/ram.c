#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

int main() {
    char *memory = (char *)malloc(600 * 1024 * 1024); // Allocate 600MB
    if (memory == NULL) {
        printf("Memory allocation failed\n");
        return 1;
    }
    memset(memory, 0, 600 * 1024 * 1024); // Use the allocated memory
    printf("Consumed 600MB of memory\n");
    sleep(60); // Sleep for 1 minute
    free(memory); // Free the memory
    return 0;
}
