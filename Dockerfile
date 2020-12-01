FROM python:3.7

EXPOSE 8000

WORKDIR /app
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.gunicorn.txt
RUN pip uninstall -y apispec
RUN pip install apispec==3.2.0

CMD ["gunicorn", "server:app", "--bind", "0.0.0.0:8000", "--worker-class", "aiohttp.GunicornWebWorker"]