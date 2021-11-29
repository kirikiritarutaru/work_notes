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

        > 		An informal but descriptive proof is as follows. Note the equality: A1B1 + A2B2 = \[A1, A2][B1; B2] where [ , ] is horizontal concatenation and [ ; ] is vertical concatenation. Let Ai be the weight of the last layer and Bi be the output response of the second-last layer in the block. In the case of C = 2, the element-wise addition in Fig. 3(a) is A1B1 + A2B2, the weight of the last layer in Fig. 3(b) is [A1, A2], and the concatenation of outputs of second-last layers in Fig. 3(b) is [B1; B2].

    - ブロックのパラメータ数

      - $C ·(256 ·d + 3 ·3 ·d ·d + d ·256) $
        - ここで，Cはカーディナリティ，dはボトルネックのチャンネル数
        - 入力のチャンネル数256，ボトルネックのカーネルサイズ3×3の場合

  

## 主張の有効性の検証方法

- ImageNet-1Kで同じくらいのパラメータ数のResNetとResNeXtを比較．ResNeXtのほうが1％ポイントぐらいよき

## 批評

- 

## 次に読むべき論文

- Grouped Convolution
  - [Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). Imagenet classification with deep convolutional neural networks. *Advances in neural information processing systems*, *25*, 1097-1105.](https://proceedings.neurips.cc/paper/2012/file/c399862d3b9d6b76c8436e924a68c45b-Paper.pdf)
