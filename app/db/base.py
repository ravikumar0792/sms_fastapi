from app.db.base_class import Base

from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.role_permission import role_permissions
from app.models.class_model import Class
from app.models.section import Section
from app.models.subject import Subject
from app.models.academic_year import AcademicYear
from app.models.student import Student
from app.models.teacher import Teacher
from app.models.teacher_subject import teacher_subject
from app.models.parent import Parent
from app.models.parent_student import parent_student