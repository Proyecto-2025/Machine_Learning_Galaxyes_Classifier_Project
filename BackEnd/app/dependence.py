
from flask import current_app

def get_com_service():
    return current_app.com_service

def get_db_service():
    return current_app.db_service

def get_storage_service():
    return current_app.storage_service
