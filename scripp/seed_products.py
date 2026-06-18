#!/usr/bin/env python3
"""
DynamoDB Product Seeder – LKS Cloud Computing 2026
Isi tabel ddb-nusashop-products-2026 dengan 20 produk

Cara pakai:
  pip install boto3
  python3 seed_products.py --table ddb-nusashop-products-2026 --region us-east-1
"""

import boto3
import argparse
from decimal import Decimal

PRODUCTS = [
    {"product_id":"PRD001","name":"Laptop Asus VivoBook 14","category":"Electronics","price":Decimal("8500000"),"stock":15,"rating":Decimal("4.3"),"brand":"Asus"},
    {"product_id":"PRD002","name":"Sepatu Nike Air Max 270","category":"Fashion","price":Decimal("1250000"),"stock":30,"rating":Decimal("4.7"),"brand":"Nike"},
    {"product_id":"PRD003","name":"Kopi Toraja Premium 500g","category":"Food","price":Decimal("125000"),"stock":200,"rating":Decimal("4.8"),"brand":"Toraja Coffee"},
    {"product_id":"PRD004","name":"Raket Badminton Yonex Astrox","category":"Sport","price":Decimal("850000"),"stock":20,"rating":Decimal("4.5"),"brand":"Yonex"},
    {"product_id":"PRD005","name":"Novel Laskar Pelangi","category":"Books","price":Decimal("75000"),"stock":50,"rating":Decimal("4.9"),"brand":"Bentang Pustaka"},
    {"product_id":"PRD006","name":"Smartphone Samsung Galaxy A55","category":"Electronics","price":Decimal("5200000"),"stock":25,"rating":Decimal("4.4"),"brand":"Samsung"},
    {"product_id":"PRD007","name":"Tas Ransel Eiger Cordura","category":"Fashion","price":Decimal("450000"),"stock":40,"rating":Decimal("4.6"),"brand":"Eiger"},
    {"product_id":"PRD008","name":"Teh Pucuk Harum 1.5L (6pcs)","category":"Food","price":Decimal("48000"),"stock":500,"rating":Decimal("4.2"),"brand":"Teh Pucuk"},
    {"product_id":"PRD009","name":"Sepeda Gunung Polygon Xtrada","category":"Sport","price":Decimal("3800000"),"stock":8,"rating":Decimal("4.5"),"brand":"Polygon"},
    {"product_id":"PRD010","name":"Buku Clean Code by Robert Martin","category":"Books","price":Decimal("185000"),"stock":35,"rating":Decimal("4.9"),"brand":"Prentice Hall"},
    {"product_id":"PRD011","name":"Headphone Sony WH-1000XM5","category":"Electronics","price":Decimal("4500000"),"stock":12,"rating":Decimal("4.8"),"brand":"Sony"},
    {"product_id":"PRD012","name":"Kemeja Batik Pria Premium","category":"Fashion","price":Decimal("320000"),"stock":60,"rating":Decimal("4.3"),"brand":"Danar Hadi"},
    {"product_id":"PRD013","name":"Rendang Padang Kaleng 500g","category":"Food","price":Decimal("85000"),"stock":150,"rating":Decimal("4.7"),"brand":"Kokita"},
    {"product_id":"PRD014","name":"Tenis Meja Butterfly Table","category":"Sport","price":Decimal("1200000"),"stock":10,"rating":Decimal("4.4"),"brand":"Butterfly"},
    {"product_id":"PRD015","name":"Atomic Habits – James Clear","category":"Books","price":Decimal("98000"),"stock":75,"rating":Decimal("4.9"),"brand":"Gramedia"},
    {"product_id":"PRD016","name":"Monitor LG 27\" 4K IPS","category":"Electronics","price":Decimal("4800000"),"stock":7,"rating":Decimal("4.6"),"brand":"LG"},
    {"product_id":"PRD017","name":"Parfum Erigo 30ml","category":"Beauty","price":Decimal("89000"),"stock":100,"rating":Decimal("4.2"),"brand":"Erigo"},
    {"product_id":"PRD018","name":"Kursi Gaming Razer Iskur","category":"Electronics","price":Decimal("6500000"),"stock":5,"rating":Decimal("4.7"),"brand":"Razer"},
    {"product_id":"PRD019","name":"Mie Instan Indomie Jumbo (40pcs)","category":"Food","price":Decimal("112000"),"stock":300,"rating":Decimal("4.8"),"brand":"Indofood"},
    {"product_id":"PRD020","name":"Sepatu Lari Adidas Ultraboost","category":"Sport","price":Decimal("2200000"),"stock":22,"rating":Decimal("4.6"),"brand":"Adidas"},
]

def seed_products(table_name: str, region: str):
    ddb = boto3.resource('dynamodb', region_name=region)
    table = ddb.Table(table_name)
    print(f"Mengisi {len(PRODUCTS)} produk ke tabel '{table_name}'...")

    with table.batch_writer() as batch:
        for p in PRODUCTS:
            batch.put_item(Item=p)
            print(f"  ✓ {p['product_id']} – {p['name']}")

    print(f"\nSelesai. {len(PRODUCTS)} produk berhasil di-load.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--table',  default='ddb-nusashop-products-2026')
    parser.add_argument('--region', default='us-east-1')
    args = parser.parse_args()
    seed_products(args.table, args.region)
