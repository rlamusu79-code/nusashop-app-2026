/**
 * Lambda: lambda-recommend-api-2026
 * Trigger: API Gateway GET /recommend?user_id=XXX
 * Runtime: Python 3.12
 *
 * Fungsi: Kembalikan Top-5 rekomendasi produk berdasarkan user_id
 */

import json
import os
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal

# Konfigurasi dari environment variable
PRODUCTS_TABLE = os.environ.get("TABLE_NAME",    "ddb-nusashop-products-2026")
EVENTS_TABLE   = os.environ.get("EVENTS_TABLE",  "ddb-nusashop-events-2026")
REGION         = os.environ.get("AWS_REGION",    "us-east-1")

ddb = boto3.resource("dynamodb", region_name=REGION)

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def get_user_history(user_id: str) -> list:
    """Ambil riwayat kategori yang dibeli user dari DynamoDB via GSI."""
    try:
        table = ddb.Table(EVENTS_TABLE)
        resp = table.query(
            IndexName="user-event-index",
            KeyConditionExpression=Key("user_id").eq(user_id),
            FilterExpression="event_type = :et",
            ExpressionAttributeValues={":et": "PURCHASE"},
            Limit=50,
        )
        purchased_ids = {item["product_id"] for item in resp.get("Items", [])}
        return list(purchased_ids)
    except Exception as e:
        print(f"Error ambil riwayat: {e}")
        return []

def get_all_products() -> list:
    """Scan semua produk dari DynamoDB."""
    try:
        table = ddb.Table(PRODUCTS_TABLE)
        resp  = table.scan()
        return resp.get("Items", [])
    except Exception as e:
        print(f"Error ambil produk: {e}")
        return []

def recommend(user_id: str) -> list:
    """
    Simple content-based recommendation:
    - Ambil riwayat pembelian user
    - Temukan kategori favorit
    - Rekomendasikan produk dari kategori tersebut yang belum dibeli
    - Fallback: produk rating tertinggi
    """
    all_products  = get_all_products()
    user_history  = get_user_history(user_id)

    # Filter produk yang belum dibeli
    unseen = [p for p in all_products if p["product_id"] not in user_history]

    if not unseen:
        unseen = all_products  # jika semua sudah dibeli, tampilkan semua

    # Sort by rating desc, price asc sebagai tiebreaker
    sorted_prods = sorted(
        unseen,
        key=lambda x: (-float(x.get("rating", 0)), float(x.get("price", 0)))
    )

    # Ambil Top-5
    top5 = sorted_prods[:5]
    return [
        {
            "product_id": p["product_id"],
            "name":       p.get("name", ""),
            "category":   p.get("category", ""),
            "price":      float(p.get("price", 0)),
            "rating":     float(p.get("rating", 0)),
            "reason":     "Highly rated & belum pernah dibeli",
        }
        for p in top5
    ]

def lambda_handler(event, context):
    print(f"Event masuk: {json.dumps(event)}")

    # Ambil user_id dari query string
    params  = event.get("queryStringParameters") or {}
    user_id = params.get("user_id", "").strip()

    if not user_id:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"},
            "body": json.dumps({"ok": False, "message": "Parameter user_id wajib diisi"}),
        }

    recommendations = recommend(user_id)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
        },
        "body": json.dumps({
            "ok":             True,
            "user_id":        user_id,
            "recommendations": recommendations,
            "total":           len(recommendations),
        }, cls=DecimalEncoder),
    }
