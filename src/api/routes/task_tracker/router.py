import logging

from fastapi import APIRouter

task_tracker = APIRouter(prefix='/task_tracker')
logger = logging.getLogger('app')
