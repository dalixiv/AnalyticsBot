FROM python:3.9

ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /app:${PYTHONPATH}

# Install requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt

# Copy service sources
WORKDIR /usr/src
COPY app app

CMD [ "python", "-m", "app" ]
