FROM nvcr.io/nvidia/pytorch:20.11-py3

LABEL title="alike_example" \
      version="1.0" \
      description="run ALIKE with camera"

RUN apt-get update && apt-get upgrade -y && apt-get install -y \
  libgl1-mesa-dev \
  libglib2.0-0

WORKDIR /workspace/src
RUN git clone https://github.com/Shiaoming/ALIKE.git

WORKDIR /workspace/src/ALIKE
