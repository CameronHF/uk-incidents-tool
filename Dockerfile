FROM python:3.9
EXPOSE 8501
WORKDIR /project
COPY . .
RUN pip3 install -r requirements.txt
ENTRYPOINT ["streamlit", "run", "app/01_🏠_Home.py", "--server.port=8501"]