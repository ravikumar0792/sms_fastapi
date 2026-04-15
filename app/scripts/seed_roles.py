from app.db.session import SessionLocal
from app.models.role import Role
from app.models.permission import Permission
from app.models.user import User  # Import your User model
from app.core.security import hash_password  # Adjust this import to your actual hash utility path

def seed():
    db = SessionLocal()
    try:
        # 1. Create Permissions
        create_user = Permission(name="create_user")
        delete_user = Permission(name="delete_user")
        view_profile = Permission(name="view_profile")

        # 2. Create Roles
        superadmin_role = Role(name="superadmin", permissions=[create_user, delete_user, view_profile])
        admin_role = Role(name="admin", permissions=[create_user, view_profile])
        user_role = Role(name="user", permissions=[view_profile])

        db.add_all([superadmin_role, admin_role, user_role])
        db.flush()  # Flush to get the IDs without committing yet

        # 3. Create SuperAdmin User
        super_user = User(
            first_name="Ravi",
            last_name="Kumar",
            phone="790379778",
            email="ravikumar.gift@gmail.com",
            hashed_password=hash_password("Pass!234"),
            role=superadmin_role,
            is_active=True,
            is_verified=True
        )

        db.add(super_user)
        db.commit()
        print("Database seeded: Permissions, Roles, and SuperAdmin created.")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed()
