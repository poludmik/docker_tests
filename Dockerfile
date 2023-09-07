# FROM ubuntu:22.04
FROM python:latest

# RUN apt-get -y update
# RUN apt-get -y install software-properties-common
# RUN add-apt-repository -y ppa:deadsnakes/ppa
# RUN apt install -y python3.10
# RUN apt-get install -y python3-pip

# ENV VIRTUAL_ENV=/opt/venv
# RUN python3 -m venv $VIRTUAL_ENV
# ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY . /folder
WORKDIR /folder

# for linux
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -r requirements.txt

# ENTRYPOINT ["python3", "src/db_tests.py", "-docker"]
ENTRYPOINT ["python3", "src/app.py"]
# ENTRYPOINT [ "python3",  "src/nlp/process_search.py"]


# RUN CONTAINER:
# docker compose build --no-cache
# docker compose up