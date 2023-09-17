## Use CUDA in docker container

* Enable WSL based engine in Docker Desktop
* In WSL console follow https://saturncloud.io/blog/how-to-install-pytorch-on-the-gpu-with-docker/
* In case of faulty **systemd** write 2 lines as described [here](https://devblogs.microsoft.com/commandline/systemd-support-is-now-available-in-wsl/)
* "Failed to start docker.service: Unit not found.": I installed unofficial docker.io, did systemctl, uninstalled it, rebooted everything and it worked :thumbsup:
* Write --gpu all compromise to docker-compose.yml
* Test with:
```console
docker run --rm -it --gpus=all nvcr.io/nvidia/k8s/cuda-sample:nbody nbody -gpu -benchmark
```

* If docker can't find some credentials on WSL, then nano ~/.docker/config.json and chacnge creds to cred