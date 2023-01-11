FROM rapidsai/rapidsai:22.12-cuda11.4-runtime-ubuntu20.04-py3.9

LABEL title="kaggle_env" \
      version="1.0" \
      description="Set Kaggle Env"

RUN apt-get update && apt-get upgrade -y

RUN source activate rapids
RUN pip install pytorch-lightning -U
RUN conda install -c conda-forge -y timm \
  faiss-gpu

WORKDIR /home/kaggle
