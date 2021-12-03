from json import load

def load_cfg():
    with open('config.json') as f:
        return load(f)
