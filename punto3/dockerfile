FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY main.py database.py models.py schemas.py s3_service.py ./

CMD ["main.handler"]