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
- Fused-MBConv ブロックについて
  - 

## 主張の有効性の検証方法

- ImageNet/ 

## 批評

- 

## 次に読むべき論文

- [EfficientNetV1](https://arxiv.org/abs/1905.11946)
