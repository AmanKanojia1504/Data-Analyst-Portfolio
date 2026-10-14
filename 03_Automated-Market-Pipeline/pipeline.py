import os
import pandas as pd
from datetime import datetime
from sqlalchemy import create_engine, text

# 1. Extraction Phase (Bypassing proxy restrictions with local mock API stream)
def fetch_market_data():
    print("[1/3] EXTRACTION: Running local data stream fallback...")
    
    # Static structured dataset payload matching real API output structures
    mock_api_payload = {
        'rates': {
            'INR': 84.12,
            'EUR': 0.92,
            'GBP': 0.77,
            'JPY': 152.45
        }
    }
    
    raw_rates = mock_api_payload['rates']
    target_assets = {
        'INR': raw_rates.get('INR'),
        'EUR': raw_rates.get('EUR'),
        'GBP': raw_rates.get('GBP'),
        'JPY': raw_rates.get('JPY')
    }
    return target_assets

# 2. Transformation Phase (Data Wrangling with Pandas)
def transform_data(raw_records):
    print(" [2/3] TRANSFORMATION: Processing quality data rules via Pandas structural edits...")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Parse payload structure cleanly into an engineering matrix
    processed_df = pd.DataFrame(list(raw_records.items()), columns=['asset_ticker', 'exchange_rate'])
    processed_df['last_updated'] = timestamp
    processed_df['base_currency'] = 'USD'
    
    # QA Check constraint parameter
    processed_df.dropna(subset=['exchange_rate'], inplace=True)
    return processed_df

# 3. Loading Phase (Atomic Database Ingestion and Schema Merging)
def load_to_database(df):
    print("[3/3] LOADING: Initiating local PostgreSQL connection...")
    
    # ⚠️ MASTER UPDATE REQUIREMENT: Change '8530807373' to your actual PostgreSQL password below
    DATABASE_URL = "postgresql://postgres:8530807373@localhost:5432/market_db"
    engine = create_engine(DATABASE_URL)
    
    # Step A: Assert and build database schema structure states
    with engine.connect() as conn:
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS asset_pricing (
                asset_ticker VARCHAR(10) PRIMARY KEY,
                exchange_rate DECIMAL(12, 4),
                base_currency VARCHAR(5),
                last_updated TIMESTAMP
            );
        """))
        conn.commit()

    # Step B: Write rows atomically to an isolated staging area table
    df.to_sql('temp_staging_table', engine, if_exists='replace', index=False)
    
    # Step C: Complete robust structural upsert validation transaction
    upsert_query = """
        INSERT INTO asset_pricing (asset_ticker, exchange_rate, base_currency, last_updated)
        SELECT asset_ticker, exchange_rate, base_currency, CAST(last_updated AS TIMESTAMP) FROM temp_staging_table
        ON CONFLICT (asset_ticker) 
        DO UPDATE SET 
            exchange_rate = EXCLUDED.exchange_rate,
            last_updated = EXCLUDED.last_updated;
    """
    
    with engine.connect() as conn:
        conn.execute(text(upsert_query))
        conn.execute(text("DROP TABLE IF EXISTS temp_staging_table;"))
        conn.commit()
    print("PIPELINE EXECUTION SUCCESSFUL: Local 'market_db' metrics synced completely.")

if __name__ == "__main__":
    try:
        raw_metrics = fetch_market_data()
        cleaned_dataframe = transform_data(raw_metrics)
        load_to_database(cleaned_dataframe)
    except Exception as pipeline_error:
        print(f"❌ CRITICAL PIPELINE FAILURE: {pipeline_error}")