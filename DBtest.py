from sqlalchemy import create_engine


HOST = 'ec2-23-23-199-57.compute-1.amazonaws.com'
USERNAME = 'bdixfxblwpkpeq'
DATBASE = 'd92n7id44085nq'
PORT = '5432'
PASSWORD = '3ab0b9eb1c88515244539d0b2e04c6d269ea4cd4e2bada888646be761598bfec'


# engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATBASE}')
engine = create_engine(f'postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATBASE}')
engine.connect()

print(engine)