from fastapi import FastAPI, Request
import uvicorn # ผู้ดูแลอาณาจักร FastAPI ให้ทำงานอย่างราบรื่น!
import os

app = FastAPI()

PORT = int(os.environ.get('PORT', 5001))

@app.on_event("startup")
async def startup_event():
    print(f"API 2: ผู้คุมคลังข้อมูลตื่นขึ้นแล้ว ณ พอร์ต {PORT}!")

@app.get("/hello")
async def hello_world(request: Request):
    print(f"API 2: ได้รับคำขอ ณ '/hello' จาก {request.client.host}! กำลังส่งสารลับ 'สวัสดีจาก API 2!'")
    return {"message": "สวัสดีจาก API 2!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
