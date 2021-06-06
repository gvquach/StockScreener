FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7
COPY requirements.txt ./app /app/
RUN pip3 install -r requirements.txt