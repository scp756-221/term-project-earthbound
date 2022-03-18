FROM quay.io/bitnami/python:3.8.6-prod-debian-10-r81

WORKDIR /code

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY songs_list.py recommendation_model.py ./

#RUN mkdir -p /data
COPY model.pkl .
COPY song_info.csv .

EXPOSE 30003

CMD ["python", "songs_list.py", "30003"]
