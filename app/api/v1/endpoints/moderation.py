from fastapi import APIRouter,Depends,HTTPException,Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.moderation import ModerationRequest,ModerationResponse
from app.services.moderator import moderation_service
from app.db.session import get_db,redis_client

router = APIRouter()

@router.post("/check", response_model=ModerationResponse)
async def check_test(payload: ModerationRequest,
                     request: Request,
                     db: AsyncSession = Depends(get_db)):
    
    #rate limit 
    user_ip = request.client.host
    limit_key = f"rate_limit:{user_ip}"

    current_requests = await redis_client.incr(limit_key)

    if current_requests == 1:
        await redis_client.expire(limit_key,60)

    if current_requests > 5:
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please wait a minute"
        )

    
    result = await moderation_service.analyze_and_save(db, payload.text)
    return result
