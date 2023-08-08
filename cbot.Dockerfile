FROM python:3.11

# Expose port you want your app on
EXPOSE 8080

# Upgrade pip and install requirements
COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install -r requirements.txt

# Copy app code and set working directory
COPY ../documentation-helper-1-starter documentation-helper-1-starter
#COPY app.py app.py
#COPY references references
WORKDIR .

# Run
ENTRYPOINT [“streamlit”, “run”, “main.py”, “–server.port=8080”, “–server.address=0.0.0.0”]