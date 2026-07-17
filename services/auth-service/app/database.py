import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, Role, Permission, User
from app.auth import hash_password

# Use SQLITE for fast local development validation
SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("auth-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def seed_database():
    """Seed initial roles, permissions, and users for UAT and testing"""
    db = SessionLocal()
    try:
        # 1. Create permissions schema
        Base.metadata.create_all(bind=engine)
        
        # Check if already seeded
        if db.query(Role).first():
            return
            
        logger.info("Seeding database with default roles & users...")
        
        # Create permissions corresponding to navigation modules
        modules = [
            "Dashboard", "Customer Management", "CKYC", "GST", "Account Aggregator",
            "EPFO", "MCA", "Financial Health Card", "Credit Engine", "CAM", "OCEN",
            "RBI Fraud", "Reports", "Administration", "Simulation Engine", "Settings"
        ]
        
        perms_dict = {}
        for m in modules:
            p = Permission(name=m.lower().replace(" ", "_"), description=f"Access to {m}")
            db.add(p)
            perms_dict[m] = p
            
        db.commit()
        
        # Helper to get permissions by names
        def get_perms(names):
            return [perms_dict[n] for n in names if n in perms_dict]
        
        # 2. Configure roles
        admin_role = Role(name="ADMINISTRATOR", description="System Administrator")
        admin_role.permissions.extend(list(perms_dict.values()))
        
        rm_role = Role(name="RELATIONSHIP_MANAGER", description="Relationship Manager")
        rm_role.permissions.extend(get_perms(["Dashboard", "Customer Management", "CKYC", "GST", "Account Aggregator", "EPFO", "MCA", "Financial Health Card", "Reports"]))
        
        credit_role = Role(name="CREDIT_MANAGER", description="Credit Manager")
        credit_role.permissions.extend(get_perms(["Dashboard", "Customer Management", "Financial Health Card", "Credit Engine", "CAM", "Reports"]))
        
        ops_role = Role(name="OPERATIONS_OFFICER", description="Operations Officer")
        ops_role.permissions.extend(get_perms(["Dashboard", "Customer Management", "OCEN", "Reports"]))
        
        exec_role = Role(name="EXECUTIVE", description="Executive Board Member")
        exec_role.permissions.extend(get_perms(["Dashboard", "Reports"]))
        
        auditor_role = Role(name="AUDITOR", description="System Auditor")
        auditor_role.permissions.extend(get_perms(["Dashboard", "Reports"]))
        
        trainer_role = Role(name="TRAINER", description="Platform Instructor/Trainer")
        trainer_role.permissions.extend(get_perms(["Dashboard", "Customer Management", "Simulation Engine", "Reports"]))
        
        demo_role = Role(name="DEMO_USER", description="Standard Demo User")
        demo_role.permissions.extend(get_perms(["Dashboard", "Customer Management", "Reports"]))
        
        db.add_all([admin_role, rm_role, credit_role, ops_role, exec_role, auditor_role, trainer_role, demo_role])
        db.commit()
        
        # 3. Create users
        users_config = [
            ("admin", "admin@aarohan.bank", "9900112233", "ADMINISTRATOR", "IT Operations", "Mumbai HQ"),
            ("rm_user", "rm@aarohan.bank", "9876543210", "RELATIONSHIP_MANAGER", "MSME Sales", "Delhi Branch"),
            ("credit_user", "credit@aarohan.bank", "9812345678", "CREDIT_MANAGER", "Underwriting", "Mumbai HQ"),
            ("ops_user", "ops@aarohan.bank", "9823456789", "OPERATIONS_OFFICER", "Retail Ops", "Bangalore Branch"),
            ("exec_user", "exec@aarohan.bank", "9834567890", "EXECUTIVE", "Management", "Mumbai HQ"),
            ("auditor_user", "auditor@aarohan.bank", "9845678901", "AUDITOR", "Risk Audit", "Delhi Branch"),
            ("trainer_user", "trainer@aarohan.bank", "9856789012", "TRAINER", "HR Enablement", "Pune Branch"),
            ("demo_user", "demo@aarohan.bank", "9988776655", "DEMO_USER", "Showcase Sandbox", "Mumbai HQ")
        ]
        
        for username, email, mobile, role_name, dept, branch in users_config:
            r = db.query(Role).filter(Role.name == role_name).first()
            user = User(
                username=username,
                mobile_number=mobile,
                email=email,
                hashed_password=hash_password("AarohanPass123!"),
                full_name=username.replace("_", " ").title(),
                department=dept,
                branch=branch,
                avatar=f"/assets/avatars/{username}.png",
                status="ACTIVE",
                role=r
            )
            db.add(user)
            
        db.commit()
        logger.info("Database successfully seeded with 8 demo roles and users.")
    except Exception as e:
        logger.error(f"Error seeding database: {str(e)}")
        db.rollback()
    finally:
        db.close()
