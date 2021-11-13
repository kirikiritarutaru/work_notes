# Dockerの作業メモ

## Get started

- 2021-11-11
- インストール

```bash
sudo apt-get remove docker docker-engine docker.io containerd runc
sudo apt-get update

sudo apt-get install ca-certificates curl gnupg lsb-release

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io

```



- Dockerのテストイメージ

```bash
sudo docker run hello-world
```

---

- 2021-11-13
- 毎回`sudo`をつけるのが面倒

> The docker daemon binds to a Unix socket instead of a TCP port. By  default that Unix socket is owned by the user root and other users can  access it with sudo. For this reason, docker daemon always runs as the  root user.
>
> To avoid having to use sudo when you use the docker command, create a Unix group called docker and add users to it. When the docker daemon  starts, it makes the ownership of the Unix socket read/writable by the  docker group.

- `docker` という名前のグループを作ってそこにユーザーを所属させればOK

```bash
# docker というグループがあるかチェック
cat /etc/group | grep docker
# なければ作る
sudo groupadd docker

sudo gpasswd -a $USER docker
sudo systemctl restart docker
```

- 上記実行後再ログイン

- コンテナ操作一覧

```bash
# 生成済みコンテナ一覧を表示
sudo docker container ls -a
# docker run 時にNAME指定
sudo docker run --name "hello-world-01" hello-world

# 結果をコンソール出力して実行（-it オプションによりterminal表示）
sudo docker run -it lukaszlach/merry-christmas
# デタッチドモードで実行（-d オプション）
sudo docker run -d lukaszlach/merry-christmas

# コンテナを停止
sudo docker stop [NAME]
sudo docker stop [UUID]

# 生成済みコンテナを起動
sudo docker start [NAME or UUID]
# terminal接続で起動
sudo docker start -a [NAME or UUID]

# 生成済みコンテナを削除
sudo docker rm [NAME]
#　起動していないコンテナを全て削除
sudo docker container prune

# docker image を一覧表示
sudo docker images
# docker image の削除
sudo docker rmi [REPOSITORY or IMAGE_ID]
# 起動していないimageの一括削除
sudo docker iamge prune --all
```



### docker image を作る

- 既存のimageをベースにライブラリなどを追加して自分のimageを作ることができる
- Dockerfileを作る
  - Dockerfileの例

```dockerfile
FROM continuumio/miniconda3

# conda create
RUN conda create -n chemodel python==3.7 

# install conda package
SHELL ["conda", "run", "-n", "chemodel", "/bin/bash", "-c"]
RUN conda install django=3.* -c conda-forge --override-channels
RUN conda install pytorch==1.7.1 torchvision==0.8.2 torchaudio==0.7.2 cpuonly -c pytorch -c conda-forge -c tboyer --override-channels 
RUN conda install -c rdkit -c conda-forge rdkit --override-channels

# install pip package
RUN pip3 install --upgrade pip
RUN pip3 install gunicorn
```

