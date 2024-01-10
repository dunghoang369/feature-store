FROM python:3.8-slim

# Copy app handler code
WORKDIR /app
COPY create_table.py create_table.py
COPY insert_table.py insert_table.py
COPY run.sh .
COPY .env .env
COPY configs ./configs
COPY requirements.txt requirements.txt
COPY postgresql_client.py postgresql_client.py
COPY main.sh main.sh
RUN apt-get update && apt-get install -y curl
RUN pip install -r requirements.txt
RUN chmod o+rwx ./run.sh
RUN chmod o+rwx ./main.sh

CMD [ "./main.sh"]