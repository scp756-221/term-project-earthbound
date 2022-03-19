FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /code

COPY requirements.txt model.pkl recommendation_model.py song_info.csv .

RUN pip install --no-cache-dir -r requirements.txt

COPY songs_list.py .
EXPOSE 30003

CMD ["python", "songs_list.py", "30003"]
