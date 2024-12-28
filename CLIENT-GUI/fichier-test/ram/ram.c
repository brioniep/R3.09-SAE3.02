#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    size_t size = 800 * 1024 * 1024;
    char *buffer = malloc(size);
    if (buffer == NULL) {
        return 1;
    }

    for (size_t i = 0; i < size; i++) {
        buffer[i] = ' ';
    }

    sleep(120);

    free(buffer);
    return 0;
}
