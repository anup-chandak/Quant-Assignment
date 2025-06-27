FROM python:3.9-slim-bullseye

RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "presenter.cli"]
CMD []
