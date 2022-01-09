# Aggregated Residual Transformations for Deep Neural Networks

## 論文について (掲載ジャーナルなど)

- [Xie, S., Girshick, R., Dollár, P., Tu, Z., & He, K. (2017).  Aggregated residual transformations for deep neural networks. In *Proceedings of the IEEE conference on computer vision and pattern recognition* (pp. 1492-1500).](https://arxiv.org/pdf/1611.05431.pdf)

## 概要

- ResNetのモジュール（ボトルネックのブロック）をより発展させてさらに性能のいいモジュールを提案するよ！
  - ネットワークの深さと幅の次元に加えて「カーディナリティ」という次元を追加するよ！
  - 深さ・幅よりもカーディナリティを増やすほうが，精度がよくなる傾向にあるよ
- 作ったモデルをResNeXtと名付けたよ！ImageNet-5KとCOCOの物体検知でSOTAだったよ！

## 問題設定と解決したこと

- 画像分類を高精度に解きたい
  - visual recognitionのタスクは「feature engineering」から「network engineering」にパラダイムが移ってきてる
- 新しいネットワークのモジュール（ブロック単位）を提案
  - 2つの重要な戦略を受け継いでいる
    - モジュールの入出力の次元を同じにする戦略
      - VGG-netやResNetで深いネットワークを構築するための戦略だね！
    - 分割・変換・集約戦略
      - Inceptionモデルで取られている戦略だね！
        - モジュールのカスタマイズ性が高すぎて，うまくいくネットワークを構築するのは難しい
- このモジュールをたくさん連結してネットワークを構築することで，ResNetよりもパラメータ数を低減しながら，高精度を達成！

## 何をどう使ったのか

- ２つの戦略をとる

  - 入出力の次元が同じになるResidual Blockを積み上げる戦略

    - ブロックはシンプルなルール2つに従う（この2つのルールがあれば，テンプレートとなるモジュールを設計するだけで，ネットワーク上のすべてのモジュールが適宜決定される）
      1. 同じサイズの spatial map を生成する場合，ブロックは同じハイパーパラメータ（幅とフィルタサイズ）を共有する
      2. spatial map が $\frac{1}{2}$ にダウンサンプリングされるたびに，ブロックの幅を2倍にする

  - 分割・変換・集約戦略（それぞれの数字は例）

    - 分割

      - 256ch の入力のチャンネルを 4ch × 32 に分割

    - 変換

      - 1つの分割に注目．4ch に 3×3 のConvolutionをかけて 4ch に変換．
      - 32つの分割それぞれで↑をする

    - 集約

      - 1つの分割に注目．4chに 1×1 のConvolutionをかけて 256ch に変換

    - 1×1conv→Grouped Convolution (group=32)→1×1conv というブロックと計算上等しい

      - 論文4pの左下の脚注に注目．同じ計算になるように$B_1$と$B_2$を恣意的に選ぶんやで．（別パラメータやんけておもたらあかん）

        > An informal but descriptive proof is as follows. Note the equality: A1B1 + A2B2 = \[A1, A2][B1; B2] where [ , ] is horizontal concatenation and [ ; ] is vertical concatenation. Let Ai be the weight of the last layer and Bi be the output response of the second-last layer in the block. In the case of C = 2, the element-wise addition in Fig. 3(a) is A1B1 + A2B2, the weight of the last layer in Fig. 3(b) is [A1, A2], and the concatenation of outputs of second-last layers in Fig. 3(b) is [B1; B2].

- ResNet の bottleneck block と ResNeXt の block のパラメータ数の比較

  - 論文図1を引用
  - <img src="/home/taru/src/work_notes/paper_summary/picture/ResNetのボトルネックブロックとResNeXtのブロック.png" alt="ResNetのボトルネックブロックとResNeXtのブロック" style="zoom: 150%;" />
  - 条件
    - 入力 256 ch、出力 256 ch、Convのカーネルサイズ $3\times3$とする
  - ResNet の bottleneck blockのパラメータ数
    - $69632= 256\times64 + 64\times(3\times3)\times64 + 64\times256$
  - ResNeXt の block のパラメータ数
    - 式：$C ·(256\times d + d\times(3\times3)\times d + d \times256) $

      - ここで，$C$はカーディナリティ，$d$はボトルネックのチャンネル数
    - $70144=32\times(256\times4+4\times(3\times3)\times4+4\times256)$　
      - カーディナリティ$=32$、ボトルネックのチャンネル数$=4$の場合


## 主張の有効性の検証方法

- 画像認識
  - 複数データセットでResNextの精度を確認
    - ImageNet-1K, 5K
    - CIFAR-10, 100
      - 8GPUで128ミニバッチ
      - momentum SGDでweight decayあり、段階的にlearning rateを減少
      - 300 epoch
  - 結果： ResNeXt > ResNet （実験ごとに層数は異なるよ）
    - **カーディナリティを増やすと精度向上**の傾向
      - 層数増やしても精度良くなるけどカーディナリティ増やすほうがよい傾向
- 物体検知
  - COCO minival
    - Faster R-CNNのバックグラウンドのネットワークとしてResNeXtを適用SOTA
      - ImageNet-1Kで事前学習
      - 8GPUで128ミニバッチ（←クソデカ）
      - momentum SGDでweight decayあり段階的にlearning rateを減少
        - やっぱSOTAだそうとしたらmomentum SGDでゆっくり学習かー


## 批評

- ニューラルネットの理論計算量
  - 「一つの入力データに対して適用される浮動小数点演算の回数」
    - ただし、メモリ転送量およびNNの推論最適化の影響は無視するとする

  - 参考：[Chainerで書いたニューラルネットの理論計算量を推定するchainer_computational_cost](https://daily.belltail.jp/?p=2537#hs_b13c81e1d93e8b709d82152347459f21_footnote_1)

- （ResNet-50とResNeXt-50のパラメータ数と計算量いうほど同程度なんやろか…？感覚がわからん）

## 次に読むべき論文

- Grouped Convolution
  - [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). Imagenet classification with deep convolutional neural networks. *Advances in neural information processing systems*, *25*, 1097-1105.](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)
- Faster R-CNN
  - [Ren, S., He, K., Girshick, R., & Sun, J. (2016). Faster R-CNN:  towards real-time object detection with region proposal networks. *IEEE transactions on pattern analysis and machine intelligence*, *39*(6), 1137-1149.](https://arxiv.org/pdf/1506.01497.pdf)
- Batch Normalization
  - [Ioffe, S., & Szegedy, C. (2015, June). Batch normalization:  Accelerating deep network training by reducing internal covariate shift. In *International conference on machine learning* (pp. 448-456). PMLR.](https://arxiv.org/pdf/1502.03167.pdf)
