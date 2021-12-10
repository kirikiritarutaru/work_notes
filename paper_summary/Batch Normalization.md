# Batch Normalization

## 論文について (掲載ジャーナルなど)
- [Ioffe, S., & Szegedy, C. (2015, June). Batch normalization:  Accelerating deep network training by reducing internal covariate shift. In *International conference on machine learning* (pp. 448-456). PMLR.](https://arxiv.org/abs/1502.03167)
  - このメモではBatch NormalizationをBNと呼称


## 概要
- ディープニュラルネットワークでは、前のレイヤのパラメータが変化するとトレーニング中に各レイヤーの入力の分布が変化し、ネットワークの学習が超困難
- 学習中の各ミニバッチごとに正規化（←やってることは標準化＋αでは…？）することで、↑の問題を解決
- BNのメリット
  - 学習率を高くできる
  - パラメータの初期値に敏感でなくなる
  - ドロップアウトが必要なくなる

## 問題設定と解決したこと
- 

## 何をどう使ったのか
- バッチ内でチャンネルごとに*BN*
  - ややこしい

<img src="/home/taru/src/work_notes/paper_summary/picture/Batch Normalization.png" alt="ResNextメモ" style="zoom:72%;" />

## 主張の有効性の検証方法
- 

## 批評
- 共変量シフトが起こらなくなると論文内では主張しているが、**そうではない**ことが後の論文で明らかに

## 次に読むべき論文
- Santurkar, S., Tsipras, D., Ilyas, A., & Mądry, A. (2018, December). How does batch normalization help optimization?. In *Proceedings of the 32nd international conference on neural information processing systems* (pp. 2488-2498).
