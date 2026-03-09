# Step 1: Upload CSV file directly
from google.colab import files
import pandas as pd
import random

uploaded = files.upload()  # This will prompt you to select your CSV file

# Get the filename
file_name = list(uploaded.keys())[0]

# Load the CSV
data = pd.read_csv(file_name)
print("Dataset Loaded Successfully:\n")
print(data.head(), "\n")

# -----------------------------
# Step 2: Greedy Test Prioritization
# -----------------------------
def greedy_prioritization(data):
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
    
    # Calculate APFD
    fault_detection_position = []
    for fault in coverage.columns:
        for index,test in enumerate(selected_order):
            if coverage.iloc[test][fault] == 1:
                fault_detection_position.append(index+1)
                break
    
    n = len(test_cases)
    m = len(coverage.columns)
    apfd = 1 - (sum(fault_detection_position)/(n*m)) + (1/(2*n))
    
    return [test_cases[i] for i in selected_order], round(apfd,3)

# -----------------------------
# Step 3: Random Test Prioritization
# -----------------------------
def random_prioritization(data):
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
    
    return [test_cases[i] for i in random_order], round(apfd,3)

# -----------------------------
# Step 4: Run Both Algorithms
# -----------------------------
greedy_order, greedy_apfd = greedy_prioritization(data)
random_order, random_apfd = random_prioritization(data)

# -----------------------------
# Step 5: Print Comparison Table
# -----------------------------
print("======= Test Case Prioritization Comparison =======\n")
print(f"{'Algorithm':<10} | {'Test Order':<30} | {'APFD Score'}")
print("-"*65)
print(f"{'Greedy':<10} | {str(greedy_order):<30} | {greedy_apfd}")
print(f"{'Random':<10} | {str(random_order):<30} | {random_apfd}")
