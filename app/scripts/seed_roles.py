from app.db.session import SessionLocal
from app.models.role import Role
from app.models.permission import Permission


def seed():
    db = SessionLocal()

    create_user = Permission(name="create_user")
    delete_user = Permission(name="delete_user")
    view_profile = Permission(name="view_profile")

    superadmin = Role(name="superadmin", permissions=[create_user, delete_user, view_profile])
    admin = Role(name="admin", permissions=[create_user, view_profile])
    user = Role(name="user", permissions=[view_profile])

    db.add_all([superadmin, admin, user])
    db.commit()
    db.close()


if __name__ == "__main__":
    seed()