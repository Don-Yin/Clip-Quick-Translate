import os
import time
from sys import platform

import pyperclip
from googletrans import Translator
from PyDictionary import PyDictionary

# https://stackoverflow.com/questions/71471811/how-to-make-python-code-executable-and-how-to-read-the-exe-file-directory-insid

# https://stackoverflow.com/questions/15921203/how-to-create-a-system-tray-popup-message-with-python-windows

translator = Translator()
dictionary = PyDictionary()

class Record:
    def __init__(self):
        self.content = pyperclip.paste()

    def refresh(self):
        self.content = pyperclip.paste()

    def check_change(self):
        return self.content != pyperclip.paste()

def notify(title, text):
    match platform:
        case "linux":
            os.system(f"notify-send '{title}' '{text}'")
        case "win32":
            os.system(f"powershell.exe -Command Add-Type –AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show('{text}', '{title}')")
        case "darwin":
            os.system("""osascript -e 'display notification "{}" with title "{}"'""".format(text, title))
        case _:
            raise ValueError("Unsupported platform")


def main(target_language: str = "zh-cn"):
    title: str = translator.translate("Translation", dest=target_language).text
    record = Record()
    while True:
        time.sleep(0.5)
        if record.check_change():
            if len(pyperclip.paste()) == 1:
                content = pyperclip.paste().replace(",", "")
                translation = translator.translate(content, dest=target_language).text
                meaning = str(dictionary.meaning(content)).replace("'", "")
                meaning = translator.translate(meaning, dest=translator.detect(content).lang).text
                notify(title, "\n".join([translation, meaning]))
            else:
                content = pyperclip.paste().replace(",", "")
                translation = translator.translate(content, dest=target_language).text
                notify(title, translation)
            record.refresh()


if __name__ == "__main__":
    main()



# euro 4.300,00 - per cauzione E. 3.150,00 + primo mese di affitto E.1.150 – da versare presso l’iban IT42X0326801602052834381820, codice SWIFT/BIC SELBIT2BXXX, intestato ai Locatori;

# euro 1.610,00 – compenso agenzia da versare presso l’iban IT26B0103036141000001191784 – bic PASCITM1JES – intestato a Gregolin Consuelo – Centro Affitti.

# 如果1号前成功换了房子
# 我：2430 + 你：3480（我比五五开少付575 之后2个月内补给你）
# 如果不行。。。
# 我：1380 + 你：4530（我比五五开少付1725 之后4个月内补给你）
