from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker

url = 'mysql+asyncmy://root:dudu1234E@localhost:3306/fastapi'

engine = create_async_engine(url)

async_session = sessionmaker(engine, class_=AsyncSession)
