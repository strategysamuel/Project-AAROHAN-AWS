import logging
from services.shared.database import engine, SessionLocal, get_db, Base
from app.models import Role, Permission, User
from app.auth import hash_password

logger = logging.getLogger("auth-service")

def init_db():
    try:
        import app.models
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")

def seed_database():
    """Seed initial roles, permissions, and users for UAT and testing"""
    db = SessionLocal()
    try:
        # 1. Create permissions schema
        import app.models
        Base.metadata.create_all(bind=engine)
        
        # Check if already seeded
        if db.query(Role).first():
            return
            
        logger.info("Seeding database with default roles & users...")
        
        p_read = Permission(name="loan:read", description="Read loan files")
        p_create = Permission(name="loan:create", description="Register new loan application")
        p_approve = Permission(name="loan:approve", description="Approve credit limit applications")
        
        db.add_all([p_read, p_create, p_approve])
        db.commit()
        
        # 2. Configure roles
        rm_role = Role(name="RELATIONSHIP_MANAGER", description="Sales Relationship Manager")
        rm_role.permissions.extend([p_read, p_create])
        
        credit_role = Role(name="CREDIT_ANALYST", description="Underwriting Analyst")
        credit_role.permissions.extend([p_read, p_approve])
        
        customer_role = Role(name="CUSTOMER", description="MSME Client")
        customer_role.permissions.append(p_read)
        
        db.add_all([rm_role, credit_role, customer_role])
        db.commit()
        
        # 3. Create users
        rm_user = User(
            mobile_number="9876543210",
            email="rm@aarohan.bank",
            hashed_password=hash_password("AarohanPass123!"),
            full_name="Rajesh RM Kumar",
            role=rm_role
        )
        
        customer_user = User(
            mobile_number="9988776655",
            email="proprietor@msme.com",
            hashed_password=hash_password("ClientPass123!"),
            full_name="Amit MSME Patel",
            role=customer_role
        )
        
        db.add_all([rm_user, customer_user])
        db.commit()
        logger.info("Database successfully seeded.")
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()
