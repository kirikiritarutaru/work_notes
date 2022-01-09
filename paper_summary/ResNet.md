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

<img src="/home/taru/src/work_notes/paper_summary/picture/residual block.png" alt="residual block" style="zoom:150%;" />

- Residual Network

  - 畳み込み層33層、最後にFC層1層
  - 入力と出力の次元数が同じである場合、スキップ接続はそのまま
  - 入力の次元数よりも出力の次元数が大きい場合（＝**次元数が同じではない場合**）、選択肢は２つ（←細かいとこやな）

    1. 次元が大きくなったぶんゼロパディングを追加して、（無理やり）恒等写像←パラメータは増えないよ
    2. 線形写像 $W_s$ を噛ませて、 $y=\mathcal{F}(x,\{W_i\})+W_sx$ として、次元を合わせる。
  - どちらのオプションでもショートカットが2つのサイズの特徴マップにまたがる場合、ストライドを2にして実行

  

- 深いResidual Network（50層〜）

  - 計算量を抑えるため、ボトルネックアーキテクチャを採用
  - ボトルネックアーキテクチャについて（←実験の章で言及するのおかしくね？）
    - residual blockを深くすると
      - 利点：精度があがる
      - 欠点：パラメータ数が膨大になって、学習に時間がかかる
    - そこで、ResNet 50層/101層/152層では**ボトルネック・アーキテクチャ**を採用
      - 1×1, 3×3, 1×1の畳み込み層3つを用いたブロック
        - 入力256chとすると、高次元(256)→低次元(64)→高次元(256)と遷移し、出力256ch
      - 下の２つブロックは時間計算量が同程度なのに、扱えるch数が4倍に
        - 入力64ch→出力64chのresidual block
        - 入力256ch→出力256chのボトルネックアーキテクチャ

  

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
- 画像認識タスクで性能を比較
  - ImageNet 
    - Residual blockのありなしで実験
      - プレーンなネットワーク18層・34層、ResNet18層・34層でImageNetの画像認識のタスクを実験
      - ResNet34層が最も良い結果
      - ResNet34層でも、3つのパターンで実験。どれも性能変わらず
        （3が微差でいいが、著者曰くパラメータ増えたからではとのこと）
        - 次元大きくなったぶんゼロパディング
        - 次元大きくなるところ**だけ**線形写像 $W_s$ を噛ませる
        - 全てのショートカットで線形写像 $W_s$ を噛ませる

    - さらに深い50層・101層・152層のResNetを構築

      - ボトルネックアーキテクチャを採用

      - 計算量
        - 50層ResNet：38億FLOPs
        - 152層ResNet：113億FLOPｓ
        - （参考　VGG-16/19：153/196億FLOPs）

      - 精度
        - 34層ResNetと比較して、数％ポイントも良い
  - CIFAR-10
    - ResNetの層の深さと精度の関係を調査
      - ResNet-20, 32, 44, 56, 110, 1202で実験
      - 110までは層を深くするほど精度向上
      - 実装詳細
        - 重みの減衰：0.0001
        -  momentum：0.9
        - 重みの初期化：
          - [K. He, X. Zhang, S. Ren, and J. Sun. Delving deep into rectifiers: Surpassing human-level performance on magenet classification. In ICCV, 2015.](https://arxiv.org/pdf/1502.01852.pdf)
        - BNあり
        - ドロップアウトなし
        - ミニバッチサイズ：128
        - データオーグメンテーション：
          - 各辺に4pixのパディング
          - パディングされた画像を水平方向の反転し画像増やす
          - 32×32のクロップをランダムサンプリング
          - テストではもとの32×32の単一画像のみを評価
- 物体検知タスクで性能を比較
  - タスク
    - PASCAL
    - MS COCO
      - COCO 2015 で the 1st place
  - Faster R-CNNのバックボーンにResNet-101を使い、工夫を3つ (box refinement, context, multi-scale testing) 加えたモデルで大体SOTA
    - box refinement
      - S. Gidaris and N. Komodakis. Object detection via a multi-region & semantic segmentation-aware cnn model. In ICCV, 2015. の論文で提案
      - Faster R-CNNでは、最終的な出力は提案ボックスとは異なる回帰されたボックス
      - 推論のために、回帰されたボックスから新しい特徴を抽出し、新しく分類スコアと回帰されたボックスを得る
      - 300個の予測値ともとの300個の予測値をアンサンブル
      - 新しい予測ボックスを収斂し、多数決
    - Global context
      - 画像全体のバウンディングボックスを使用して[ピラミッドプーリング](https://arxiv.org/abs/1406.4729)により特徴を抽出し、グローバルコンテキスト特徴量を得る
      - もとの領域ごとの特徴と連結して、新しく分類スコアと回帰ボックスを得る
    - multi-scale testing
      - 特徴ピラミッドから、隣接する2つのスケールを選択
      - RoIプーリングとその後のレイヤーを2つのスケールの特徴マップに実行
      - maxout レイヤーにより統合
      - 詳しくは[S. Ren, K. He, R. Girshick, X. Zhang, and J. Sun. Object detection networks on convolutional feature maps. arXiv:1504.06066, 2015.](https://arxiv.org/abs/1504.06066)を読んでね

## 批評
- SGDのパラメータ、dropoutを使わないという選択、畳み込み層のフィルタのサイズ、層の数はやっぱり職人芸なのかな…
- ResNetの次元増えるところのスキップ接続の細かいところ、解説記事に書いてないよなぁ。ちゃんと原論文にあたらないと。枝葉だけど
  - 耳年増になるのは避けたいね
- [weight decayまわりの話](https://twitter.com/icoxfog417/status/931417538407235584?ref_src=twsrc%5Etfw%7Ctwcamp%5Etweetembed%7Ctwterm%5E931417538407235584%7Ctwgr%5E%7Ctwcon%5Es1_&ref_url=https%3A%2F%2Farakan-pgm-ai.hatenablog.com%2Fentry%2F2018%2F04%2F16%2F100000)
  - SGDの場合、正則化としてL2正則= weight decayとして使うとうまくいくことが多いよ
  - weight decay = 0.0001　にしたらいいかな
  - Adamの場合は正則化として効かないよ
  - 詳しくは論文読んでね！
    - 参考：[過学習抑制「Weight Decay」はSGDと相性が良く、Adamと良くない？／NNCで確かめる](https://arakan-pgm-ai.hatenablog.com/entry/2018/04/16/100000)
      - **自分で確かめよう！！**
- 物体検知タスクの方、いろんな論文の工夫をアドホックに組み合わせたんですか？
  - 工夫による精度向上が、VGG-16→ResNet-101に変更したときの精度向上よりも大きいですが…
  - ResNet自体の性能へのコントリビューションを調べるという意味では疑問符が付きますね
  - まぁ、ResNetが物体検知で強いのを示すというよりも一位とるために様々な工夫を凝らしましたということなのかな

## 次に読むべき論文
- ReNext

  - [Xie, S., Girshick, R., Dollár, P., Tu, Z., & He, K. (2017).  Aggregated residual transformations for deep neural networks. In *Proceedings of the IEEE conference on computer vision and pattern recognition* (pp. 1492-1500).](https://arxiv.org/pdf/1611.05431.pdf)

- バッチ正規化

  - [Ioffe, S., & Szegedy, C. (2015, June). Batch normalization:  Accelerating deep network training by reducing internal covariate shift. In *International conference on machine learning* (pp. 448-456). PMLR.](https://arxiv.org/pdf/1502.03167.pdf)

  

  

