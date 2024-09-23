FROM python:3.12 

EXPOSE 80

WORKDIR /code

# Set evnironment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1 

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /code/

#CMD ["uvicorn", "main:app", "--host"]

CMD ["fastapi", "run", "main.py", "--port", "80"]
