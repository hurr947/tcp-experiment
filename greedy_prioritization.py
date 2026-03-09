import pandas as pd

data = pd.read_csv("test_dataset.csv")

test_cases = data.iloc[:,0]
coverage = data.iloc[:,1:]

remaining_faults = set(coverage.columns)
selected_order = []

coverage_matrix = coverage.copy()

while remaining_faults:
    max_detected = -1
    best_test = None
    
    for i,row in coverage_matrix.iterrows():
        detected = sum([1 for f in remaining_faults if row[f]==1])
        
        if detected > max_detected:
            max_detected = detected
            best_test = i
    
    selected_order.append(best_test)
    
    detected_faults = [f for f in remaining_faults if coverage_matrix.loc[best_test,f]==1]
    
    for f in detected_faults:
        remaining_faults.remove(f)

coverage_matrix = coverage_matrix.drop(best_test)

fault_detection_position = []

for fault in coverage.columns:
    for index,test in enumerate(selected_order):
        if coverage.iloc[test][fault] == 1:
            fault_detection_position.append(index+1)
            break

n = len(test_cases)
m = len(coverage.columns)

apfd = 1 - (sum(fault_detection_position)/(n*m)) + (1/(2*n))

print("Greedy Test Order:", [test_cases[i] for i in selected_order])
print("Greedy APFD Score:", round(apfd,3))
