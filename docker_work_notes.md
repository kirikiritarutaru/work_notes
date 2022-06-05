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
FROM centos

MAINTAINER tarutaru

LABEL title="sampleImage"\
      version="1.0"\
      description="This is a sample."

RUN mkdir /myvol
RUN echo "hello world" > /myvol/greeting
VOLUME /myvol

ENV hoge=hogehoge

EXPOSE 80

WORKDIR /tmp
RUN ["pwd"]

ADD https://github.com/docker/cli/blob/master/README.md /tmp

COPY sample.txt /tmp
```

  - ビルド
    - `docker image build -f Dockerfile .`
  - きちんと実行できたか確認

```bash
#イメージ一覧確認
docker image ls
REPOSITORY          TAG                 IMAGE ID            CREATED             SIZE
<none>              <none>              b4dc0b57f8a8        23 seconds ago      200MB

#コンテナ起動
docker container run -it -p 8080:80 b4dc0b57f8a8

#/tmpに移動していることを確認
[root@6ea955b74e97 tmp# pwd
/tmp

#OSがCentOS最新版であることを確認(上記Step1)
cat /etc/redhat-release
CentOS Linux release 7.5.1804 (Core)

#マウントされていることを確認(上記Step4~6)
cat /myvol/greeting
hello world

#環境変数確認(上記Step7)
[root@6ea955b74e97 tmp]# printenv |grep hoge
hoge=hogehoge

#/tmpにファイルが格納されていることを確認(上記Step11~12)
[root@6ea955b74e97 tmp]# ls /tmp
README.md  ks-script-3QMvMi  sample.txt  yum.log

#exitでコンテナを抜ける
exit

#ポート番号確認(上記Step8)
docker container ls -a
CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS                         PORTS                  NAMES
6ea955b74e97        b4dc0b57f8a8        "/bin/bash"         24 minutes ago      Up 24 minutes                  0.0.0.0:8080->80/tcp   dazzling_beaver

#メタ情報確認(上記Step3)
docker image inspect 6ea955b74e97 |grep title
                "title": "sampleImage",
docker image inspect 6ea955b74e97 |grep version
                "org.label-schema.schema-version": "= 1.0     org.label-schema.name=CentOS Base Image     org.label-schema.vendor=CentOS     org.label-schema.license=GPLv2     org.label-schema.build-date=20180531",
                "version": "1.0"
docker image inspect 6ea955b74e97 |grep description
                "description": "This is a sample.",
```

- Dockerfile

  - 一言でいうと、「コンテナの構成情報を定義したファイル」

  - Dockerfileを用意すれば何回もDockerコマンドを叩く必要なく、1コマンドでDockerイメージを生成できる

  - [Dockerfileのベストプラクティス](http://docs.docker.jp/engine/articles/dockerfile_best-practice.html)

    - `RUN`命令はバックスラッシュを使い複数行に分割
    - `RUN apt-get update`と`apt-get install`は常に同じ`RUN`命令文で連結すべき

  - 命令一覧
    - FROM：ベースイメージの指定
    - MAINTAINER：作成者情報を設定
        - ベストプラクティスいわく非推奨→LABELを使うほうが良いとのこと
    - ENV：環境変数を設定
    - WORKDIR：場所(ディレクトリ)を移動
    - USER：ユーザ変更設定
    - LABEL：メタ情報(バージョンやコメントなど)設定
    - EXPOSE：公開ポート番号設定
    - ADD：ファイルやディレクトリを取得（リモート可）
    - COPY：ファイルやディレクトリを取得（ローカルのみ）
    - VOLUME：ボリューム設定
    - ONBUILD：次のbuild時に実行されるコマンドを設定
    - RUN：ベースイメージから起動したコンテナ内で実行するコマンドを設定
    - CMD：作成したイメージが起動されたら実行するコマンドを設定
    - ENTRYPOINT：作成したイメージが起動されたら実行するコマンドを設定


[いまさらだけどDockerに入門したので分かりやすくまとめてみた](https://qiita.com/gold-kou/items/44860fbda1a34a001fc1)より引用

![image.png](https://qiita-user-contents.imgix.net/https%3A%2F%2Fqiita-image-store.s3.amazonaws.com%2F0%2F221948%2Fd10acbd7-0e24-7368-2e07-bcceec665451.png?ixlib=rb-4.0.0&auto=format&gif-q=60&q=75&s=ce635ac70d424206facd8a8862f0d0e5)

- build

```bash
docker image build -t [イメージ名] -f [Dockerfile]
```


### イメージの構造

- イメージは2つの特徴を持つ
  1. レイヤー構造になっている
  2. 一度作成されたイメージは編集不可能

- イメージは一つのミドルウェアのインストールにつき、1レイヤー重なっていくイメージ
- イメージのレイヤーはRead Only
- イメージからコンテナを起動した際に作られる「コンテナレイヤー」のみが編集可能
- コンテナからイメージを生成(commit)した場合に、既存のレイヤーの上に重なってコンテナレイヤーが保存される

`docker run` ：下記の3つを実行するコマンド
  - `docker pull` :DockerHubからイメージを取得
  - `docker create` ：取得したイメージからコンテナを作成
  - `docker start` ：作成したコンテナを起動

```bash
# 指定したコンテナの詳細情報を表示
docker inspect [NAME or UUID]
```



---

## Dockerにおけるデータ管理

- コンテナ内で扱う動的なデータは、コンテナレイヤーに置くこともできるが、下記の理由で**推奨しない**（使い勝手が悪い）
  - コンテナが削除された時点で、そのコンテナ内のデータは消える
  - コンテナ間でデータの共有はできない
  - コンテナレイヤーへのデータの書き込みは、書き込み速度が遅い
   - コンテナでは、通常のファイルシステムと異なるユニオンファイルシステムが使われている

- Dockerでは「ホストマシン上にデータを管理し、それをコンテナにマウントする」手法が使われる

- 手法は主に以下の3つ
  - volume
    - ホストマシン上に自動生成される指定ディレクトリをコンテナにマウント
  - bind mount
    - ホストマシン上の任意のディレクトリをマウント（ホスト側のディレクトリを直接操作しても良い）
  - tempfs
    - ホストマシン上のメモリ領域をコンテナ上にマウント

  

- いったんコンテナが起動すれば、コンテナ用のプロセス空間内からアクセス可能なファイルシステムでは、Dockerコンテナ用のイメージレイヤかvolumeか見分けがつかない



### volume

- ホストマシン上で以下を実行することで、volume(`/var/lib/docker/volumes` ディレクトリ)を作成
```bash
docker volume create [volumeの名前]
```
- コンテナ起動時に`--mount`オプションをつけることで指定したvolumeをマウントすることも可能
```bash
docker run -itd --name [作成するコンテナ名] --mount source=[マウントするvolume名],target=[コンテナ上のマウント先ディレクトリ] [イメージ名]
# 例：
docker run -itd --name mount-test --mount source=volume1,target=/app nginx
```

- **マウントしたvolumesディレクトリは、ホスト上のディレクトリから直接操作すべきではない**
- ホスト内で異なるコンテナを立てている場合、同じvolumeをマウントすることで、コンテナ間でファイルの共有が可能

#### volumeの管理コマンド
```bash
# volumeの一覧を表示
docker volume ls
# volumeの詳細を確認
docker volume inspect [volume名]
# volumeを削除
docker volume rm [volume名]
```

- **コンテナを削除してもvolumeは残り続けるので、必要なくなったvolumeは自分で削除する必要あり**



### bind mount

- **ホスト上の空ディレクトリをコンテナ上の`/usr`などにマウントした場合、コンテナ上のデータが消え、まともに動かなくなることがあるので、注意**
- volumeのように事前設定する必要はなく、以下のコマンドでコンテナ起動時にオプション指定しマウント

```bash
docker run -itd --name [コンテナ名] --mount type=bind,source=[マウント元ディレクトリ],target=[マウント先ディレクトリ] [イメージ名]
# 例:
docker run -itd —-name bind-mount-test —-mount type=bind,source=“$(pwd)”/mount,target=/app nginx
```



### tmpfs

- ホストマシンが終了した場合も、コンテナが終了した場合も、保持していたデータは解放される
- ホスト上のメモリを無制限に使用してしまう可能性があるので、メモリサイズを制限すべき
- コンテナ起動時に、`--mount`オプションのtypeにtmpfsを指定することでマウント

```bash
docker run -itd --name [コンテナ名] --mount type=tmpfs,destination=[マウント先ディレクトリ] [イメージ名]
# 例:
docker run -itd --name tmpfs-test --mount type=tmpfs,destination=/app nginx
```



---

## Dockerネットワーク

- 一言でいうと
  - Dockerコンテナの相互通信や、コンテナの外部との通信時に利用するLANのような内部ネットワーク
  - Dockerコンテナ内から認識できる、ネットワークインターフェースやルーティングの情報は、ホスト上から隔離されている
- `docker network ls`コマンドを実行すると、3つのネットワークを表示する
  - bridge ネットワーク
    - Dockerコンテナ実行時デフォルトで適用されるネットワーク
    - コンテナ内から外のネットワークに通信するには、Linuxのbridge機能を通して利用

  - host ネットワーク
    - ホスト側のインターフェース情報がそのまま見えるモード（ネットワーク機能を隔離せずにコンテナを起動している状態）

  - none ネットワーク
    - ネットワークインターフェースを持たない
    - コンテナ外からの通信もコンテナ内からネットワーク側への通信もできない

- **複数立ち上げたコンテナ間で通信する手法**について



---

## Docker Engine

- 一言でいうと
  - Dockerサーバーの中心的な存在。Linux上でDockerをデーモンとして管理する対称全体がDocker Engine。
  - Dockerのサーバー機能を担うプログラムやライブラリ群で構成される
    - dockerd
      - Dcoker Engineのまとめ役
      - CLIからの命令を受け付けるAPIエンドポイントを持つ
      - 処理内容をcontainerdに伝える
    - containerd
      - 内部でのAPI処理を行い、runcのようなコンテナランタイムに委ねる
      - 複数のDockerコンテナやDockerイメージ群を管理する役割
      - ockerd-shimプロセスを通し、コンテナランタイムを操作する
    - runc
      - デフォルトのコンテナランタイム。Linuexカーネルの機能を利用
      - 個々のコンテナを隔離したり特別な権限を付与するために、Linuxカーネルと通信する機能を担う



---

## Docker CLI

- 一言でいうと
  - `docker run`や`docker build`など、`docker`から始めるコマンド群で構成されるCLIツール
  - Docker Engineに対してコンテナやイメージを操作する命令を送信



---

## Docker Compose

- 一言でいうと
  - Docker CLIの一つ。複数のDockerのコンテナアプリケーションや、Dockerネットワーク、Dockerボリュームをプロジェクトと呼ぶ単位で管理
  - YAML形式のファイル単位でプロジェクトを管理

​	


---

## DockerでGPUを使用

参考：

- [PyTorch+GPUをDockerで実装](https://qiita.com/conankonnako/items/787b69cd8cbfe7d7cb88)
- dockerhubにある公式のイメージ：[pytorch/pytorch](https://hub.docker.com/r/pytorch/pytorch)

### Dockerのdefault runtimeをnvidiaに変更

-   参考:

    -   [dockerのdefault runtimeをnvidia(GPUが使えるruntime)にする](https://qiita.com/tsota/items/59948952591fd4a443be)

        -   `/etc/docker/daemon.json`に`"default-runtime": "nvidia"`を加えてサービス再起動

        -   ```sh
            # vi /etc/docker/daemon.json
            # cat /etc/docker/daemon.json 
            {
                "default-runtime": "nvidia",  # <-追加
                "runtimes": {
                    "nvidia": {
                        "path": "nvidia-container-runtime",
                        "runtimeArgs": []
                    }
                }
            }
            # systemctl restart docker
            # docker info 2> /dev/null | grep -i runtime
            Runtimes: nvidia runc
            Default Runtime: nvidia
            ```

            

参考URL：

- [【図解】Dockerの全体像を理解する -前編-](https://qiita.com/etaroid/items/b1024c7d200a75b992fc)
- [いまさらだけどDockerに入門したので分かりやすくまとめてみた](https://qiita.com/gold-kou/items/44860fbda1a34a001fc1)

