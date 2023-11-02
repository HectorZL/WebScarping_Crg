import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QListWidget, QMessageBox
from link_extractor import LinkExtractor
from emule_handler import EmuleHandler

class LinkExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.link_extractor = LinkExtractor()
        self.emule_handler = EmuleHandler([
            "C:\\Program Files\\eMule",
            "D:\\Program Files\\eMule",
            "E:\\Program Files\\eMule",
        ])
        self.links = set()  # Usar un conjunto para eliminar duplicados
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Extractor de Enlaces")

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        self.url_input = QLineEdit()
        self.extract_button = QPushButton("Extraer y Enviar a eMule")
        self.link_list = QListWidget()

        vbox.addWidget(self.url_input)
        vbox.addWidget(self.extract_button)
        vbox.addWidget(self.link_list)

        self.extract_button.clicked.connect(self.extract_and_send)

    def extract_and_send(self):
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(None, "Error", "El campo de enlace está vacío.")
            return

        if not self.link_extractor.is_valid_url(url):
            QMessageBox.warning(None, "Error", "El enlace no sigue el formato esperado.")
            return

        links = self.link_extractor.extract_links(url)

        if links is not None:
            self.links.update(links)  # Agregar los enlaces al conjunto
            self.update_link_list()

            # Verificar si eMule está instalado y ejecutarlo si no está en ejecución
            self.emule_handler.check_and_send_links(self.links)

        else:
            QMessageBox.warning(None, "Error", "Error accediendo al URL.")

        self.url_input.clear()

    def update_link_list(self):
        self.link_list.clear()
        for link in sorted(self.links):  # Mostrar los enlaces ordenados
            self.link_list.addItem(link)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = LinkExtractorApp()
    ex.show()
    sys.exit(app.exec_())
