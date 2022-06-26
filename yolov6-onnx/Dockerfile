FROM nvidia/cuda:11.4.2-cudnn8-runtime-ubuntu20.04

LABEL title="yolov6_onnx" \
      version="1.0" \
      description="run YOLOv6 by onnxruntime-gpu with camera"

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y tzdata
ENV TZ=Asia/Tokyo

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  git \
  python3 \
  python3-pip \
  xvfb \
  libgl1-mesa-dev \
  libglib2.0-0

RUN pip3 install \
  opencv-python \
  imread-from-url \
  onnxruntime-gpu

WORKDIR /workspace/src
RUN git clone https://github.com/ibaiGorordo/ONNX-YOLOv6-Object-Detection.git

WORKDIR /workspace/src
