# On Empirical Comparisons of Optimizers for Deep Learning

## 論文について (掲載ジャーナルなど)
- [Choi, D., Shallue, C. J., Nado, Z., Lee, J., Maddison, C. J., &  Dahl, G. E. (2019). On empirical comparisons of optimizers for deep  learning. *arXiv preprint arXiv:1910.05446*.](https://arxiv.org/pdf/1910.05446.pdf)

## 概要
- ディープラーニングの最適化手法についてめっちゃ調べたよ！
- 最適化手法同士を比較するときには、**ハイパラチューニングに気をつけないといけない**ということがわかったよ！
  - Adaptive gradient methods は基本、SGDやMomentumを下回らない
  - しかしながら、ハイパラチューニングをミスったら Adaptive gradient methods のほうが悪くなるケースも普通にある


## 問題設定と解決したこと
- 各最適化手法の包含関係を定め、関係を明らかにした。
  - ここで、「包含関係」とは「ある最適化手法Aを他の最適化手法Bで近似的にシミュレートできる場合、$A\subseteq B$ と書く」

- 各最適化手法の包含関係
  - $\text{SGD} \subseteq \text{MOMENTUM} \subseteq \text{RMSPROP}$
  - $\text{SGD} \subseteq \text{MOMENTUM} \subseteq \text{ADAM}$
  - $\text{SGD} \subseteq \text{NESTEROV} \subseteq \text{NADAM}$


## 何をどう使ったのか
- 

## 主張の有効性の検証方法
- 

## 批評
- Conclusions より引用（内容を要約して抜粋）

> 本論文の結果を過度に一般化しないように注意が必要。注意点は2つ。
>
> 1. バッチサイズを変化させた場合の効果を測定していない点
> 2. 結果はパラメータのチューニングプロトコルと解いている問題（とモデル）に**強く**依存している点
>
> ベストプラクティスをあげるとするならば、
>
> - *何回も実験しなおせるほど潤沢にお金 or 時間があるならば*、Adaptive gradient methods で**全ての**ハイパラをチューニングすべし
>   - 一つのハイパラの最適値は、他のハイパラの設定値に依存する可能性があることを頭に残す
> - 最適化手法を比較する場合はハイパラを探索した範囲を記載し、結果を解釈する際に、どのハイパラをチューニングしたかを強調すべし

## 次に読むべき論文
- [Adamの論文](https://arxiv.org/abs/1412.6980)
