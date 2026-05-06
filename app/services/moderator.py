import torch 
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.moderation import ModerationLog
from detoxify import Detoxify
from app.db.session import redis_client
import json

torch.set_num_threads(1)

class ModerationService:
    def __init__(self):
        self.model = Detoxify('original')
    
    async def analyze_and_save(self, db: AsyncSession,text: str):
        #check redis cache
        cache_key = f"mod:{hash(text)}"
        cached_data = await redis_client.get(cache_key)

        if cached_data:
            print("--- CACHE HIT! ---")
            return json.loads(cached_data)


        #runn check
        results = self.model.predict(text)
        toxicity_score = float(results['toxicity'])
        is_flagged = toxicity_score > 0.5
        category=max(results, key=results.get) if is_flagged else "clean"

        new_log = ModerationLog(
            content=text,
            is_flagged=is_flagged,
            toxicity_score=toxicity_score,
            category=category
        )
        
        db.add(new_log)
        await db.commit()
        await db.refresh(new_log) # receive Id from Postgres

        # return new_log
        #save to redis
        result_dict ={
            "text":text,
            "is_flagged":is_flagged,
            "toxicity_score": toxicity_score,
            "category":category
        }
        
        await redis_client.set(cache_key, json.dumps(result_dict), ex=3600)
        
        print("--- CACHE MISS (Saved to Redis) ---")
        return result_dict


moderation_service = ModerationService()