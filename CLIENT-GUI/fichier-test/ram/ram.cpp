#include <iostream>
#include <vector>
#include <chrono>
#include <thread>

int main() {
    size_t size = 800 * 1024 * 1024;
    std::vector<char> buffer(size, ' ');

    std::this_thread::sleep_for(std::chrono::minutes(2));

    return 0;
}
