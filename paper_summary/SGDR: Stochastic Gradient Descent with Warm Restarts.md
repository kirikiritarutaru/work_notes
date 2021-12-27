# SGDR: Stochastic Gradient Descent with Warm Restarts

## 論文について (掲載ジャーナルなど)
- [Loshchilov, I., & Hutter, F. (2016). Sgdr: Stochastic gradient descent with warm restarts. *arXiv preprint arXiv:1608.03983*.](https://arxiv.org/abs/1608.03983)

## 概要
- CosineAnealingWarmRestartsの元論文
- 一言でいうと学習率のスケジューリング手法の提案

## 問題設定と解決したこと
- DNNの学習において、学習を早くしたい＆収束性を良くしたい
 - DNNを学習する際の、学習率のスケジューリング手法を提案
   - 多峰性関数を扱う勾配フリーな最適化ではリスタートテクニックが一般的
   - 勾配ベースの最適化においても、ill-conditioned 関数において学習を加速させ収束率を向上するために部分的な warm restartテクニックがよく使われる
   - SGDに応用しちゃおうぜ！

## 何をどう使ったのか
- こんなふう↓に遷移
  - 参考記事：[PyTorchのSchedulerまとめtorch v1.1.0](https://katsura-jp.hatenablog.com/entry/2019/07/24/143104#CosineAnnealingWarmRestarts)
  - <img src="https://cdn-ak.f.st-hatena.com/images/fotolife/k/katsura_jp/20190724/20190724134004.png" alt="f:id:katsura_jp:20190724134004p:plain" style="zoom:67%;" />

- 次の式に従って学習率$\eta$をスケジューリング

  - $$
    \eta_t=\eta^i_{\min}+\frac{1}{2} \left(\eta^i_{\max}-\eta^i_{\min}\right)\left(1+\cos\left(\frac{T_{\text{cur}}}{T_i}\pi \right) \right)
    $$

    - ここで、$i$はランの回数。$t$はbatch iteration。
    - $\eta^i_{\min}$と$\eta^i_{\max}$は学習率の範囲。$T_{\text{cur}}$は最後のリスタートから経過したエポック数。
    - $T_i$が$i$番目のランの総エポック数。

  - $T_i=T_0\times T_{\text{multi}^i}$で徐々にリスタートする間隔を伸ばしていく。$\eta^i_{\max}$から$\eta^i_{\min}$まで徐々に減少していって、$T_{\text{cur}}=T_i$になったら、$\eta^i_{\max}$に戻ってリスタート。


## 主張の有効性の検証方法
 - 以下の条件で精度比較
   - データセット
     - CIFAR-10
     - CIFAR-100
   - DNNモデル
     - Wide Residual Neural Networks (WRN)
 - 結果
   - 精度：微増
   - 学習速度：同じ精度に達する速度を比較した場合、デフォルトの2~4倍に高速化。大きなネットワークも学習可能に。
   - 備考：オーバーフィットが小さくなる？

 - リスタート直前のモデルを保存して、アンサンブルすると精度向上する（という発見を再現した）
   - 多様性のある予測モデルが得られているようだ

## 批評
 - 学習が早くなって、少ないエポックで実験が回せるから色々試す場合には良さそう
 - 最終的な精度の向上という意味ではそれほど改善はなさそう
 - 既存の研究でwarm restart テクニックがよく使われるからDNNでもためそう→うまくいったという感じ
   - 実験科学だなぁ。あまり理屈はない。
 - テストエラーが直角にカックカク曲がりながらさがっているけど、停滞してる時間って意味あるのかな
   - ぐっと降りたあとの周辺の地形の情報を探索するのが大切なのかな？
 - 多峰性関数の穴から抜け出すのにリスタートテクニックを使う、は直感的にわかりやすい
 - しかし、学習高速化・精度向上がうまくいくのは謎。
   - 学習率高い状態に戻したらそこまで微調整のために動いていたのが台無しになりそうなのに
 - アンサンブルもなんでうまくいくんだろ
   - いい初期値から徐々に学習率低くしながら学習する←これが本質？コサインアニーリング自体は枝葉なのか？

## 次に読むべき論文
- 
