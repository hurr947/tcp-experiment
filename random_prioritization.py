import pandas as pd
import random

data = pd.read_csv("test_dataset.csv")

test_cases = list(data.iloc[:,0])
coverage = data.iloc[:,1:]

random_order = list(range(len(test_cases)))
random.shuffle(random_order)

fault_detection_position = []

for fault in coverage.columns:
    for index,test in enumerate(random_order):
        if coverage.iloc[test][fault] == 1:
            fault_detection_position.append(index+1)
            break

n = len(test_cases)
m = len(coverage.columns)

apfd = 1 - (sum(fault_detection_position)/(n*m)) + (1/(2*n))

print("Random Test Order:", [test_cases[i] for i in random_order])
print("Random APFD Score:", round(apfd,3))
