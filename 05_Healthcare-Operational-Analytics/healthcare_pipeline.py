import time
import random
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text

# 1. Extraction: Generating simulated live ER and ICU patient triage metric entries
def generate_patient_stream():
    print("Capturing live emergency room and clinical triage data events...")
    
    wards = ['ER', 'ICU', 'General Ward', 'Pediatrics']
    urgency_levels = ['Routine', 'Urgent', 'Emergency']
    statuses = ['Admitted', 'Discharged', 'In-Treatment']
    
    assigned_ward = random.choice(wards)
    urgency = random.choice(urgency_levels)
    status = random.choice(statuses)
    
    # Operational Logic: Emergency cases in the ER/ICU experience longer processing latencies
    if urgency == 'Emergency' or assigned_ward in ['ER', 'ICU']:
        transit_minutes = random.randint(15, 60)
        billing_inr = random.randint(25000, 85000)
    else:
        transit_minutes = random.randint(5, 20)
        billing_inr = random.randint(4500, 18000)
        
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    return {
        'patient_id': f"PT_{random.randint(1000, 9999)}",
        'timestamp': current_time,
        'urgency_level': urgency,
        'assigned_ward': assigned_ward,
        'transit_minutes': transit_minutes,
        'total_billing_inr': billing_inr,
        'operational_status': status
    }

# 2. Transformation: Formatting matrices cleanly with Pandas dataframe wrappers
def transform_clinical_data(record):
    df = pd.DataFrame([record])
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# 3. Loading: Streaming records atomically to local database engines
def stream_to_warehouse(df):
    # CONFIGURATION: Update '853808737' to your true master database password
    DATABASE_URL = "postgresql://postgres:8530807373@localhost:5432/market_db"
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS clinical_operations (
                record_id SERIAL PRIMARY KEY,
                patient_id VARCHAR(20),
                timestamp TIMESTAMP,
                urgency_level VARCHAR(20),
                assigned_ward VARCHAR(50),
                transit_minutes INT,
                total_billing_inr DECIMAL(12, 2),
                operational_status VARCHAR(20)
            );
        """))
        conn.commit()
        
    df.to_sql('clinical_operations', engine, if_exists='append', index=False)
    print("Database sync completed. Clinical records ingested successfully.")

if __name__ == "__main__":
    try:
        print("Initializing Real-Time Healthcare Operational Ingestion Engine...")
        # Simulate continuous operational logging loops
        simulated_patient = generate_patient_stream()
        processed_metrics = transform_clinical_data(simulated_patient)
        stream_to_warehouse(processed_metrics)
    except Exception as error:
        print(f"Operational pipeline execution failure: {error}")