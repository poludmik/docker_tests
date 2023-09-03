FROM python:latest

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . /folder
WORKDIR /folder

RUN pip3 install -r requirements.txt

# ENTRYPOINT ["python3", "src/db_tests.py", "-docker"]
ENTRYPOINT ["python3", "src/app.py"]



# RUN CONTAINER:
# docker compose build —no-cache
# docker compose up