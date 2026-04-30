from pydantic import BaseModel, field_validator
from datetime import date
from enum import Enum


class LeaveStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"


class LeaveCreate(BaseModel):
    start_date: date
    end_date: date
    reason: str

    @field_validator("end_date")
    def validate_dates(cls, v, values):
        if "start_date" in values and v < values["start_date"]:
            raise ValueError("end_date cannot be before start_date")
        return v


class LeaveOut(BaseModel):
    id: int
    start_date: date
    end_date: date
    reason: str
    status: LeaveStatus

    class Config:
        from_attributes = True