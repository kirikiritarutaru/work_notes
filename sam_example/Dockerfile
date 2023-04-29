FROM nvcr.io/nvidia/pytorch:20.11-py3

LABEL title="sam_example" \
      version="1.0" \
      description="run SAM"

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  libgl1-mesa-dev \
  libglib2.0-0

WORKDIR /workspace/src
RUN git clone https://github.com/facebookresearch/segment-anything.git
WORKDIR /workspace/src/segment-anything
RUN pip install -e .
RUN pip install opencv-python pycocotools matplotlib onnxruntime onnx

WORKDIR /workspace/src/segment-anything/models
RUN wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth

WORKDIR /workspace/src/segment-anything
