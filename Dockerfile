# FROM python:3.9 # We use a copied version of the `python` Docker image, because sometimes the CI/CD can't connect to Docker Hub.
FROM repo.tools-k8s.hellofresh.io/python:3.9

WORKDIR /project

# install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy source code explicitly
COPY app app/
COPY input input/
COPY sql sql/

# make Streamlit port available
EXPOSE 8501

# run Streamlit app
CMD streamlit run \
    --server.port 8501 \
    --server.enableCORS false \
    --server.enableXsrfProtection false \
    --server.enableWebsocketCompression false \
    app/01_home.py
