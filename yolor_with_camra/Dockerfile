FROM nvcr.io/nvidia/pytorch:20.11-py3

LABEL title="yolor_camera" \
      version="1.0" \
      description="run YOLOR with camera"

RUN apt-get update && apt-get install -y \
  htop \
  libgl1-mesa-glx \
  screen \
  zip

RUN pip install \
  gdown \
  seaborn \
  thop

WORKDIR /workspace/src
RUN git clone https://github.com/WongKinYiu/yolor.git
RUN git clone https://github.com/fbcotter/pytorch_wavelets
RUN git clone https://github.com/JunnYu/mish-cuda

WORKDIR /workspace/src/yolor
RUN gdown 'https://drive.google.com/u/0/uc?id=1Tdn3yqpZ79X7R1Ql0zNlNScB1Dv9Fp76'
RUN gdown 'https://drive.google.com/u/0/uc?id=1UflcHlN5ERPdhahMivQYCbWWw7d2wY7U'

WORKDIR /workspace/src/pytorch_wavelets
RUN pip install .

WORKDIR /workspace/src/mish-cuda
RUN python setup.py build install

WORKDIR /workspace/src
