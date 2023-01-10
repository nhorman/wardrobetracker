FROM python:3.10-slim

EXPOSE 8501

WORKDIR /app

RUN apt-get update && apt-get install -y \
	build-essential \
	software-properties-common \
	git \
	mariadb-client \
	&& rm -rf /var/lib/apt/lists

ADD requirements.txt .
ADD index.py .
ADD start-streamlit.sh .
ADD createdb.sql .
RUN mkdir -p /app/.streamlit/
ADD secrets.toml ./.streamlit/secrets.toml

RUN pip3 install -r requirements.txt
ENV PATH "$PATH:/app"
RUN chmod 755 /app/start-streamlit.sh

ENTRYPOINT ["start-streamlit.sh"]
