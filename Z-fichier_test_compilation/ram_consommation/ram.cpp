#include <iostream>
#include <vector>
#include <thread>
#include <chrono>

int main() {
    try {
        std::vector<char> memory(600 * 1024 * 1024); // Allocate 600MB
        std::fill(memory.begin(), memory.end(), 0); // Use the allocated memory
        std::cout << "Consumed 600MB of memory" << std::endl;
        std::this_thread::sleep_for(std::chrono::minutes(1)); // Sleep for 1 minute
    } catch (const std::bad_alloc&) {
        std::cerr << "Memory allocation failed" << std::endl;
        return 1;
    }
    return 0;
}
