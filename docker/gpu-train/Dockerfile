FROM 063759612765.dkr.ecr.us-east-1.amazonaws.com/gpu-base:seb-test as base

ARG IMAGE_NAME=gpu-train

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

# LABEL maintainer="Amazon AI"
# LABEL dlc_major_version="1"
ENV HOME="docker/${IMAGE_NAME}"

ARG RMM_VERSION=0.15.0

# The smdebug pipeline relies for following format to perform string replace and trigger DLC pipeline for validating
# the nightly builds. Therefore, while updating the smdebug version, please ensure that the format is not disturbed.
ARG SMDEBUG_VERSION=1.0.24

ENV SAGEMAKER_TRAINING_MODULE=sagemaker_pytorch_container.training:main

# Install AWS-PyTorch and other torch packages
RUN pip uninstall -y torch torchvision torchaudio torchdata \
 && pip install --no-cache-dir -U ${PT_SM_TRAINING_URL} ${PT_TORCHVISION_URL} ${PT_TORCHAUDIO_URL} ${PT_TORCHDATA_URL} torchnet

# Install Nvidia Apex
## Pin apex commit requested by sm-model-parallel team
RUN git clone https://github.com/NVIDIA/apex && \
    cd apex && \
    git checkout aa756ce && \
    pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

# Configure Open MPI and configure NCCL parameters
RUN mv $OPEN_MPI_PATH/bin/mpirun $OPEN_MPI_PATH/bin/mpirun.real \
 && echo '#!/bin/bash' > $OPEN_MPI_PATH/bin/mpirun \
 && echo "${OPEN_MPI_PATH}/bin/mpirun.real --allow-run-as-root \"\$@\"" >> $OPEN_MPI_PATH/bin/mpirun \
 && chmod a+x $OPEN_MPI_PATH/bin/mpirun \
 && echo "hwloc_base_binding_policy = none" >> $OPEN_MPI_PATH/etc/openmpi-mca-params.conf \
 && echo "rmaps_base_mapping_policy = slot" >> $OPEN_MPI_PATH/etc/openmpi-mca-params.conf \
 && echo NCCL_DEBUG=INFO >> /etc/nccl.conf \
 && echo NCCL_SOCKET_IFNAME=^docker0 >> /etc/nccl.conf

# Install AWS OFI NCCL plug-in
RUN apt-get update && apt-get install -y autoconf
RUN mkdir /tmp/efa-ofi-nccl \
 && cd /tmp/efa-ofi-nccl \
 && git clone https://github.com/aws/aws-ofi-nccl.git -b v${BRANCH_OFI} \
 && cd aws-ofi-nccl \
 && ./autogen.sh \
 && ./configure --with-libfabric=/opt/amazon/efa \
  --with-mpi=/opt/amazon/openmpi \
  --with-cuda=/usr/local/cuda \
  --with-nccl=/usr/local --prefix=/usr/local \
 && make \
 && make install \
 && rm -rf /tmp/efa-ofi-nccl \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# Install OpenSSH for MPI to communicate between containers, allow OpenSSH to talk to containers without asking for confirmation
RUN apt-get update \
 && apt-get install -y  --allow-downgrades --allow-change-held-packages --no-install-recommends \
 && apt-get install -y --no-install-recommends openssh-client openssh-server \
 && mkdir -p /var/run/sshd \
 && cat /etc/ssh/ssh_config | grep -v StrictHostKeyChecking > /etc/ssh/ssh_config.new \
 && echo "    StrictHostKeyChecking no" >> /etc/ssh/ssh_config.new \
 && mv /etc/ssh/ssh_config.new /etc/ssh/ssh_config \
 && rm -rf /var/lib/apt/lists/* \
 && apt-get clean

# Configure OpenSSH so that nodes can communicate with each other
RUN mkdir -p /var/run/sshd && \
 sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

RUN rm -rf /root/.ssh/ && \
 mkdir -p /root/.ssh/ && \
 ssh-keygen -q -t rsa -N '' -f /root/.ssh/id_rsa && \
 cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys \
 && printf "Host *\n StrictHostKeyChecking no\n" >> /root/.ssh/config

# Install Horovod
RUN pip uninstall -y horovod \
 && ldconfig /usr/local/cuda-11.3/targets/x86_64-linux/lib/stubs \
 && HOROVOD_GPU_ALLREDUCE=NCCL HOROVOD_CUDA_HOME=/usr/local/cuda-11.3 HOROVOD_WITH_PYTORCH=1 pip install --no-cache-dir horovod==${HOROVOD_VERSION} \
 && ldconfig

# Install PT S3 plugin
RUN pip install --no-cache-dir -U ${PT_S3_WHL_GPU}
RUN mkdir -p /etc/pki/tls/certs && cp /etc/ssl/certs/ca-certificates.crt /etc/pki/tls/certs/ca-bundle.crt

WORKDIR /

# Install scikit-learn and pandas
RUN /opt/conda/bin/conda install -y -c conda-forge \
    scikit-learn \
    pandas

WORKDIR /

# Install libboost from source. This package is needed for smdataparallel functionality [for networking asynchronous IO].
RUN wget https://sourceforge.net/projects/boost/files/boost/1.73.0/boost_1_73_0.tar.gz/download -O boost_1_73_0.tar.gz \
 && tar -xzf boost_1_73_0.tar.gz \
 && cd boost_1_73_0 \
 && ./bootstrap.sh \
 && ./b2 threading=multi --prefix=/opt/conda -j 64 cxxflags=-fPIC cflags=-fPIC install || true \
 && cd .. \
 && rm -rf boost_1_73_0.tar.gz \
 && rm -rf boost_1_73_0 \
 && cd /opt/conda/include/boost

WORKDIR /opt/pytorch

# Copy workaround script for incorrect hostname
RUN pwd
COPY ${HOME}/changehostname.c /
COPY ${HOME}/start_with_right_hostname.sh /usr/local/bin/start_with_right_hostname.sh

RUN chmod +x /usr/local/bin/start_with_right_hostname.sh

WORKDIR /root

# Install sagemaker
RUN pip install --no-cache-dir -U \
    # disable smdebug pip install until available stable smdebug releases
    # smdebug==${SMDEBUG_VERSION} \
    smclarify \
    "sagemaker>=2,<3" \
    sagemaker-experiments==0.* \
    sagemaker-pytorch-training

# Install sagemaker debugger smdebug from souce
RUN cd /tmp \
  && git clone -b master --single-branch https://github.com/awslabs/sagemaker-debugger.git \
  && cd sagemaker-debugger \
  # pin the debugger to the numpy deprecation fix
  && git checkout -f 9764a221fd3086ad8d2736128ccc2d69f269df1c \
  && python setup.py install \
  && rm -rf /tmp/*

# Install extra packages
# numba 0.54 only works with numpy>=1.20. See https://github.com/numba/numba/issues/7339
RUN pip install --no-cache-dir -U \
    "bokeh>=2.3,<3" \
    "imageio>=2.9,<3" \
    "opencv-python>=4.3,<5" \
    "plotly>=5.1,<6" \
    "seaborn>=0.11,<1" \
    "numba<0.54"

# Install RAPIDSMemoryManager.
# Requires cmake>=3.14.
RUN  wget -nv https://github.com/rapidsai/rmm/archive/v${RMM_VERSION}.tar.gz \
 && tar -xvf v${RMM_VERSION}.tar.gz \
 && cd rmm-${RMM_VERSION} \
 && INSTALL_PREFIX=/usr/local ./build.sh librmm \
 && cd .. \
 && rm -rf v${RMM_VERSION}.tar* \
 && rm -rf rmm-${RMM_VERSION}

# Install ZeRO-2D Binary
RUN pip install --no-cache-dir -U ${ZERO_2D_URL}

# Install flash attention
WORKDIR /flash
RUN git clone https://github.com/HazyResearch/flash-attention.git \
    && cd flash-attention \
    && git checkout ${FLASH_ATTENTION_VERSION} \
    && python setup.py install \
    && rm -rf /flash

WORKDIR /

# Install SM Distributed Modelparallel binary
RUN pip install --no-cache-dir -U ${SMD_MODEL_PARALLEL_URL}

# Install SM Distributed DataParallel binary
RUN SMDATAPARALLEL_PT=1 pip install --no-cache-dir ${SMD_DATA_PARALLEL_URL}

ENV LD_LIBRARY_PATH="/opt/conda/lib/python${PYTHON_SHORT_VERSION}/site-packages/smdistributed/dataparallel/lib:$LD_LIBRARY_PATH"

WORKDIR /

RUN HOME_DIR=/root \
 && curl -o ${HOME_DIR}/oss_compliance.zip https://aws-dlinfra-utilities.s3.amazonaws.com/oss_compliance.zip \
 && unzip ${HOME_DIR}/oss_compliance.zip -d ${HOME_DIR}/ \
 && cp ${HOME_DIR}/oss_compliance/test/testOSSCompliance /usr/local/bin/testOSSCompliance \
 && chmod +x /usr/local/bin/testOSSCompliance \
 && chmod +x ${HOME_DIR}/oss_compliance/generate_oss_compliance.sh \
 && ${HOME_DIR}/oss_compliance/generate_oss_compliance.sh ${HOME_DIR} ${PYTHON} \
 && rm -rf ${HOME_DIR}/oss_compliance* \
 && rm -rf /tmp/tmp*

# Removing the cache as it is needed for security verification
RUN rm -rf /root/.cache | true

ENTRYPOINT ["bash", "-m", "start_with_right_hostname.sh"]
CMD ["/bin/bash"]

FROM base as production

FROM base as development
