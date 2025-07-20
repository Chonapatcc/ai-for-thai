from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
import httpx # นักเดินทางผู้รวดเร็วสำหรับภารกิจ HTTP แบบ Asynchronous!
import os
import uvicorn # ผู้ดูแลอาณาจักร FastAPI ให้ทำงานอย่างราบรื่น!

app = FastAPI()

# พลังงานลับสำหรับเรียกหา API 2!
API2_URL = os.environ.get('API2_URL', 'http://api2:5001/hello') 
PORT = int(os.environ.get('PORT', 5000))

@app.on_event("startup")
async def startup_event():
    print(f"API 1: ประตูมิติเปิดออกแล้ว ณ พอร์ต {PORT}! พลังแห่ง API 2 เชื่อมต่ออยู่ที่ {API2_URL}")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print(f"API 1: ได้รับคำขอจากนักผจญภัยท่านหนึ่ง ณ '/' จาก {request.client.host}")
    return """
    <html>
        <head>
            <title>ประตูมิติ API 1</title>
        </head>
        <body>
            <h1>สวัสดีจาก API 1! จงกล้าหาญพอที่จะไปที่ <a href="/proxy-hello">/proxy-hello</a> เพื่อปลดล็อกข้อความจาก API 2!</h1>
        </body>
    </html>
    """

@app.get("/proxy-hello")
async def proxy_hello(request: Request):
    print(f"API 1: ได้รับคำขอ ณ '/proxy-hello' จาก {request.client.host}! กำลังส่งสารไปยัง API 2...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(API2_URL)
            response.raise_for_status()  # หากมีสิ่งผิดปกติเกิดขึ้น จงบอกข้ามา!
            api2_response = response.text
            print(f"API 1: ได้รับสารลับจาก API 2 แล้ว: '{api2_response}'")
            return {"message": f"สารลับจาก API 2 ผ่านทาง API 1: {api2_response}"}
        except httpx.ConnectError as e:
            print(f"API 1: ไม่สามารถเชื่อมต่อกับ API 2 ที่ {API2_URL} ได้! ข้อผิดพลาด: {e}")
            raise HTTPException(status_code=500, detail="ไม่สามารถติดต่อกับผู้คุมคลังข้อมูลได้!")
        except httpx.HTTPStatusError as e:
            print(f"API 1: เกิดข้อผิดพลาด HTTP จาก API 2: {e.response.status_code} - {e.response.text}")
            raise HTTPException(status_code=500, detail=f"เกิดความผิดปกติในการสื่อสารกับ API 2: {e.response.text}")
        except httpx.RequestError as e:
            print(f"API 1: เกิดข้อผิดพลาดที่ไม่คาดคิดระหว่างส่งสารไปยัง API 2: {e}")
            raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาดที่ไม่คาดคิด: {e}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)
