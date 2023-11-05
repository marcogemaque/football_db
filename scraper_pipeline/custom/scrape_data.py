from .scripts.loader.initial_loader import load_credentials
from os import listdir

@custom
def test_stuff():
    print(listdir("./scripts/"))