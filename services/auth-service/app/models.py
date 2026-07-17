import datetime
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

# Many-to-many relationship helper table for Role and Permission
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column("role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True),
    Column("permission_id", Integer, ForeignKey("permissions.id", ondelete="CASCADE"), primary_key=True)
)

class Permission(Base):
    __tablename__ = "permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True) # e.g. "loan:create", "loan:approve"
    description = Column(String(255), nullable=True)

class Role(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False, index=True) # e.g. "RELATIONSHIP_MANAGER", "CUSTOMER"
    description = Column(String(255), nullable=True)
    
    permissions = relationship("Permission", secondary=role_permissions, backref="roles")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=True, index=True)
    mobile_number = Column(String(15), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    department = Column(String(100), nullable=True)
    branch = Column(String(100), nullable=True)
    avatar = Column(String(255), nullable=True)
    status = Column(String(50), default="ACTIVE")
    
    role_id = Column(Integer, ForeignKey("roles.id"), nullable=False)
    role = relationship("Role", backref="users")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token = Column(String(255), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=False)
    is_revoked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
