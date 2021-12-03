- - Understanding Human Hands in Contact at Internet Scale
  
    - [Dandan Shan](https://arxiv.org/search/cs?searchtype=author&query=Shan%2C+D), [Jiaqi Geng](https://arxiv.org/search/cs?searchtype=author&query=Geng%2C+J), [Michelle Shu](https://arxiv.org/search/cs?searchtype=author&query=Shu%2C+M), [David F. Fouhey](https://arxiv.org/search/cs?searchtype=author&query=Fouhey%2C+D+F)
    - CVPR 2020 (Oral)
    - [論文](https://arxiv.org/abs/2006.06669)
    - [プロジェクトページ](https://fouheylab.eecs.umich.edu/~dandans/projects/100DOH/)
  
    ## 概要
  
    -  論文のコントリビューションは主に3つ
       1. シーン内での手と物体の接触に関する情報を得る手法
       2. 大規模データセット作成
          - 手で物体に接触している動画を大量に収集
          - 豊富な情報をアノテーション
       3. 上記データセットで学習したモデルの応用例の検討
    -  ネットにあるペタバイト級の動画データから手の状態の情報を抽出することが著者らの目標
  
    ## 問題設定と解決したこと
  
    - 手は人間が世界とインタラクションするための中心的存在
      - 既存の研究は実験室内での作業に焦点をあてたものばっかり
      - 実際の動画（インターネット上の動画など）は、視点やコンテクストの多様さがマジパネェ
      - 実験室での作業に対するアプローチを適用するのマジムリ
    - **多様な動画**から**手に関する情報を得る**問題を解く
    - 手の情報を得る手法の検討と学習するためのデータセットを作成
  
    ## 何をどう使ったのか
  
    - データセット 100DOH 作成
      - 100日以上の動画収集
        - youtubeから収集
        - ※すべてにアノテーションがあるわけではない
      - 動画の10万フレームにアノテーション
        - 手のバウンディングボックス
          - ＋右手か左手かの情報
        - 手とcontactしている物体のバウンディングボックス
        - 手と物体のcontact状態
          - なし/自分に接触/他人に接触/持ち運べない物に接触/持ち運べる物に接触
  
    ## 主張の有効性の検証方法
  
    - 100DOHで学習したモデルを以下5種類のデータセットでテスト。高い汎化性能を確認
      - VLOG
      - VIVA
      - EgoHands
      - VGGHands
      - TV+Co
    - モデルはFaster-RCNN
      - 手と手を接触している物体を検出するように学習
  
    ## 批評
  
    - モデルの新規性はあまりない
    - データセットのアノテーションのやばさがやばい
  
    ## 次に読むべき論文
  
    -  Faster-RCNN
