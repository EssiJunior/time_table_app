FROM python:3.9.4

WORKDIR /Desktop/FastAPI_2/application

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn","application.main:app","--host","0.0.0.0","--port","8000"]