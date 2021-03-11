import threading
import Server.Server
import ServiceToServer.Service
import ServiceHardware.Worker
if __name__ == '__main__':
    thread1 = threading.Thread(target=Server.Server.exec)
    thread2 = threading.Thread(target=ServiceToServer.Service.exec)
    thread3 = threading.Thread(target=ServiceHardware.Worker.exec)
    thread1.start()
    thread2.start()
    thread3.start()
