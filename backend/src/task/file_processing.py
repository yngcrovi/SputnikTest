from src.db.service import FileService, AlertService

class FileProcessing(FileService, AlertService):

    def __init__(self):
        FileService.__init__(self)
        AlertService.__init__(self)

    async def process_file(self, file_id: str) -> None:
        await self.scan_file_for_threats(file_id)
        await self.extract_file_metadata(file_id)
        await self.send_file_alert(file_id)

    async def scan_file_for_threats(self, file_id: str) -> None:
        await self._scan_file_for_threats(file_id)


    async def extract_file_metadata(self, file_id: str) -> None:
        await self._extract_file_metadata(file_id)

    async def send_file_alert(self, file_id: str) -> None:
        file_item = await self.get_file(file_id, False)
        if file_item.processing_status == "failed":
            await self.create_alert(file_id=file_id, level="critical", message="File processing failed")
        elif file_item.requires_attention:
            await self.create_alert(
                file_id=file_id,
                level="warning",
                message=f"File requires attention: {file_item.scan_details}",
            )
        else:
            await self.create_alert(file_id=file_id, level="info", message="File processed successfully")

file_processing = FileProcessing()