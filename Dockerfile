FROM python:3.9

WORKDIR /app

COPY . /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD alembic upgrade head && uvicorn main:app --host 0.0.0.0 --reload
