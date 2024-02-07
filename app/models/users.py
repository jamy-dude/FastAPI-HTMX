from datetime import datetime

# from fastapi import Depends
from fastapi_users.db import SQLAlchemyBaseUserTableUUID

# from fastapi_users_db_sqlalchemy import GUID
from sqlalchemy import UUID, DateTime, String

# from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.schema import ForeignKey

from app.models.base import Base, BaseSQLModel
from app.models.groups import UserGroupLink


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "users"
    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    # add 1 to 1 relationship with the role model keeping default as None
    # Default value on creating user is None and updated later
    role_id: Mapped[UUID] = mapped_column(
        ForeignKey("roles.id"), nullable=True, default=None
    )
    # Role is defined in quotes to avoid type errors
    role: Mapped["Role"] = relationship(
        "Role",
        uselist=False,
        back_populates="user",
    )
    # items: Mapped["Item"] = relationship(back_populates="user", cascade="all, delete")
    # Creating a relationship with the activity model
    activity: Mapped["UserActivity"] = relationship(
        "UserActivity", back_populates="user"
    )
    # Creating a relationship with the group user link model
    group_users: Mapped["UserGroupLink"] = relationship(
        "UserGroupLink",
        back_populates="user",
    )

    # string representation of an object
    def __repr__(self):
        return f"User(id={self.id!r}, name={self.email!r})"


class Role(BaseSQLModel):
    __tablename__ = "roles"
    role_name: Mapped[str] = mapped_column(
        String(length=200), nullable=False, unique=True
    )
    role_desc: Mapped[str | None] = mapped_column(String(length=1024), nullable=True)

    # user_id: Mapped[UUID] = mapped_column(GUID, ForeignKey("users.id"))
    user: Mapped["User"] = relationship("User", back_populates="role")


# Sql alchemy model to track and save user activity
class UserActivity(BaseSQLModel):
    """
    Tracks user activities such as sign-ins, sign-ups, and other events.

    Parameters:
        user_id (UUID): The ID of the user.
        activity_date (datetime): The date and time of the activity.
        activity_type (str): The type of activity, such as "sign-in" or "sign-up".
        activity_desc (str): A description of the activity.
    """

    __tablename__ = "user_activity"
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), default=None)
    activity_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    activity_type: Mapped[str] = mapped_column(String(length=200), nullable=False)
    activity_desc: Mapped[str | None] = mapped_column(
        String(length=1024), nullable=True
    )
    user: Mapped["User"] = relationship("User", back_populates="activity")
