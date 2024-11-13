import threading
import time

def compte_a_rebours(n, thread_id):
    for i in range(n, 0, -1):
        print(f"thread {thread_id} : {i}")
        time.sleep(0.5) 

n1 = 5
n2 = 3

thread1 = threading.Thread(target=compte_a_rebours, args=(n1, 1))
thread2 = threading.Thread(target=compte_a_rebours, args=(n2, 2))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print("Fin du programme")
