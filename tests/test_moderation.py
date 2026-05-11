import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.db.session import redis_client,get_db, Base
from httpx import AsyncClient,ASGITransport
from app.main import app
pytestmark = pytest.mark.asyncio(scope="module")


# test db
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(TEST_DATABASE_URL)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)

# Create the override function
async def override_get_db():
    async with TestSessionLocal() as session:
        yield session

# tell app to use the override
app.dependency_overrides[get_db] = override_get_db

#Create the tables in RAM before the tests run
@pytest_asyncio.fixture(autouse=True, scope="module")
async def setup_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    # await redis_client.aclose()

@pytest.mark.asyncio
async def test_check_text_toxicity():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/moderation/check",
            json={"text": "I hate you, you are a terrible person!"}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["is_flagged"] is True
    assert data["category"] != "clean"

@pytest.mark.asyncio
async def test_check_test_clean():
    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/moderation/check",
            json={"text": "I love FastAPI , it is fantastic"}
        )
    assert response.status_code ==200
    assert response.json()["is_flagged"] is False

@pytest_asyncio.fixture(autouse=True)
async def cleanup_redis():
    yield
    # runs AFTER each test
    await redis_client.flushdb() # Clean up rate limit counters
    await redis_client.aclose()  # Close connection