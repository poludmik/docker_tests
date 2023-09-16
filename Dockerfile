# FROM nvidia/cuda:12.2.0-devel-ubuntu20.04
# WORKDIR /app
# COPY . .
# RUN apt-get update && DEBIAN_FRONTEND=noninteractive \
#     apt-get install -y software-properties-common && \
#     DEBIAN_FRONTEND=noninteractive add-apt-repository -y ppa:deadsnakes/ppa && \
#     apt-get install -y python3.10 curl && \
#     curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10

# RUN curl -sSL https://install.python-poetry.org | python3.10 - --preview
# RUN pip3 install --upgrade requests
# RUN ln -fs /usr/bin/python3.10 /usr/bin/python
# RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CMD ["python", "--version"]
# ENTRYPOINT ["python3", "main.py"]



# # Stage 1: Builder/Compiler
# FROM python:3.10-slim as builder

# # To install build-essential without interaction
# ARG DEBIAN_FRONTEND=noninteractive

# RUN apt update
# RUN apt-get install -y libpq-dev gcc && \
#     apt clean && rm -rf /var/lib/apt/lists/*
# COPY requirements.txt /requirements.txt

# # RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# RUN pip3 install -r requirements.txt


# # estep dos
# FROM nvidia/cuda:12.2.0-devel-ubuntu20.04

# ARG DEBIAN_FRONTEND=noninteractive

# RUN apt update
# RUN apt install --no-install-recommends -y build-essential software-properties-common
# RUN add-apt-repository -y ppa:deadsnakes/ppa 
# RUN apt install --no-install-recommends -y python3.10 python3-pip python3-setuptools python3-distutils python3-dev
# RUN apt-get install -y libpq-dev && \
#     apt clean && rm -rf /var/lib/apt/lists/*

# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# # make python3.10 default
# COPY --from=builder /root/.local/lib/python3.10/site-packages /usr/local/lib/python3.10/dist-packages

# # COPY all files to /folder in the container and make it WORKDIR
# COPY . /folder
# WORKDIR /folder

# # RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# # RUN pip3 install -r requirements.txt
# ENTRYPOINT ["python3", "src/app.py"]



# FROM ubuntu:22.04
FROM python:3.10

# RUN apt-get -y update
# RUN apt-get -y install software-properties-common
# RUN add-apt-repository -y ppa:deadsnakes/ppa
# RUN apt install -y python3.10
# RUN apt-get install -y python3-pip

COPY . /folder
WORKDIR /folder

# for linux
RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install -r requirements.txt

# ENTRYPOINT ["python3", "src/db_tests.py", "-docker"]
# ENTRYPOINT ["python3", "src/app.py", "--docker"]
ENTRYPOINT ["python3", "-m", "src", "--docker"]
# ENTRYPOINT [ "python3",  "src/nlp/process_search.py"]


# RUN CONTAINER:
# docker compose build --no-cache
# docker compose up