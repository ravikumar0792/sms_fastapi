from pydantic import BaseModel
from datetime import date
from typing import List
from enum import Enum


class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"
    leave = "leave"   # ✅ add this


class AttendanceCreate(BaseModel):
    student_id: int
    status: AttendanceStatus


class BulkAttendanceCreate(BaseModel):
    date: date
    records: List[AttendanceCreate]


class AttendanceOut(BaseModel):
    student_id: int
    date: date
    status: AttendanceStatus

    class Config:
        from_attributes = True