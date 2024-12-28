import time

def consume_memory():
    large_list = []
    while True:
        large_list.append(' ' * 10**6)
        if len(large_list) * 10**6 >= 800 * 10**6:
            break

    time.sleep(120)

if __name__ == "__main__":
    consume_memory()
