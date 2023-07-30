import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QPlainTextEdit, QFileDialog
from PyQt5.QtCore import Qt
import requests
from bs4 import BeautifulSoup

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Href Extractor')

        # layout
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # widgets
        self.url_input = QPlainTextEdit()
        self.paste_button = QPushButton('Paste from Clipboard')
        self.directory_output = QPushButton('Select Output Directory')
        self.extract_button = QPushButton('Extract href values')

        # adding widgets to layout
        vbox.addWidget(self.url_input)
        vbox.addWidget(self.paste_button)
        vbox.addWidget(self.directory_output)
        vbox.addWidget(self.extract_button)

        # event handlers
        self.paste_button.clicked.connect(self.paste_from_clipboard)
        self.directory_output.clicked.connect(self.select_output_directory)
        self.extract_button.clicked.connect(self.extract_href_values)

        self.show()

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        self.url_input.setPlainText(clipboard.text())

    def select_output_directory(self):
        self.directory_path = QFileDialog.getExistingDirectory(self, 'Select Output Directory')

    def extract_href_values(self):
        url = self.url_input.toPlainText()
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        div_tags = soup.find_all('div', {'align': 'center'})

        href_values = []

        for tag in div_tags:
            a_tags = tag.find_all('a')
            for a_tag in a_tags:
                href_value = a_tag.get('href')
                if href_value.startswith("ed2k"):
                    href_values.append(href_value)

        # Use the directory_path and append the file name
        with open(f"{self.directory_path}/output.txt", 'w') as f:
            for href in href_values:
                f.write(href + '\n')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())
