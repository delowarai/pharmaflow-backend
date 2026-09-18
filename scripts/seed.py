from sqlalchemy import select

from app.core.permissions import UserRole
from app.core.security import hash_password
from app.db.database import Base, SessionLocal, engine
from app.models.pharmacy import Pharmacy
from app.models.user import User


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        existing = db.scalar(select(User).where(User.email == "owner@example.com"))
        if existing:
            print("Seed data already exists.")
            return

        pharmacy = Pharmacy(name="Example Pharmacy")
        owner = User(
            pharmacy=pharmacy,
            name="Pharmacy Owner",
            email="owner@example.com",
            password_hash=hash_password("ChangeMe123!"),
            role=UserRole.OWNER,
        )
        db.add(owner)
        db.commit()
        print("Created owner@example.com with password ChangeMe123!.")


if __name__ == "__main__":
    seed()
