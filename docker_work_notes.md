# Dockerの作業メモ

## Get started

### インストール

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

---

## 基本操作

### イメージ操作一覧

```bash
# docker image を一覧表示
docker images
# docker image の削除
docker rmi [REPOSITORY or IMAGE_ID]
# 起動していないimageの一括削除
docker iamge prune --all
```



### コンテナ操作一覧

```bash
# 生成済みコンテナ一覧を表示
docker container ls -a
# docker run 時にNAME指定
docker run --name "hello-world-01" hello-world

# 結果をコンソール出力して実行（-it オプションによりterminal表示）
docker run -it lukaszlach/merry-christmas
# デタッチドモードで実行（-d オプション）
docker run -d lukaszlach/merry-christmas

# コンテナを停止
docker stop [NAME or UUID]

# 生成済みコンテナを起動
docker start [NAME or UUID]
# terminal接続で起動
docker start -a [NAME or UUID]

# 生成済みコンテナを削除
docker rm [NAME]
#　起動していないコンテナを全て削除
docker container prune

# 起動中コンテナへ接続
docker container attach [NAME or UUID]
# exitで抜ける
exit
# exitで抜けるとSTATUSがExitedになる
# 起動したまま抜けるには Ctrl+Q+P

# コンテナ名の変更
docker container rename [変更前NAME] [変更後NAME]

# コンテナとホストOS間でファイルとディレクトリのコピー
# 以下では、コンテナ[CONTAINER ID]の/etc/passwdファイルをホストの/tmpディレクトリに移動している
docker container cp [CONTAINER ID:/etc/passwd] /tmp

# Dockerイメージが生成されてからの差分を表示
# A:ファイル追加、C:ファイル更新、D:ファイル削除
docker container diff [NAME or UUID]

# コンテナからイメージを作成
docker container commit [NAME or UUID] [イメージ名]
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

- Dockerfile

  - 一言でいうと、「コンテナの構成情報を定義したファイル」

  - Dockerfileを用意すれば何回もDockerコマンドを叩く必要なく、1コマンドでDockerイメージを生成できる

  - [Dockerfileのベストプラクティス](http://docs.docker.jp/engine/articles/dockerfile_best-practice.html)

    - `RUN`命令はバックスラッシュを使い複数行に分割
    - `RUN apt-get update`と`apt-get install`は常に同じ`RUN`命令文で連結すべき

    

参考URL：https://qiita.com/gold-kou/items/44860fbda1a34a001fc1

![image.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F221948%2Fd10acbd7-0e24-7368-2e07-bcceec665451.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=ce635ac70d424206facd8a8862f0d0e5)

- build

```sudo
docker image build -t [イメージ名] -f [Dockerfile]
```



---

## DockerでGPUを使用

参考：

- [PyTorch+GPUをDockerで実装](https://qiita.com/conankonnako/items/787b69cd8cbfe7d7cb88)
- dockerhubにある公式のイメージ：[pytorch/pytorch](https://hub.docker.com/r/pytorch/pytorch)

