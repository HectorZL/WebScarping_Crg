import subprocess
import os
import time
from PyQt5.QtWidgets import QMessageBox
import psutil

class EmuleHandler:
    def __init__(self, emule_paths):
        self.emule_paths = emule_paths

    def check_and_send_links(self, links):
        if not links:
            QMessageBox.warning(None, "Error", "No hay enlaces para enviar a eMule.")
            return

        for path in self.emule_paths:
            emule_exe_path = os.path.join(path, "emule.exe")
            if os.path.exists(emule_exe_path):
                for link in links:
                    try:
                        for process in psutil.process_iter(["name"]):
                            if process.info["name"] == "emule.exe":
                                break
                        else:
                            # eMule no está en ejecución, abrir eMule
                            subprocess.Popen([emule_exe_path])
                            time.sleep(7)  # Esperar un tiempo para asegurar que eMule se abra correctamente

                        subprocess.Popen([emule_exe_path, link])

                    except subprocess.CalledProcessError:
                        QMessageBox.warning(None, "Error", f"Error running eMule at {emule_exe_path}")

                return

        QMessageBox.warning(None, "Error", "eMule no se encontró en ninguno de los directorios especificados.")
