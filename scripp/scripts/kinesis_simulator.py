#!/usr/bin/env python3
"""
Kinesis Event Simulator – LKS Cloud Computing 2026
Kirim 1000 event ke Kinesis Data Stream: kds-nusashop-events-2026

Cara pakai:
  pip install boto3 faker
  python3 kinesis_simulator.py --stream kds-nusashop-events-2026 --count 1000 --region us-east-1
"""

import boto3
import json
import uuid
import random
import argparse
from datetime import datetime, timedelta

EVENT_TYPES = ['CLICK', 'VIEW', 'PURCHASE', 'ADD_TO_CART', 'WISHLIST']
CATEGORIES  = ['Electronics', 'Fashion', 'Food', 'Sport', 'Books', 'Beauty']
PRODUCTS    = [f'PRD{str(i).zfill(3)}' for i in range(1, 21)]
USERS       = [f'USR{str(i).zfill(3)}' for i in range(1, 51)]

def make_event():
    product_id = random.choice(PRODUCTS)
    category   = random.choice(CATEGORIES)
    price      = round(random.uniform(10000, 5000000), 2)
    ts         = datetime.utcnow() - timedelta(seconds=random.randint(0, 86400))

    return {
        "event_id":   str(uuid.uuid4()),
        "event_type": random.choice(EVENT_TYPES),
        "user_id":    random.choice(USERS),
        "product_id": product_id,
        "category":   category,
        "price":      price,
        "timestamp":  ts.isoformat() + "Z",
        "session_id": str(uuid.uuid4()),
        "platform":   random.choice(["web", "mobile-ios", "mobile-android"]),
    }

def send_events(stream_name: str, count: int, region: str):
    client = boto3.client('kinesis', region_name=region)
    sent   = 0
    batch  = []
    print(f"Mengirim {count} event ke stream '{stream_name}'...")

    for i in range(count):
        event = make_event()
        batch.append({
            'Data':         json.dumps(event).encode('utf-8'),
            'PartitionKey': event['user_id'],
        })

        # Kirim per 25 record (batas put_records)
        if len(batch) == 25 or i == count - 1:
            resp = client.put_records(StreamName=stream_name, Records=batch)
            failed = resp.get('FailedRecordCount', 0)
            sent  += len(batch) - failed
            print(f"  Batch {i//25 + 1}: {len(batch)} dikirim, {failed} gagal")
            batch = []

    print(f"\nSelesai. Total terkirim: {sent}/{count}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Kinesis Event Simulator LKS 2026')
    parser.add_argument('--stream', default='kds-nusashop-events-2026')
    parser.add_argument('--count',  type=int, default=1000)
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()

    send_events(args.stream, args.count, args.region)
