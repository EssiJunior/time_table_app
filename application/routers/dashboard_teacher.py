from fastapi import APIRouter
from datetime import datetime

router = APIRouter(
    prefix="",
    tags=["Teacher's Dashbord"]
)

@router.post("/t_home")
def display_some_thing():
    return {"message": "I am a teacher.","date": datetime.now()}
    