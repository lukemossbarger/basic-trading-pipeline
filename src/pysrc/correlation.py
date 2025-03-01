import numpy as np

predict = []
actual = []
with open("test.txt", "r") as file:
    for line in file:
        p_val, a_val = map(float, line.strip().split(","))
        predict.append(p_val)
        actual.append(a_val)

predict_arr = np.array(predict)
actual_arr = np.array(actual)

correlation = np.corrcoef(predict_arr, actual_arr)[0, 1]
