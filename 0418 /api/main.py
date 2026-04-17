import uuid #중복없는 문자열 만들어주는.
import json

from fastapi import FastAPI, Body
from fastapi.responses import StreamingResponse
# from sqlalchemy import text
from redis  import asyncio as aredis

# from connection import SessionFactory

redis_client = aredis.from_url("redis://redis:6379", decode_responses=True)

app = FastAPI()

# @app.get("/health-check")
# def health_check_handler():
#     with SessionFactory() as session:
#         stmt = text("SELECT * FROM user LIMIT 1;")
#         row = session.execute(stmt).fetchone()
#     return {"user": row._asdict()}

@app.post("/chats")
async def generate_chat_handler(
    user_input: str = Body(..., embed=True)
,):
    #1) 요청 본문 : user_input
    #2) SUBSCRIBE 채널 (대기 중...)
    channel = str(uuid.uuid4())

    pubsub = redis_client.pubsub()
    await pubsub.subscribe(channel)

    #3) Queue를 통해서 worker에 job을 전달한다(enqueue)
    # LPUSH queue 
    task = {"channel":channel,"user_input": user_input}
    await redis_client.lpush("queue", json.dumps(task))

    #4) 채널에서 메시지 읽기(대기)
    async def event_generator():
        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            token = message["data"]
            if token == "[DONE]":
                break
            yield token # data

        await pubsub.unsubscribe(channel)
        await pubsub.close()
    #5) 결과 수신
    return StreamingResponse(
        event_generator(),
        media_type = "text/event-stream",
    )
