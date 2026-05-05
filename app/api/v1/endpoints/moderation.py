from fastapi import APIRouter,Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.moderation import ModerationRequest,ModerationResponse
from app.services.moderator import moderation_service
from app.db.session import get_db

router = APIRouter()

@router.post("/check", response_model=ModerationResponse)
async def check_test(payload: ModerationRequest,
                     db: AsyncSession = Depends(get_db)):
    
    result = await moderation_service.analyze_and_save(db, payload.text)

    return {
        "text": result.content,
        "is_flagged": result.is_flagged,
        "toxicity_score": result.toxicity_score,
        "category": result.category
    }
