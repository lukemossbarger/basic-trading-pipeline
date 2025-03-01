import numpy as np

predict = []
actual = []
with open("test.txt", "r") as file:
    for line in file:
        p_val, a_val = map(float, line.strip().split(","))
        predict.append(p_val)
        actual.append(a_val)

predict = np.array(predict)
actual = np.array(actual)

correlation = np.corrcoef(predict, actual)[0, 1]
print("Correlation: " + str(correlation))
print("Expected: ")
