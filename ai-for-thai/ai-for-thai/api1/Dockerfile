# ใช้พิมพ์เขียว Python ฉบับทางการเป็นรากฐาน
FROM python:3.9-slim-buster

# ตั้งที่ตั้งการทำงานภายในเรือเหาะ
WORKDIR /app

# ติดตั้งเครื่องมือที่จำเป็น
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกสมบัติทั้งหมดลงในเรือเหาะ
COPY . /app

# เปิดช่องทางสื่อสารที่พอร์ต 5000 ให้โลกภายนอก
EXPOSE 5000

# คำสั่งที่จะเริ่มทำงานเมื่อเรือเหาะออกเดินทาง!
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
