import csv
import time
import random
import os
from datetime import datetime

NIFI_CONTAINER_NAME = "nifi" 
NIFI_INPUT_DIR = "/opt/nifi/nifi-current/nifi_input_data"
NIFI_OUTPUT_DIR = "/opt/nifi/nifi-current/nifi_output_data"
LOCAL_TMP_IN = "/tmp/nifi_input_data"
LOCAL_TMP_OUT = "/tmp/nifi_output_data"

for d in [LOCAL_TMP_IN, LOCAL_TMP_OUT]:
    if not os.path.exists(d):
        os.makedirs(d)

os.system(f"docker exec {NIFI_CONTAINER_NAME} mkdir -p {NIFI_INPUT_DIR}")
os.system(f"docker exec {NIFI_CONTAINER_NAME} mkdir -p {NIFI_OUTPUT_DIR}")

def generate_and_push_data():
    """توليد بيانات ملوثة وإرسالها إلى NiFi"""
    data_samples = [
        ["101", "Ahmed Mansour", "ahmed@example.com", "2023-01-10"],
        ["102", "Sara Ali", "sara_at_example.com", "15/05/2023"],
        ["103", "Omar Khaled", "", "June 20, 2023"],
        ["101", "Ahmed Mansour", "ahmed@example.com", "2023-01-10"],
        ["ERR_99", "Invalid User", "unknown@mail.com", "2024-02-01"],
        ["", "Missing ID", "id@null.com", "2024-03-01"]
    ]
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transaction_{timestamp}.csv"
    filepath = os.path.join(LOCAL_TMP_IN, filename)
    
    try:
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["CustomerID", "Name", "Email", "JoinDate"])
            rows = random.choices(data_samples, k=random.randint(5, 12))
            writer.writerows(rows)
            
        os.system(f"docker cp {filepath} {NIFI_CONTAINER_NAME}:{NIFI_INPUT_DIR}/")
        print(f"[IN] Data generated and sent to NiFi: {filename}")
    except Exception as e:
        print(f"Error generating data: {e}")

def pull_and_upload_to_hdfs():
    """سحب البيانات النظيفة من NiFi ورفعها إلى HDFS"""
    os.system(f"docker cp {NIFI_CONTAINER_NAME}:{NIFI_OUTPUT_DIR}/. {LOCAL_TMP_OUT}/ > /dev/null 2>&1")
    
    files = os.listdir(LOCAL_TMP_OUT)
    if files:
        print(f"[OUT] Found {len(files)} cleaned files. Uploading to HDFS...")
        os.system(f"hdfs dfs -put -f {LOCAL_TMP_OUT}/* /user/hadoop/nifi_processed/")
        
        os.system(f"rm {LOCAL_TMP_OUT}/*")
        os.system(f"docker exec {NIFI_CONTAINER_NAME} sh -c 'rm -f {NIFI_OUTPUT_DIR}/*'")
        print("Upload to HDFS complete!")

if __name__ == "__main__":
    print("🚀 Starting Data Pipeline Orchestrator...\n")
    while True:
        generate_and_push_data()   
        pull_and_upload_to_hdfs()  
        print("-" * 40)
        time.sleep(5)