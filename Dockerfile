FROM python:3.10
WORKDIR /usr/src/personalised_nudges
COPY ./src ./src
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
CMD ["uvicorn", "src.main:app","--reload", "--host", "0.0.0.0", "--port", "80"]