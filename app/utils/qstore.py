import os
import pickle


def store_object(obj, filename: str = "query.dat"):
    """
    Serialize and store an object to a file in the data directory.
    """
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    filepath = os.path.join(data_dir, filename)
    with open(filepath, "wb") as f:
        pickle.dump(obj, f)


def retrieve_object(filename: str = "query.dat"):
    """
    Load and deserialize an object from a file in the data directory.
    """
    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    filepath = os.path.join(data_dir, filename)

    try:
        with open(filepath, "rb") as f:
            obj = pickle.load(f)
    except FileNotFoundError:
        obj = None
    return obj
