# Adam: A Method for Stochastic Optimization

## 論文について (掲載ジャーナルなど)
- [Kingma, D. P., & Ba, J. (2014). Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*.](https://arxiv.org/abs/1412.6980)

## 概要
- 新しい最適化手法を提案した
  - Adamと改良版AdaMax（←$L_\infty$ ノルムに基づく）

- 実装が簡単で、計算効率が高く、必要なメモリも少ない手法です
- データやパラメータ数が大きい問題に適しているよ！

## 問題設定と解決したこと
- 目的関数が確率的な挙動をするときは、高次の最適化手法は適してないよ。一次の手法に限定して考えたよ
- 「ノイズの多い高次元な損失関数の期待値をパラメータに対して最小化」するのを、効率的にできるアルゴリズムを提案したよ

## 何をどう使ったのか
- 勾配の1次および2次モーメントの推定値から**学習率を学習過程の中で更新していくAdaGrad**と**古い勾配情報を落として、新しい勾配情報が反映して動くRMSProp**を組み合わせたアルゴリズム
  - 振動：目的関数の谷底に向かってガタガタに動くこと
- Adamは勾配と勾配の二乗の指数移動平均を更新するよ

![Adam Algprighm](/home/taru/src/work_notes/paper_summary/picture/Adam Algprighm.png)

## 主張の有効性の検証方法
- ロジスティック回帰をMNISTやIMDBでトレーニングして、Adamでチューニングしたらめっちゃはやく精度↑
- MLPでMNISTとかCNNでCIFAR-10したら早く高精度に到達できた

## 批評
- あとあとの論文で$\beta$とか$\varepsilon$が精度にかなり影響するって言われるようになるね

## 次に読むべき論文
- [SAM](https://arxiv.org/abs/2010.01412)
- [ASAM](https://arxiv.org/abs/2102.11600)
  - SAM を Adaptive にしたバージョン

