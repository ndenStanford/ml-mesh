# Overview

A python core image with all OS container-level dependencies installed to make use of GPU support
for training and inference of pytorch-based models. Note that for GPU support, there is no docker
container level requirement outside of the standard torch library. All required drivers etc are
set up at the node level

# Node setup

We are using [the official AWS GPU **base** AMIs](https://aws.amazon.com/releasenotes/aws-deep-learning-base-ami-amazon-linux-2/
) to set up the node.

More specifically, while developing this core image we used
- AMI `ami-0cd6b97ad78d4c09e` and
- instance type `g4dn.xlarge` (e.g. Tesla GPUs)

An additional installation of the docker compose plugin was required to allow the running of the
`make` targets:

```
sudo systemctl stop docker
sudo systemctl stop docker.socket
sudo systemctl stop containerd
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo sed -i 's/$releasever/7/g' /etc/yum.repos.d/docker-ce.repo
sudo yum install -y docker-compose-plugin jq
sudo systemctl enable docker
sudo systemctl start docker
```

Running `nvidia-smi` generates the nvidia driver and CUDA specs overview, e.g.

```
(.venv) [ec2-user@ip-10-2-0-126 ml-mesh]$ nvidia-smi
Mon Jul 24 18:23:12 2023
+---------------------------------------------------------------------------------------+
| NVIDIA-SMI 535.54.03              Driver Version: 535.54.03    CUDA Version: 12.2     |
|-----------------------------------------+----------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |         Memory-Usage | GPU-Util  Compute M. |
|                                         |                      |               MIG M. |
|=========================================+======================+======================|
|   0  Tesla T4                       On  | 00000000:00:1E.0 Off |                    0 |
| N/A   33C    P8               9W /  70W |      0MiB / 15360MiB |      0%      Default |
|                                         |                      |                  N/A |
+-----------------------------------------+----------------------+----------------------+

+---------------------------------------------------------------------------------------+
| Processes:                                                                            |
|  GPU   GI   CI        PID   Type   Process name                            GPU Memory |
|        ID   ID                                                             Usage      |
|=======================================================================================|
|  No running processes found                                                           |
+---------------------------------------------------------------------------------------+
```
