from backend.app.db.database import engine, Base, SessionLocal
from backend.app.db.models import UserDB
from backend.app.auth.password_utils import hash_password

# Ensure tables exist
Base.metadata.create_all(bind=engine)

def add_user():
    db = SessionLocal()
    try:
        username = input("Enter username : ").strip()
        role = input("Enter role     : ").strip().lower()
        password = input("Enter password : ").strip()

        existing = (
            db.query(UserDB)
            .filter(UserDB.username == username, UserDB.role == role)
            .first()
        )

        if existing:
            print("❌ User with same username and role already exists.")
            return

        user = UserDB(
            username=username,
            role=role,
            hashed_password=hash_password(password),
        )

        db.add(user)
        db.commit()
        print("✅ User added successfully.")

    finally:
        db.close()


def delete_user():
    db = SessionLocal()
    try:
        username = input("Enter username to delete : ").strip()
        role = input("Enter role of user       : ").strip().lower()

        user = (
            db.query(UserDB)
            .filter(UserDB.username == username, UserDB.role == role)
            .first()
        )

        if not user:
            print("❌ No user found with given username and role.")
            return

        db.delete(user)
        db.commit()
        print("✅ User deleted successfully.")

    finally:
        db.close()


def main():
    print("\n=== USER DATABASE MANAGER ===")
    print("1. Add user")
    print("2. Delete user")
    print("3. Exit")

    choice = input("\nSelect an option (1/2/3): ").strip()

    if choice == "1":
        add_user()
    elif choice == "2":
        delete_user()
    elif choice == "3":
        print("Exiting...")
    else:
        print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
