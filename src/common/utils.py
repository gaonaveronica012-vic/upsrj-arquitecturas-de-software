import os, json

def load_item(file):
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_item(file, item):
    with open(file, "w") as f:
        json.dump(item, f, indent=4)

def get_host(url: str):
    # Retorna solo el puerto de la URL
    return int(url.split(":")[-1])

