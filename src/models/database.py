from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL_ASYNC,
    echo=True, 
)

async_session_maker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)