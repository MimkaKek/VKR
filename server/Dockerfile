FROM python:3
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt
ENV FLASK_APP=/app/src/app.py
EXPOSE 5000
COPY . .
CMD [ "python3", "-m" , "flask", "--debug", "run", "--host=0.0.0.0"]