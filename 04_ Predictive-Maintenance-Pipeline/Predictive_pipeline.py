import time
import random
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text

# 1. Extraction Phase: Simulating live IoT factory machine sensors
def simulate_sensor_stream():
    print("Reading real-time machine telemetry streams...")
    
    # Establish standard safe baseline operating metrics
    base_temperature = 65.0
    base_vibration = 2.1
    base_rpm = 1500.0
    
    # Introduce random environmental fluctuations
    temperature = base_temperature + random.uniform(-2.5, 2.5)
    vibration = base_vibration + random.uniform(-0.3, 0.3)
    rpm = base_rpm + random.uniform(-50.0, 50.0)
    
    # Mathematical anomaly trigger: 15% chance to inject an operational spike (simulating machine friction)
    anomaly_trigger = random.random()
    if anomaly_trigger > 0.85:
        print("ALERT: Temporary thermal and mechanical anomaly injected into stream.")
        temperature += random.uniform(15.0, 25.0)
        vibration += random.uniform(1.5, 2.5)
        rpm -= random.uniform(200.0, 400.0)
        
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Package parameters into a structured record format
    telemetry_record = {
        'machine_id': 'MC_001',
        'timestamp': current_time,
        'temperature_celsius': round(temperature, 2),
        'vibration_mm_s': round(vibration, 2),
        'rpm_speed': round(rpm, 2)
    }
    return telemetry_record

# 2. Transformation Phase: Pandas structured formatting
def process_telemetry_batch(record):
    print("Formatting structural telemetry parameters using Pandas...")
    df = pd.DataFrame([record])
    
    # Data Quality Validation Gates
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df['machine_id'] = df['machine_id'].astype(str)
    return df

# 3. Loading Phase: Relational database table creation and streaming ingestion
def stream_to_database(df):
    print("Ingesting structured telemetry rows into relational data layers...")
    
    # CONFIGURATION: Update 'yourpassword' below to your actual PostgreSQL password
    DATABASE_URL = "postgresql://postgres:8530807373@localhost:5432/market_db"
    engine = create_engine(DATABASE_URL)
    
    # Enforce underlying destination schema table structures if missing
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS factory_telemetry (
                record_id SERIAL PRIMARY KEY,
                machine_id VARCHAR(20),
                timestamp TIMESTAMP,
                temperature_celsius DECIMAL(6, 2),
                vibration_mm_s DECIMAL(5, 2),
                rpm_speed DECIMAL(7, 2)
            );
        """))
        conn.commit()
        
    # Append the stream records seamlessly into your database
    df.to_sql('factory_telemetry', engine, if_exists='append', index=False)
    print("Database data sync loop cycle finalized successfully.")

if __name__ == "__main__":
    try:
        # Simulate running a continuous streaming cycle loop for data gathering
        print("Starting active predictive maintenance operational pipeline setup...")
        simulated_record = simulate_sensor_stream()
        processed_data = process_telemetry_batch(simulated_record)
        stream_to_database(processed_data)
    except Exception as error:
        print(f"Critical execution breakdown encountered: {error}")