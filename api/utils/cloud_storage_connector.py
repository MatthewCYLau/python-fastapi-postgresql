from datetime import datetime, timezone
from google.cloud import storage
import pytz


class CloudStorageConnector:
    def __init__(
        self,
        bucket_name,
    ) -> None:

        self.bucket_name = bucket_name
        self.storage_client = storage.Client()
        self.placeholder_text = ["Column A,Column B", "Value A,Value B"]

    def upload_csv_file(self) -> str:
        bucket = self.storage_client.bucket(self.bucket_name)

        GB = pytz.timezone("Europe/London")
        timestamp = datetime.now(timezone.utc).astimezone(GB).strftime("%Y%m%d%H%M%S")
        csv_file_name = f"{timestamp}-export.csv"

        blob = bucket.blob(f"uploads/{csv_file_name}")
        with open(csv_file_name, "wt", encoding="utf-8") as f:
            for line in self.placeholder_text:
                f.write(line + "\n")

        with open(csv_file_name, "rb") as f:
            blob.upload_from_file(f)

        return blob.public_url
