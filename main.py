from threading import Thread
import subprocess

if __name__ == "__main__":
    components = [
        "python3 sensores.py",
        "python3 camera.py",
        "python3 atuadores.py",
        "python3 gateway.py",
        "python3 servidor_nuvem.py"
    ]

    threads = []
    for command in components:
        thread = Thread(target=lambda: subprocess.run(command, shell=True))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
