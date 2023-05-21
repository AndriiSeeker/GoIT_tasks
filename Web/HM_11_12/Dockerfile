FROM python:3.10
RUN apt update
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["uvicorn", "main:app", "--reload"]