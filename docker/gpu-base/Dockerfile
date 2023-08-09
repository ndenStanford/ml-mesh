FROM nvidia/cuda:11.3.1-base-ubuntu20.04 AS base

ARG IMAGE_NAME=gpu-base

# taken from: https://github.com/aws/deep-learning-containers/pytorch/training/docker/1.12/py3/cu113/Dockerfile.gpu
ARG PYTHON=python3
ARG PYTHON_VERSION=3.8.16
ARG PYTHON_SHORT_VERSION=3.8
ARG MAMBA_VERSION=22.11.1-2

# PyTorch Binaries
ARG PT_EC2_TRAINING_URL=https://aws-pytorch-unified-cicd-binaries.s3.us-west-2.amazonaws.com/r1.12.1_ec2/20221208-233710/d3dae914337cde7e182d28544aed5efce29255c4/torch-1.12.1%2Bcu113-cp38-cp38-linux_x86_64.whl
ARG PT_SM_TRAINING_URL=https://aws-pytorch-unified-cicd-binaries.s3.us-west-2.amazonaws.com/r1.12.1_sm/20230106-042344/626f1a6ec58817e524705e0917dbab97c81b440e/torch-1.12.1%2Bcu113-cp38-cp38-linux_x86_64.whl
ARG PT_TORCHVISION_URL=https://download.pytorch.org/whl/cu113/torchvision-0.13.1%2Bcu113-cp38-cp38-linux_x86_64.whl
ARG PT_TORCHAUDIO_URL=https://download.pytorch.org/whl/cu113/torchaudio-0.12.1%2Bcu113-cp38-cp38-linux_x86_64.whl
ARG PT_TORCHDATA_URL=https://download.pytorch.org/whl/test/torchdata-0.4.1-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl
ARG PT_S3_WHL_GPU=https://aws-s3-plugin.s3.us-west-2.amazonaws.com/binaries/0.0.1/1c3e69e/awsio-0.0.1-cp38-cp38-manylinux1_x86_64.whl

# SMD model parallel and data parallel binaries
ARG SMD_DATA_PARALLEL_URL=https://smdataparallel.s3.amazonaws.com/binary/pytorch/1.12.1/cu113/2022-12-05/smdistributed_dataparallel-1.6.0-cp38-cp38-linux_x86_64.whl
ARG SMD_MODEL_PARALLEL_URL=https://sagemaker-distributed-model-parallel.s3.us-west-2.amazonaws.com/pytorch-1.12.1/build-artifacts/2022-12-08-21-34/smdistributed_modelparallel-1.13.0-cp38-cp38-linux_x86_64.whl

# ZeRO-2D Binary
ARG ZERO_2D_URL=https://aws-deepspeed-zero-2d-binaries.s3.us-west-2.amazonaws.com/r1.12.1/20221203-014851/b3d766ee27e7fa0e9b078665273a9550768445e7/deepspeed-0.6.1%2Bb3d766e-py3-none-any.whl

# Flash Attention version installed from source
# TODO: This version needs to be updated to GitHub Tags or replaced with installation from pypi/conda releases
ARG FLASH_ATTENTION_VERSION=1d0b41be3b0fa759502e274779db6758617fc7b9

ENV DEBIAN_FRONTEND=noninteractive \
    LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:/usr/local/lib"

RUN apt-get update \
 && apt-get upgrade -y \
 && apt-get autoremove -y \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

ARG CUBLAS_VERSION=11.5.1.109
ARG EFA_PATH=/opt/amazon/efa
ARG CUDA_HOME=/usr/local/cuda

# This arg required to stop docker build waiting for region configuration while installing tz data from ubuntu 20
ARG DEBIAN_FRONTEND=noninteractive

# Python won’t try to write .pyc or .pyo files on the import of source modules
# Force stdin, stdout and stderr to be totally unbuffered. Good for logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LD_LIBRARY_PATH="/usr/local/lib:${LD_LIBRARY_PATH}"
ENV LD_LIBRARY_PATH="/opt/conda/lib:${LD_LIBRARY_PATH}"
ENV PYTHONIOENCODING=UTF-8
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH
ENV TORCH_CUDA_ARCH_LIST="3.7 5.0 7.0+PTX 8.0"
ENV TORCH_NVCC_FLAGS="-Xfatbin -compress-all"

ENV CUDNN_VERSION=8.2.0.53
ENV NCCL_VERSION=2.10.3
ENV HOROVOD_VERSION=0.24.3
ENV EFA_VERSION=1.15.1
ENV OMPI_VERSION=4.1.1
ENV BRANCH_OFI=1.3.0-aws

ENV CMAKE_PREFIX_PATH="$(dirname $(which conda))/../"
ENV OPEN_MPI_PATH=/opt/amazon/openmpi

ENV DGLBACKEND=pytorch
ENV MANUAL_BUILD=0
ENV RDMAV_FORK_SAFE=1
ENV DLC_CONTAINER_TYPE=training

RUN apt-get update \
 # TODO: Remove systemd upgrade once it is updated in base image
 && apt-get -y upgrade --only-upgrade systemd \
 && apt-get install -y --allow-change-held-packages --no-install-recommends \
    build-essential \
    ca-certificates \
    cmake \
    cuda-command-line-tools-11-3 \
    cuda-cudart-11-3 \
    cuda-libraries-11-3 \
    curl \
    emacs \
    git \
    hwloc \
    jq \
    libcublas-11-3=${CUBLAS_VERSION}-1 \
    libcublas-dev-11-3=${CUBLAS_VERSION}-1 \
    libcudnn8=$CUDNN_VERSION-1+cuda11.3 \
    libcufft-dev-11-3 \
    libcurand-dev-11-3 \
    libcurl4-openssl-dev \
    libcusolver-dev-11-3 \
    libcusparse-dev-11-3 \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    libibverbs-dev \
    libhwloc-dev \
    libnuma1 \
    libnuma-dev \
    libssl1.1 \
    libssl-dev \
    libtool \
    openssl \
    python3-dev \
    unzip \
    vim \
    wget \
    zlib1g-dev \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# Install NCCL
RUN cd /tmp \
 && git clone https://github.com/NVIDIA/nccl.git -b v${NCCL_VERSION}-1 \
 && cd nccl \
 && make -j64 src.build BUILDDIR=/usr/local \
 && rm -rf /tmp/nccl

# Install EFA alone without AWS OPEN_MPI
RUN mkdir /tmp/efa \
 && cd /tmp/efa \
 && curl -O https://s3-us-west-2.amazonaws.com/aws-efa-installer/aws-efa-installer-${EFA_VERSION}.tar.gz \
 && tar -xf aws-efa-installer-${EFA_VERSION}.tar.gz \
 && cd aws-efa-installer \
 && apt-get update \
 && ./efa_installer.sh -y --skip-kmod -g \
 && rm -rf $OPEN_MPI_PATH \
 && rm -rf /tmp/efa \
 && rm -rf /tmp/aws-efa-installer-${EFA_VERSION}.tar.gz \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# Install OpenMPI without libfabric support
RUN mkdir /tmp/openmpi \
 && cd /tmp/openmpi \
 && wget --quiet https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-${OMPI_VERSION}.tar.gz \
 && tar zxf openmpi-${OMPI_VERSION}.tar.gz \
 && cd openmpi-${OMPI_VERSION} \
 && ./configure --enable-orterun-prefix-by-default --prefix=$OPEN_MPI_PATH --with-cuda \
 && make -j $(nproc) all \
 && make install \
 && ldconfig \
 && cd / \
 && rm -rf /tmp/openmpi

ENV PATH="$OPEN_MPI_PATH/bin:$PATH"
ENV LD_LIBRARY_PATH=$OPEN_MPI_PATH/lib/:$EFA_PATH/lib/:$LD_LIBRARY_PATH


RUN ompi_info --parsable --all | grep mpi_built_with_cuda_support:value \
 && curl -L -o ~/mambaforge.sh https://github.com/conda-forge/miniforge/releases/download/${MAMBA_VERSION}/Mambaforge-${MAMBA_VERSION}-Linux-x86_64.sh \
 && chmod +x ~/mambaforge.sh \
 && ~/mambaforge.sh -b -p /opt/conda \
 && rm ~/mambaforge.sh \
 && /opt/conda/bin/conda install -c conda-forge \
    python=$PYTHON_VERSION \
    cython \
    mkl \
    mkl-include \
    parso \
    typing \
    h5py \
    requests \
    "pyopenssl>=17.5.0" \
    libgcc \
    # Below 2 are included in miniconda base, but not mamba so need to install
    conda-content-trust \
    charset-normalizer \
    "shap<1" \
 # pin dgl since PyTorch 1.12 has accurancy error with 1.0.0
 && /opt/conda/bin/conda install -c dglteam -y dgl-cuda11.3=0.9.1 \
 && /opt/conda/bin/conda install -c pytorch magma-cuda113 \
 # Upstream conda looks to have moved to 4.13 which is incompatible with mamba 0.22.1 and will fail the conda-forge installs.
 # having "conda update conda" before the "conda -c conda-forge" commands will automatically update conda to 4.13.
 # Moving conda update conda" after the "conda -c conda-forge" commands keep conda at 4.12 but will update other packages using
 # the current conda 4.12
 && /opt/conda/bin/conda update conda \
 && /opt/conda/bin/conda clean -ya

# Conda installs links for libtinfo.so.6 and libtinfo.so.6.2 both
# Which causes "/opt/conda/lib/libtinfo.so.6: no version information available" warning
# Removing link for libtinfo.so.6. This change is needed only for ubuntu 20.04-conda, and can be reverted
# once conda fixes the issue
RUN rm -rf /opt/conda/lib/libtinfo.so.6

RUN /opt/conda/bin/conda config --set ssl_verify False \
 && pip install --upgrade pip --trusted-host pypi.org --trusted-host files.pythonhosted.org \
 && ln -s /opt/conda/bin/pip /usr/local/bin/pip3

WORKDIR /root

RUN pip install --no-cache-dir -U \
    "awscli<2" \
    boto3 \
    click \
    cmake==3.18.2.post1 \
    "cryptography>3.2" \
    ipython \
    mpi4py==3.1.3 \
    opencv-python \
    packaging \
    "Pillow>=9.0.0" \
    psutil \
    pybind11 \
    "pyyaml>=5.4,<5.5"

COPY docker/${IMAGE_NAME}/deep_learning_container.py /usr/local/bin/deep_learning_container.py

RUN chmod +x /usr/local/bin/deep_learning_container.py

RUN curl -o /license.txt  https://aws-dlc-licenses.s3.amazonaws.com/pytorch-1.12/license.txt

FROM base as production

FROM base as development
