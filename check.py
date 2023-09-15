"""
This script checks for available language from google API
"""


from googletrans import LANGUAGES

for lang_code, lang_name in LANGUAGES.items():
    print(f"{lang_code}: {lang_name}")
