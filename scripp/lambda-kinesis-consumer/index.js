/**
 * Lambda: lambda-kinesis-consumer-2026
 * Trigger: Kinesis Data Stream kds-nusashop-events-2026
 * Runtime: Node.js 20.x
 *
 * Fungsi: Baca event dari Kinesis, validasi schema, simpan ke DynamoDB
 */

const { DynamoDBClient, PutItemCommand } = require("@aws-sdk/client-dynamodb");
const { marshall } = require("@aws-sdk/util-dynamodb");

const client = new DynamoDBClient({ region: process.env.AWS_REGION || "us-east-1" });
const TABLE  = process.env.TABLE_NAME || "ddb-nusashop-events-2026";

const REQUIRED_FIELDS = ["event_id", "event_type", "user_id", "product_id", "timestamp"];

exports.handler = async (event) => {
  console.log(`Menerima ${event.Records.length} record dari Kinesis`);

  let success = 0;
  let failed  = 0;

  for (const record of event.Records) {
    try {
      // Decode dari base64
      const payload = Buffer.from(record.kinesis.data, "base64").toString("utf-8");
      const item    = JSON.parse(payload);

      // Validasi field wajib
      const missing = REQUIRED_FIELDS.filter(f => !item[f]);
      if (missing.length > 0) {
        console.warn(`Lewati record: field tidak lengkap [${missing.join(", ")}]`);
        failed++;
        continue;
      }

      // Simpan ke DynamoDB
      await client.send(new PutItemCommand({
        TableName: TABLE,
        Item: marshall({
          event_id:   item.event_id,
          timestamp:  item.timestamp,
          event_type: item.event_type,
          user_id:    item.user_id,
          product_id: item.product_id,
          category:   item.category   || "unknown",
          price:      item.price      || 0,
          platform:   item.platform   || "web",
          session_id: item.session_id || "",
          ingested_at: new Date().toISOString(),
        }),
        ConditionExpression: "attribute_not_exists(event_id)", // hindari duplikat
      }));

      success++;
    } catch (err) {
      if (err.name === "ConditionalCheckFailedException") {
        // Event sudah ada, skip
        success++;
      } else {
        console.error("Error simpan record:", err);
        failed++;
      }
    }
  }

  console.log(`Selesai: ${success} berhasil, ${failed} gagal`);
  return { statusCode: 200, processed: success, failed };
};
