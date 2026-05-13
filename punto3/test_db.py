import os
os.environ['DATABASE_URL'] = 'postgresql://postgres:5156montes@fastapi-taller-db.cp0uua4wm9yi.us-east-2.rds.amazonaws.com:5432/postgres'
os.environ['S3_BUCKET_NAME'] = 'seb-punto3-talleraws'

from database import get_engine
from models import Base

engine = get_engine()
Base.metadata.create_all(bind=engine)
print('✅ Conexión a RDS exitosa y tablas creadas')