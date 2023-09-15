import os
import time
from sys import platform

import pyperclip
from googletrans import Translator
from PyDictionary import PyDictionary


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
    main("en")