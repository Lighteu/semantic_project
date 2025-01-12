import pickle

def save_cache(filename, data):
    with open(filename, "wb") as f:
        pickle.dump(data, f)

def load_cache(filename):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None