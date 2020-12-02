FROM python:3.7

EXPOSE 8001

WORKDIR /app
COPY . .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.gunicorn.txt
RUN pip uninstall -y apispec
RUN pip install apispec==3.2.0

CMD ["gunicorn", "server:app", "-b", "0.0.0.0:8001", "--worker-class", "aiohttp.GunicornWebWorker", "--log-level", "debug"]