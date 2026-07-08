import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, ExecKPI, ExecBranchPerformance

SQLALCHEMY_DATABASE_URL = "sqlite:///./aarohan_local.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

logger = logging.getLogger("exec-service")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    try:
        logger.info("Initializing database tables for exec-service...")
        Base.metadata.create_all(bind=engine)
        
        # Seed default dashboard KPIs if empty
        db = SessionLocal()
        if not db.query(ExecKPI).first():
            k1 = ExecKPI(metric_name="TOTAL_PORTFOLIO_VOLUME", metric_value=2450000000.0) # 245 Crores
            k2 = ExecKPI(metric_name="ACTIVE_MSME_COUNT", metric_value=1240.0)
            k3 = ExecKPI(metric_name="AVERAGE_HEALTH_SCORE", metric_value=82.4)
            k4 = ExecKPI(metric_name="PORTFOLIO_APPROVAL_RATE", metric_value=78.6) # 78.6%
            db.add_all([k1, k2, k3, k4])
            
        if not db.query(ExecBranchPerformance).first():
            b1 = ExecBranchPerformance(branch_name="Coimbatore MSME Hub", region="South", loan_disbursed_amt=850000000.0, active_accounts=450, average_health_score=84.5)
            b2 = ExecBranchPerformance(branch_name="Mumbai Corporate", region="West", loan_disbursed_amt=1100000000.0, active_accounts=520, average_health_score=81.2)
            b3 = ExecBranchPerformance(branch_name="Ludhiana Industrial Hub", region="North", loan_disbursed_amt=500000000.0, active_accounts=270, average_health_score=80.6)
            db.add_all([b1, b2, b3])
            
        db.commit()
        db.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Failed to initialize database: {str(e)}")
