import subprocess
import sys
import os
import time
from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QPlainTextEdit,
    QMessageBox,
    QLabel,
)
from PyQt5.QtCore import QThread, pyqtSignal
import requests
from bs4 import BeautifulSoup
import psutil


class ExtractLinksThread(QThread):
    progressChanged = pyqtSignal(int)
    finished = pyqtSignal()
    error = pyqtSignal(str)  # Signal to emit error messages

    def __init__(self, link_queue):
        super().__init__()
        self.link_queue = link_queue

    def run(self):
        total_links = len(self.link_queue)
        current_dir = os.getcwd()
        for i, url in enumerate(self.link_queue):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, "html.parser")

                href_values = []

                for a_tag in soup.find_all("a"):
                    href_value = a_tag.get("href")
                    if href_value and href_value.startswith("ed2k"):
                        href_values.append(href_value)

                if not href_values:
                    self.progressChanged.emit(int(((i + 1) / total_links) * 100))
                    continue

                # Remove duplicate links
                href_values = list(set(href_values))

                # Sort the links from smallest to largest
                href_values.sort()

                # Use the current directory and append the file name with a number
                file_name = f"output_{i+1}.txt"
                file_path = os.path.join(current_dir, file_name)

                with open(file_path, "w") as f:
                    for href in href_values:
                        f.write(href + "\n")

                self.progressChanged.emit(int(((i + 1) / total_links) * 100))
            except requests.exceptions.RequestException as e:
                self.error.emit(f"Error accedieno al URL: {url}\n\n{str(e)}")

        self.finished.emit()


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.link_queue = []
        self.extract_thread = None
        # Add the paths where eMule might be installed
        self.emule_paths = [
            "C:\\Program Files\\eMule",
            "D:\\Program Files\\eMule",
            "E:\\Program Files\\eMule",
        ]

    def initUI(self):
        self.setWindowTitle("Extractor Links del CRG")

        # layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # widgets
        self.url_input = QPlainTextEdit()
        self.extract_button = QPushButton("Extraer y guardar links en archivos")
        self.send_emule_button = QPushButton("Enviar links a eMule")
        self.progress_label = QLabel()
        self.progress_bar = QLabel()

        # adding widgets to layout
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.extract_button)
        vbox.addWidget(self.send_emule_button)
        vbox.addWidget(self.progress_label)
        vbox.addWidget(self.progress_bar)

        # event handlers
        self.extract_button.clicked.connect(self.start_extraction)
        self.send_emule_button.clicked.connect(self.send_to_emule)

        self.show()

    def start_extraction(self):
        urls = self.url_input.toPlainText().split(",")
        urls = [url.strip() for url in urls if url.strip()]

        if not urls:
            QMessageBox.warning(self, "Error", "No existen links.")
            return

        self.link_queue = urls

        self.extract_thread = ExtractLinksThread(self.link_queue)
        self.extract_thread.progressChanged.connect(self.update_progress)
        self.extract_thread.finished.connect(self.extraction_finished)
        self.extract_thread.error.connect(self.show_error_message)

        self.extract_thread.start()

        self.extract_button.setEnabled(False)
        self.progress_label.setText("Extrayendo links...")
        self.progress_bar.setText("0%")

    def update_progress(self, progress):
        self.progress_bar.setText(f"{progress}%")

    def extraction_finished(self):
        QMessageBox.information(
            self,
            "Exit",
            "Links se guardaron con exito en los archivos de texto. ",
        )
        self.send_to_emule()  # Add this line to send the links to eMule

        self.link_queue = []
        self.extract_button.setEnabled(True)
        self.progress_label.setText("")
        self.progress_bar.setText("")

    def show_error_message(self, error_message):
        QMessageBox.warning(self, "Error", error_message)

    def send_to_emule(self):
        if not self.link_queue:
            QMessageBox.warning(self, "Error", "No hay links que enviar a Emule")
            return

        for i in range(1, len(self.link_queue) + 1):
            file_name = f"output_{i}.txt"
            if not os.path.exists(file_name):
                QMessageBox.warning(self, "Error", f"File {file_name} does not exist.")
                continue

            with open(file_name, "r") as f:
                for link in f:
                    self.run_emule(link.strip())


    def run_emule(self, link):
     for path in self.emule_paths:
         emule_exe_path = os.path.join(path, "emule.exe")
         if os.path.exists(emule_exe_path):
             # Verificar si eMule ya está en ejecución
             for process in psutil.process_iter(["name"]):
                 if process.name() == "emule.exe":
                     # eMule ya está en ejecución, enviar el enlace directamente
                     try:
                         subprocess.Popen([emule_exe_path, link])
                         return  # Salir del método después de ejecutar eMule
                     except subprocess.CalledProcessError:
                         QMessageBox.warning(
                             self, "Error", f"Error running eMule at {emule_exe_path}"
                         )
                     break
 
             # eMule no está en ejecución, abrir eMule y enviar el enlace
             try:
                 subprocess.Popen([emule_exe_path])  # Abrir eMule
                 time.sleep(7)  # Esperar un tiempo para asegurar que eMule se abra correctamente
                 subprocess.Popen([emule_exe_path, link])
                 return  # Salir del método después de ejecutar eMule
             except subprocess.CalledProcessError:
                 QMessageBox.warning(
                     self, "Error", f"Error running eMule at {emule_exe_path}"
                 )
 
     # Si no se encontró eMule en ninguno de los directorios, mostrar un mensaje de advertencia
     QMessageBox.warning(self, "Error", "eMule not found in any of the specified paths.")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
