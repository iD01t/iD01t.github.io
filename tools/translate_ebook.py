import sys

def translate_and_update(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    translations = {
        "Anarchie et évolution - L'histoire de la musique punk": "Anarchy and Evolution - The History of Punk Music",
        "Anarchie et évolution : L'histoire de la musique punk": "Anarchy and Evolution: The History of Punk Music"
    }

    for fr_text, en_text in translations.items():
        content = content.replace(fr_text, en_text)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        translate_and_update(filepath)
        print(f"File '{filepath}' updated successfully.")
    else:
        print("Please provide a filepath as an argument.")
