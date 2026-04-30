from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import extract

from app.db.deps import get_db
from app.models.attendance import Attendance
from app.models.student import Student
from app.models.leave import Leave

from app.schemas.attendance import BulkAttendanceCreate
from app.schemas.leave import LeaveCreate

from app.core.permissions import require_permission
from app.core.security import get_current_user

from app.services.notification import send_email, send_sms, send_email_background
from fastapi import BackgroundTasks


router = APIRouter(prefix="/attendance", tags=["Attendance"])

@router.post(
    "/mark",
    dependencies=[Depends(require_permission("mark_attendance"))]
)
def mark_attendance(
    payload: BulkAttendanceCreate,
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):

    for record in payload.records:

        student = db.query(Student).filter(Student.id == record.student_id).first()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        existing = db.query(Attendance).filter(
            Attendance.student_id == record.student_id,
            Attendance.date == payload.date
        ).first()

        if existing:
            existing.status = record.status
            attendance_obj = existing
        else:
            attendance_obj = Attendance(
                student_id=record.student_id,
                date=payload.date,
                status=record.status
            )
            db.add(attendance_obj)

        # 🔔 Send async notification ONLY if absent
        if record.status == "absent" and not attendance_obj.is_notified:

            message = f"Your child is absent on {payload.date}"

            if student.user and student.user.email:
                background_tasks.add_task(
                    send_email,
                    student.user.email,
                    "Absent Alert",
                    message
                )

            if student.user and student.user.phone:
                background_tasks.add_task(
                    send_sms,
                    student.user.phone,
                    message
                )

            attendance_obj.is_notified = True

    db.commit()

    return {"message": "Attendance recorded successfully"}

@router.get(
    "/by-date",
    dependencies=[Depends(require_permission("view_attendance"))]
)
def get_attendance_by_date(att_date: date, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.date == att_date).all()

@router.get(
    "/student/{student_id}",
    dependencies=[Depends(require_permission("view_attendance"))]
)
def get_student_attendance(student_id: int, db: Session = Depends(get_db)):
    return db.query(Attendance).filter(Attendance.student_id == student_id).all()

@router.get(
    "/report/daily",
    dependencies=[Depends(require_permission("view_reports"))]
)
def daily_report(att_date: date, db: Session = Depends(get_db)):

    records = db.query(Attendance).filter(Attendance.date == att_date).all()

    return {
        "total": len(records),
        "present": sum(r.status == "present" for r in records),
        "absent": sum(r.status == "absent" for r in records),
        "late": sum(r.status == "late" for r in records),
    }

@router.get(
    "/report/monthly",
    dependencies=[Depends(require_permission("view_reports"))]
)
def monthly_report(month: int, year: int, db: Session = Depends(get_db)):

    records = db.query(Attendance).filter(
        extract("month", Attendance.date) == month,
        extract("year", Attendance.date) == year
    ).all()

    return {"total_records": len(records)}

@router.get(
    "/report/yearly",
    dependencies=[Depends(require_permission("view_reports"))]
)
def yearly_report(year: int, db: Session = Depends(get_db)):

    records = db.query(Attendance).filter(
        extract("year", Attendance.date) == year
    ).all()

    return {"total_records": len(records)}

@router.post(
    "/leave/apply",
    dependencies=[Depends(require_permission("apply_leave"))]
)
def apply_leave(
    data: LeaveCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):

    leave = Leave(
        user_id=current_user.id,
        start_date=data.start_date,
        end_date=data.end_date,
        reason=data.reason
    )

    db.add(leave)
    db.commit()

    return {"message": "Leave applied"}

@router.put(
    "/leave/{leave_id}",
    dependencies=[Depends(require_permission("approve_leave"))]
)
def update_leave(leave_id: int, status: str, db: Session = Depends(get_db)):

    leave = db.query(Leave).filter(Leave.id == leave_id).first()

    if not leave:
        raise HTTPException(status_code=404, detail="Leave not found")

    if status not in ["approved", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status")

    leave.status = status
    db.commit()

    return {"message": f"Leave {status}"}