# Deep Residual Learning for Image Recognition

## 論文について (掲載ジャーナルなど)
- [He, K., Zhang, X., Ren, S., & Sun, J. (2016). Deep residual learning for image recognition. In *Proceedings of the IEEE conference on computer vision and pattern recognition* (pp. 770-778).](https://arxiv.org/pdf/1512.03385.pdf)

## 概要
- 深いニューラルネットワークの学習は困難
- 従来（数十層程度）よりも大幅に深いネットワークの学習を容易にする、**残差学習フレームワーク**を提案
- visual recognition tasks （画像認識、位置特定、物体検出、セグメンテーション）で高精度を達成することを確認

## 問題設定と解決したこと
- visual recognition tasks で高い精度のニューラルネットワークモデルを作りたい
- 高精度なニューラルネットワークを学習するには、層を深くすることが重要っぽいことが既存の研究で示されている
- 深いニューラルネットワークを学習したいが、勾配消失/爆発問題が起こりやすく、学習が困難
  - **バッチ正規化**のおかげで、勾配消失/爆発問題はある程度緩和されたが、非常に深い（百数十層程度）では、学習誤差が大きくなり精度劣化をまねく
- 深いニューラルネットワークを学習可能な残差学習フレームワークを提案した
  - このフレームワークによって、下記2点を達成
    - 学習誤差により精度が劣化する問題を防ぐ
      - 深い層まで、情報（初期層で獲得した表現）を届けることで
    - 最適化の簡易化

## 何をどう使ったのか
- 残差ブロック (Residual Block) を提案
  - 畳み込み層のまとまり（2~3層）に対して、並列に恒等写像（**スキップ接続**）を加える
  - $x$を入力とする。
    複数の非線形層を積み上げることにより、
    目的の複雑な関数$H(x)$を漸近的に近似＝残差関数$\mathcal{F}(x)=H(x)-x$を漸近的に近似
    - どちらも同じ「目的の関数」を漸近的に近似できるが、*学習のしやすさ*が異なる可能性があるのでは！？
  - $y=\mathcal{F}(x,\{W_i\})+x$
    - ここで、 $x$ は入力ベクトル。 $y$ は出力ベクトル。 $\mathcal{F}(x,\{W_i\})$ は residual mapping
    - 下の図の例だと、$\mathcal{F}=W_2\sigma(W_1x)$ （$\sigma$ はReLU）（論文の図2より引用）

![residual block](/home/taru/src/work_notes/paper_summary/picture/residual block.png)

- Residual Network

  - 畳み込み層33層、最後にFC層1層

  - 入力と出力の次元数が同じである場合、スキップ接続はそのまま

  - 入力の次元数よりも出力の次元数が大きい場合（＝**次元数が同じではない場合**）、選択肢は２つ（←細かいとこやな）

    1. 次元が大きくなったぶんゼロパディングを追加して、（無理やり）恒等写像←パラメータは増えないよ
    2. 線形写像 $W_s$ を噛ませて、 $y=\mathcal{F}(x,\{W_i\})+W_sx$ として、次元を合わせる。

  - どちらのオプションでもショートカットが2つのサイズの特徴マップにまたがる場合、ストライドを2にして実行

    

- 実装（めっちゃ他の論文の設定を踏襲してる→論文読まねば…）

  - 各畳み込み層の直後、活性化関数の前にバッチ正規化
  - 重みの初期化：ネットワークをゼロから学習
  - 最適化手法：SGD
    - ミニバッチサイズ：256
    - 学習率：初期値0.1→誤差がピークに達したときに$\frac{1}{10}$
    - 重みの減衰：0.0001
    - モメンタム：0.9
  - ドロップアウトは使わない
  - 10クロップテスト
    - 複数のスケール（{224, 256, 384, 480, 640}）でのスコアを平均


## 主張の有効性の検証方法
- 各データセットを用いてタスクを問いて、性能を評価
  - ImageNet 
  - COCO


## 批評
- SGDのパラメータ、dropoutを使わないという選択、畳み込み層のフィルタのサイズ、層の数はやっぱり職人芸なのかな…


## 次に読むべき論文
- ReNext

  - [Xie, S., Girshick, R., Dollár, P., Tu, Z., & He, K. (2017).  Aggregated residual transformations for deep neural networks. In *Proceedings of the IEEE conference on computer vision and pattern recognition* (pp. 1492-1500).](https://arxiv.org/pdf/1611.05431.pdf)

- バッチ正規化

  - [Ioffe, S., & Szegedy, C. (2015, June). Batch normalization:  Accelerating deep network training by reducing internal covariate shift. In *International conference on machine learning* (pp. 448-456). PMLR.](https://arxiv.org/pdf/1502.03167.pdf)

  

  

