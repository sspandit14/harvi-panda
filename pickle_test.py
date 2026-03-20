import pickle
import numpy as np

with open("mat1_low-med/2026-02-13T16_36_22.030447.pkl", "rb") as f:
    data = pickle.load(f)

print(type(data))
print(data)