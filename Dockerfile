FROM python:3.10.14
WORKDIR /usr/src/personalised_nudges
COPY ./src ./src
COPY requirements.txt requirements.txt
RUN pip install --default-timeout=1000 --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm
CMD ["uvicorn", "src.main:app","--reload", "--host", "0.0.0.0", "--port", "80"]