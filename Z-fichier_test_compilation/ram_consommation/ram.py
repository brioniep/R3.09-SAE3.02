import time

def allocate_memory():
    memory = [bytearray(1024 * 1024) for _ in range(600)]  # Allocate 600MB
    print("Consumed 600MB of memory")
    time.sleep(60)  # Sleep for 1 minute

if __name__ == "__main__":
    allocate_memory()
