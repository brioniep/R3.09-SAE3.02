import threading
import time

def message(thread_id):
    for i in range(5):
        print(f"Je suis la thread {thread_id}")
        time.sleep(1)

t1 = threading.Thread(target=message, args=(1,))
t2 = threading.Thread(target=message, args=(2,))

t1.start()
t2.start()

t1.join() # le join permet d'attendre la fin des thread avant de passer a la suite (pas utile dans cette exercice)
t2.join()


