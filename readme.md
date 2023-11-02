# Link Extractor and eMule Sender

This is a simple Python application that allows you to extract links from a specified URL and send those links to the eMule application on a Windows system. The application uses PyQt5 for the graphical user interface and PyInstaller for creating an executable file.

## How It Works

1. **Link Extraction**: The application extracts links from the specified URL when you click the "Extract and Send to eMule" button. It checks for valid URL format, and if valid, it scrapes the webpage for links following the format `http://lamansion-crg.net/forum`.

2. **eMule Integration**: If eMule is installed on the system, the application will check if it's already running. If not, it will open eMule. Then, it will send the extracted links to eMule, allowing you to download the content.

3. **Link List**: The extracted links are displayed in the list on the application's interface. This list eliminates duplicates and sorts the links from smallest to largest.

## Prerequisites

- Python 3.x
- PyQt5
- PyInstaller (for generating the executable)

## Installation

1. Clone the repository to your local machine.
2. Install the required packages using `pip install -r requirements.txt`.
3. Run the application using `python main.py`.
4. To generate an executable file, run `pyinstaller --onefile main.py`.
5. The executable file will be located in the `dist` folder.

## Usage

1. Enter a valid URL in the text box.
2. Click the "Extract and Send to eMule" button.
3. The extracted links will be displayed in the list.
4. If eMule is not running, it will be opened automatically.
5. The links will be sent to eMule.
6. You can now download the content using eMule.