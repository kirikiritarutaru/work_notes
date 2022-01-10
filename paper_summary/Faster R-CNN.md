# Faster R-CNN: Towards Real-Time Object Detection with Region Proposal Networks

## 論文について (掲載ジャーナルなど)
- [Ren, S., He, K., Girshick, R., &  Sun, J. (2015). Faster r-cnn: Towards real-time object detection with  region proposal networks. *Advances in neural information processing systems*, *28*, 91-99.](https://arxiv.org/pdf/1506.01497.pdf)

## 概要
- 最新（2016年）の object detection ネットワークは物体の領域提案アルゴリズムに依存している
  - 物体の領域提案の計算がボトルネックとなっていることが最近の研究でわかってきた

- 本研究では、Region Proposal Network (RPN) ＝領域提案ネットワークを提案する
  - RPNは、検出ネットワークと畳込み特徴を共有し、ほぼ計算コストなしで物体の領域を提案する


## 問題設定と解決したこと
- 問題：
  - 物体検出は Region-based convolutional neuralnetworks (RCNNs) と物体の領域提案アルゴリズムにより高精度化しているが、「領域提案」にかかる計算コストが膨大なのがボトルネック

- 解決：
  - 領域提案アルゴリズムをネットワークに置き換えることで高速化しボトルネックを解消した


## 何をどう使ったのか

（全体的に[Faster R-CNNにおけるRPNの世界一分かりやすい解説](https://medium.com/lsc-psd/faster-r-cnn%E3%81%AB%E3%81%8A%E3%81%91%E3%82%8Brpn%E3%81%AE%E4%B8%96%E7%95%8C%E4%B8%80%E5%88%86%E3%81%8B%E3%82%8A%E3%82%84%E3%81%99%E3%81%84%E8%A7%A3%E8%AA%AC-dfc0c293cb69)より引用）

- Faster R-CNNの全体像
  - 全体構造
    1. 入力画像から、VGG16等を用いて畳み込み特徴マップを作成
       - 畳み込み特徴マップをRPNに通して物体領域の候補を得る
    2. 畳み込み特徴マップ＋物体領域の候補を、ROI Pooling（入力を固定長に変換するアルゴリズム）により変換
    3. 2で得たベクトル4096の全結合層に2回通して、物体のクラス分類用と物体領域の回帰用の出力を得る
       - 物体領域の回帰用の出力は正確にいうと、「Anchor（後述）と画像中の物体の位置のズレの量」
  - [MathWorksのドキュメント](https://jp.mathworks.com/help/vision/ug/getting-started-with-r-cnn-fast-r-cnn-and-faster-r-cnn.html)より引用<img src="/home/taru/src/work_notes/paper_summary/picture/Faster R-CNNの概要.png" alt="Faster R-CNNの概要" style="zoom:110%;" />

- 本論文のコントリビューション

  - 領域提案ネットワーク（RPN）（の設計と学習方式）の提案
    - Fast R-CNNの中の領域提案アルゴリズムを領域提案ネットワーク（RPN）に置き換えることで2つの利点がある
      - 前段の畳み込み層で算出した畳み込み特徴マップを、後段のRPNと共有することで領域提案にかかる計算をほぼノーコストで実行
      - RPNはFCN ([Fully Convolutional Network](https://arxiv.org/abs/1411.4038))の一種であり、E2Eに学習が可能
    - 領域提案に”アンカーボックス”という方式を導入している
      - アンカーボックスとは？（←超ややこしい）
        - 
        - Anchor
          - 特徴マップ上の各点
            - 画像中の調べる矩形の*中心*の役割をはたす
          - 例：VGG16のを特徴抽出のネットワークとして用いた場合
            - VGG16から出力される特徴マップを元画像に対応付けると、16ピクセルに1つの割合で等間隔にAnchorが配置される
            - $300\times400$の画像だと特徴マップの大きさは$18\times25$
        - Ancor box
          - Anchorを中心に作られる物体領域の候補となるボックス
          - 各Anchorから(1)基準の長さ、(2)縦横比をそれぞれ決めることで、複数のAnchor boxesを作成
            - 例：
              - (1)と(2)を以下のように設定すると、Anchor boxesは$3\times3$個作成される
                - 基準の長さ＝64, 128, 256
                - 縦横比＝1:1, 1:2, 2:1
              - $300\times400$の画像だと、Anchor boxesの総数は最大で$4050(=18\times25\times9)$個
          - 画像からはみ出たAnchor boxesは無視
    - RPNの学習について
      - 以下の2つを学習
        1. あるAnchor boxの中身が背景か物体か
        2. 物体だった場合、ground truthとどれぐらいズレているか
      - 1.について
        - 背景か物体かの2値分類タスク
          - ground truth と Anchor boxes のIoUを計算
          - IoU<0.3→背景、IoU>0.7→物体とラベル付け（0.3<IoU<0.7のAnchor boxesは無視）
          - 例：
            - Anchor boxes が各Anchorに9個作成される場合、一つのAnchorにつき$18(=9\times2)$個の2値分類タスクとなる
          - 誤差関数：バイナリクロスエントロピー
      - 2.について
        - Anchor box と ground truthとの"ズレ量"を当てる回帰タスク
          - ズレの4つの指標
            - 中心x座標のズレ
            - 中心y座標のズレ
            - 横の長さのズレ
            - 縦の長さのズレ
          - 例：
            - Anchor boxes が各Anchorに9個作成される場合、一つのAnchorにつき$36(=9\times4)$個の数値の回帰タスク
          - 誤差関数：$L_1$ノルムベースの関数

  - Faster R-CNNの学習方式の提案
    - (1)領域提案タスクの学習と(2)物体検出タスクの学習を交互に実行
      1. RPNの勾配更新
      2. Faster R-CNN全体の勾配更新
    - 物体領域の提案の固定化と学習の収束の高速化を狙っている

## 主張の有効性の検証方法
- 物体検出精度
  - 下記データセットでSOTA
  - PASCAL VOC 2007, 2012
  - MSCOCO
  - ILSVRC, COCO 2015のコンペでは一位解法のベースとなっている

- 物体検出の実行時間
  - PASCAL VOCにおいて、物体領域の提案の実効実行時間は10 msec
  - 深いネットワーク（VGG16）を使ってもGPUなら 5 fps だせる


## 批評
- 実装はCaffe！歴史を感じる
  - 論文2016年発表だもんね
- 論文読んでたらExperimentsの章からはいはいSOTA, SOTAって気分になるな…
- 1枚数十msecで処理可能っていうのが当時としては革新的なのか
  - 世の中の流れがリアルタイム処理に傾倒していった
  - 計算機、特にGPUのスペックどっかに書いてるのか？
    - 当時は選択肢がなかったとか？
- AnchorあたりとかRPNの出力とかRPN学習とか説明不足では
  - 解説記事読んでやっとわかった…（わかったのか？）

- まだまだエンジニアリング的な要素が強い
  - Anchor boxesを画像中にばらまくところとかRPNでズレの回帰とか
- RoI poolingについてはFast R-CNNの論文読んでね！

## 次に読むべき論文

- [[DL輪読会]YOLO9000: Better, Faster, Stronger](https://www.slideshare.net/DeepLearningJP2016/dl-reading-paper20170804pdf)より引用
  - 領域候補だすアルゴリズム（Selective Search）が重いからSelective Search使うの回避したい→RPNに置き換え（Faster R-CNNの貢献）→物体検出の速度上げたい→領域候補生成と各領域の特徴ベクトルを切り出して分類の2段階かかるのかったるいから一度にやる（YOLOの貢献）→物体検出の精度上げたい→深さの異なる複数の特徴マップ（浅い側は小さい物体、深い側は大きい物体を検出）を追加（SSDの貢献）
  - YOLOの作者 Redmanのクセがすごいらしい
- [物体検出のDeepLearning読むべき論文7選とポイントまとめ【EfficientDetまでの道筋】](https://qiita.com/kazukiii/items/f5a35450a8dd02d3a266)より引用
  - [Fast R-CNN](https://arxiv.org/abs/1504.08083)
  - [YOLO](https://arxiv.org/pdf/1506.02640.pdf)
  - [Focal Loss for Dense Object Detection](https://arxiv.org/pdf/1708.02002.pdf)
    - 通称RetinaNet
