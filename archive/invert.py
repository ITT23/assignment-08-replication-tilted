import os
import pandas as pd

SCRIPT_DIR = os.path.dirname(__file__)
ALLTXT_PATH = os.path.join(SCRIPT_DIR, "all.txt")
DATA_PATH = os.path.join(SCRIPT_DIR, "..", "gesture_recognition", "data")

with open(ALLTXT_PATH, "r") as f:
  for file_name in f:
    file_name_new = os.path.join(DATA_PATH, file_name.rstrip("\n"))
    content = pd.read_csv(file_name_new)
    content['accelerometer_x'] *= -1
    content.to_csv(file_name_new, index=False)