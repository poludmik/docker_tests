FROM python:3.10

# RUN apt-get -y update
# RUN apt-get -y install software-properties-common
# RUN add-apt-repository -y ppa:deadsnakes/ppa
# RUN apt install -y python3.10
# RUN apt-get install -y python3-pip

ENV AM_I_IN_A_DOCKER_CONTAINER Yes

COPY . /folder
WORKDIR /folder

# No cuda for macos, torch will be installed in sentence-transformers
# RUN pip3 install torch torchvision torchaudio; 
RUN pip3 install -r requirements.txt

ENTRYPOINT ["python3", "-m", "src"]

# RUN CONTAINER:
# docker compose -f docker-compose-macos.yml build --no-cache
# docker compose up -d

# Another possibility
# chmod +x docker_compose_build.sh # make the script executable