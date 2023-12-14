#install_module.py

import subprocess

def install_module(module_name):
    try:
        subprocess.run(["pip", "install", module_name], check=True)
        print(f"Das Modul {module_name} wurde erfolgreich installiert.")
    except subprocess.CalledProcessError as e:
        print(f"Fehler beim Installieren des Moduls {module_name}: {e}")

if __name__ == "__main__":

    module_name = ["numpy","discord","asyncio","configparser","logNow","discord-py-interactions"]

    for modul in module_name:
        install_module(modul)
