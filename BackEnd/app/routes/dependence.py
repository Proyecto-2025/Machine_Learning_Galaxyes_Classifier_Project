
from ..services.db_service import DbService
from ..services.file_storage_service import FileStorageService
from ..services.com_service import ComService

db_service = DbService()
file_storage_service = FileStorageService()
com_service = ComService(db_service=db_service, storage_service=file_storage_service)
