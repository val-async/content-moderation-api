from sqlalchemy.ext.asyncio import AsyncSession
from app.models.moderation import ModerationLog

class ModerationService:
    def __init__(self):
        self.forbidden_words = ["spam","scam","badword"]
    
    async def analyze_and_save(self, db: AsyncSession,text: str):
        is_flagged = any(word in text.lower() for word in self.forbidden_words)
        toxicity_score = 0.95 if is_flagged else 0.05
        category = "toxic" if is_flagged else "clean"
        # return {
        #     "is_flagged": is_flagged,
        #     "toxicity_score": 0.95 if is_flagged else 0.05,
        #     "category": "toxic" if is_flagged else "clean"
        # }
        new_log = ModerationLog(
            content=text,
            is_flagged=is_flagged,
            toxicity_score=toxicity_score,
            category=category
        )
        
        db.add(new_log)
        await db.commit()
        await db.refresh(new_log) # receive Id from Postgres

        return new_log

moderation_service = ModerationService()