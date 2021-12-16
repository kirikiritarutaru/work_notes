# EfficientNetV2: Smaller Models and Faster Training

- [Tan, M., & Le, Q. V. (2021). Efficientnetv2: Smaller models and faster training. *arXiv preprint arXiv:2104.00298*.](https://arxiv.org/abs/2104.00298)

## 概要

-  従来よりも高速に学習できてパラメータ効率の優れたCNNを提案するよ
   -  NAS (Neural architecture search) によってトレーニング速度とパラメータ効率を最適化したよ
-  学習する過程で工夫した Progressive learningを提案するよ
-  提案ネットワーク EfficientNetV2 は従来のモデルよりも高精度なのに5~11倍の速度で学習できるよ

## 問題設定と解決したこと

- ネットワークはたくさん提案されてているけど計算量パないし学習に時間かかりまくるよ
- そんなネットワークはお金と時間がなんぼあっても足りなくなるから、学習効率（低パラメータかつ高速学習）に注目したネットワークを提案するよ
  - EfficientNetsを改善
    - EfficientNetsの学習ボトルネック
      1. 大きな画像サイズでのトレーニングが遅い
         - 画像サイズ大きい→メモリにのらないから小さいバッチサイズで学習→学習速度が低下
      2. 浅い層での depth-wise convolution が遅い
      3. EfficientNetの各ステージで均等にスケールアップする手法は最適ではない
- 上記を解決した高精度・高速学習・低パラメータ数を両立するネットワークと学習手法を提案するよ

## 何をどう使ったのか

- EfficientNetV2の工夫
  - NASで探索したネットワーク構造→低パラメータ数だが高精度
  - Progressive learning：学習中の工夫→学習速度UP
    - エポック数が増えるほど画像サイズを**大きく**する
    - エポック数が増えるほど正則化（データ拡張の度合い）を**強く**かける
- EfficientNetsの学習ボトルネックの解決
  1. 大きな画像サイズでのトレーニングが遅い
     - 解決策：学習時の画像サイズを小さくする&学習中に画像サイズと正則化を段階的に調整する
  2. 浅い層での depth-wise convolution (DwC)が遅い
     - 解決策：DwC を使っているMBConvブロックを、DwCを使っていない Fused-MBConvブロックに置き換える
  3. EfficientNetの各ステージで均等にスケールアップする手法は最適ではない
     - 解決策：非一様なスケーリング戦略（後ろのステージの層を徐々にに追加していく）を採用
- Depth-wise convolutionについて
  - [参考](https://www.robotech-note.com/entry/2017/12/27/084952)
  - 1チャンネルに一つのフィルタが対応して畳み込み
  - チャンネルごとに独立して畳み込みし、入力と出力のチャンネル数は変化しない

- Fused-MBConv ブロックについて
  - depthwise convolution 3×3 と convolution 1×1にわかれていたものを convolution 3×3 に置き換える
    - 最初の方の層をFused-MBConvに置き換えることで、パラメータとFLOPｓのオーバヘッドを小さくして、学習速度を向上
    - 深い層ではDwCのが効果的（らしい）

  - 図中のSE：[Squeeze-and-Excitationモジュール ( SENet より )](https://openaccess.thecvf.com/content_cvpr_2018/papers/Hu_Squeeze-and-Excitation_Networks_CVPR_2018_paper.pdf)（←これ論文内で言及ないけどそんなありふれているか…？）


![Fused-MBConv](/home/taru/src/work_notes/paper_summary/picture/Fused-MBConv.png)

- Progressive learning について
  - 学習をステージごとにわけてステージが進むごとに正則化を強くする![progressive learning example](/home/taru/src/work_notes/paper_summary/picture/progressive learning example.png)
  - *正則化*とは？
    1. **Dropout**
       - ランダムにチャンネルをドロップすることで *co-adaptation* を抑える
    2. **RandAugment**
       - 画像ごとのデータオーグメンテーション
         - 14種類のデータ拡張操作からランダムに$N$個選び、それぞれを強さ$M$で順番に適用する方法
    3. **Mixup**
       - クロスイメージデータオーグメンテーション
       - 2枚の画像とそのラベル $(x_i, y_i), (x_j, y_j)$ を混合比 $\lambda$ でミックス
         - $\hat x_i  = \lambda x_j + (1-\lambda) x_i, \ \hat y_i = \lambda y_j + (1-\lambda)y_i$
  - アルゴリズムは以下の通り
    - （スタートとゴールの強度を決めて、ステージごとにだんだん正則化を強くかけていくという意味でしかないな…）

![Progressive learning algorithm](/home/taru/src/work_notes/paper_summary/picture/Progressive learning algorithm.png)

## 主張の有効性の検証方法

- ImageNetでSOTA
- ImageNet21kでもSOTA
  - 学習画像13M、クラス数21841というどれかデータセット
  - 学習速度がくっっっっそ早いEfficientNetV2はImageNet21kでも問題なく学習できる
    - 他のモデルには無理ですよねというｲｷﾘ


## 批評

- （ImageNetに過剰適合してませんか？？）
  - でもKaggleで採用率高いから有能なのかも？
  - 学習が早いから実験のイテレーション回しやすくて採用している人が多いのかもしれない…


## 次に読むべき論文

- [EfficientNetV1](https://arxiv.org/abs/1905.11946)

- [SENet](https://openaccess.thecvf.com/content_cvpr_2018/papers/Hu_Squeeze-and-Excitation_Networks_CVPR_2018_paper.pdf)
  - ![squeeze-and-Excitation block](/home/taru/src/work_notes/paper_summary/picture/squeeze-and-Excitation block.png)
  - [MobileNet(v1,v2,v3)を簡単に解説してみた](https://qiita.com/omiita/items/77dadd5a7b16a104df83)（チャネル方向のself-attentionとも言えるな！）
    1. 各チャネルの代表値をGlobal Average Pooling 2D でとる
    2. とった代表値を全結合層に入れて各チャネルの重みを計算
    3. 計算した重みをもともとのinputと掛け合わせる

- [RandAugment](https://arxiv.org/abs/1909.13719)

  - Cubuk, E. D., Zoph, B., Shlens, J.,  & Le, Q. V. (2020). Randaugment: Practical automated data  augmentation with a reduced search space. In *Proceedings of the IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops* (pp. 702-703).

  - [【論文読解】RandAugment: Practical automated data augmentation with a reduced search space](https://qiita.com/takoroy/items/e2f1ee627311be5d879d)

    
