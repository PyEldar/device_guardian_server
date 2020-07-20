from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models import devices as devices_models
from app.schemas import devices as devices_schemas
from app import crud, deps

router = APIRouter()
