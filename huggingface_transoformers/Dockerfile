FROM huggingface/transformers-pytorch-gpu

LABEL title="huggingface/transformers-pytorch-gpu" \
      version="1.0" \
      description="huggingface_transformers"

RUN apt-get update && apt-get install -y \
  python3-tk \
  git \
  vim

WORKDIR /workspace
COPY segformer_example.py /workspace/
