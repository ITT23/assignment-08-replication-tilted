import os, time
from typing import TypedDict, Callable


class Recogniser:

  CURR_DIR = os.path.dirname(__file__)
  MODEL_PATH = "lstm_model"

  def __init__(self) -> None:
    pass

  def run(self) -> None:
    pass

if __name__ == "__main__":
  recogniser = Recogniser()
  recogniser.run()