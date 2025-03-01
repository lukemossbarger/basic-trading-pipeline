import argparse
from model import Model

if __name__ == "__main__":
    tick_size = 60
    model = Model()
    model.run(tick_size)
