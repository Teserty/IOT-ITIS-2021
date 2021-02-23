import threading
from Server import Server as server
from ServiceToServer import Service as service
from ServiceHardware import Worker as worker
if __name__ == '__main__':
    thread1 = threading.Thread(target=server.exec)
    thread2 = threading.Thread(target=service.exec)
    thread3 = threading.Thread(target=worker.exec)
    thread1.start()
    thread2.start()
    thread3.start()
