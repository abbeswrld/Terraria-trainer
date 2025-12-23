import pymem

def find_terraria_process():
    try:
        return pymem.Pymem('Terraria.exe')
    except pymem.exception.ProcessNotFound:
        return None