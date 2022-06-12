FROM pytorch/pytorch

LABEL title="sota_semantic_segmentation" \
      version="1.0" \
      description="Easy to use and customizable SOTA Semantic Segmentation models with abundant datasets in PyTorch"

RUN apt-get update && apt-get install -y \
  eog \
  git \
  vim

RUN pip install \
  gdown \
  coremltools \
  onnx \
  onnx-simplifier \
  onnxruntime

WORKDIR /workspace
RUN git clone https://github.com/sithu31296/semantic-segmentation

WORKDIR /workspace/semantic-segmentation
RUN pip install -e .

WORKDIR /workspace/semantic-segmentation/checkpoints/pretrained/segformer
RUN gdown 'https://drive.google.com/u/0/uc?id=18PN_P3ajcJi_5Q2v8b4BP9O4VdNCpt6m'
RUN gdown 'https://drive.google.com/u/0/uc?id=1AcgEK5aWMJzpe8tsfauqhragR0nBHyPh'
RUN gdown 'https://drive.google.com/u/0/uc?id=1-OmW3xRD3WAbJTzktPC-VMOF5WMsN8XT'

WORKDIR /workspace/semantic-segmentation/output/test_results
WORKDIR /workspace/semantic-segmentation
RUN python tools/export.py --cfg configs/ade20k.yaml

WORKDIR /workspace
