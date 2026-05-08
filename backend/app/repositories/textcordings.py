import base64
import json
from datetime import UTC, datetime

import boto3
import ulid
from boto3.dynamodb.conditions import Key
from botocore.exceptions import BotoCoreError, ClientError


def _now() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _encode_cursor(key: dict | None) -> str | None:
    if not key:
        return None
    return base64.urlsafe_b64encode(json.dumps(key).encode()).decode()


def _decode_cursor(cursor: str | None) -> dict | None:
    if not cursor:
        return None
    return json.loads(base64.urlsafe_b64decode(cursor.encode()).decode())


class TextCordingRepository:
    def __init__(self, table_name: str, processor_function_name: str | None) -> None:
        self.table = boto3.resource("dynamodb").Table(table_name)
        self.processor_function_name = processor_function_name
        self.lambda_client = boto3.client("lambda") if processor_function_name else None

    def create(
        self,
        owner_user_id: str,
        original_text: str,
        vendor: str | None,
        voice: str | None,
    ) -> dict:
        textcording_id = str(ulid.new())
        now = _now()
        item = {
            "pk": f"USER#{owner_user_id}",
            "sk": f"TEXTCORDING#{textcording_id}",
            "textcording_id": textcording_id,
            "owner_user_id": owner_user_id,
            "original_text": original_text,
            "read_text": None,
            "recording": None,
            "vendor": vendor,
            "voice": voice,
            "status": "processing",
            "metadata": {},
            "char_count": len(original_text),
            "created_at": now,
            "updated_at": now,
        }

        self.table.put_item(Item=item)
        try:
            self._start_processing(owner_user_id, textcording_id)
        except ProcessingStartError:
            self._mark_processing_start_failed(owner_user_id, textcording_id)
            item["status"] = "failed_to_start"
            item["metadata"] = {"processing_start_error": "lambda_invoke_failed"}
            item["updated_at"] = _now()
            raise
        return item

    def _start_processing(self, owner_user_id: str, textcording_id: str) -> None:
        if not self.lambda_client or not self.processor_function_name:
            raise ProcessingStartError

        try:
            response = self.lambda_client.invoke(
                FunctionName=self.processor_function_name,
                InvocationType="Event",
                Payload=json.dumps(
                    {"textcording_id": textcording_id, "owner_user_id": owner_user_id}
                ).encode(),
            )
        except (BotoCoreError, ClientError) as exc:
            raise ProcessingStartError from exc

        if response.get("StatusCode") != 202:
            raise ProcessingStartError

    def _mark_processing_start_failed(self, owner_user_id: str, textcording_id: str) -> None:
        self.table.update_item(
            Key={"pk": f"USER#{owner_user_id}", "sk": f"TEXTCORDING#{textcording_id}"},
            UpdateExpression="SET #status = :status, metadata = :metadata, updated_at = :updated_at",
            ExpressionAttributeNames={"#status": "status"},
            ExpressionAttributeValues={
                ":status": "failed_to_start",
                ":metadata": {"processing_start_error": "lambda_invoke_failed"},
                ":updated_at": _now(),
            },
        )

    def list(
        self, owner_user_id: str, limit: int, cursor: str | None
    ) -> tuple[list[dict], str | None]:
        query = {
            "KeyConditionExpression": Key("pk").eq(f"USER#{owner_user_id}")
            & Key("sk").begins_with("TEXTCORDING#"),
            "Limit": limit,
            "ScanIndexForward": False,
        }
        if start_key := _decode_cursor(cursor):
            query["ExclusiveStartKey"] = start_key
        response = self.table.query(**query)
        return response.get("Items", []), _encode_cursor(response.get("LastEvaluatedKey"))

    def get(self, owner_user_id: str, textcording_id: str) -> dict | None:
        return self._get_item(owner_user_id, textcording_id)

    def delete(self, owner_user_id: str, textcording_id: str) -> None:
        item = self._get_item(owner_user_id, textcording_id)
        if not item:
            return
        self.table.delete_item(
            Key={"pk": f"USER#{owner_user_id}", "sk": f"TEXTCORDING#{textcording_id}"}
        )

    def _get_item(self, owner_user_id: str, textcording_id: str) -> dict | None:
        response = self.table.get_item(
            Key={"pk": f"USER#{owner_user_id}", "sk": f"TEXTCORDING#{textcording_id}"}
        )
        return response.get("Item")


class ProcessingStartError(Exception):
    pass
