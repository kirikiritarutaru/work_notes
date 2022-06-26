# YOLOv6 ONNX
YOLOv6をonnxruntime-gpuで動かす環境を構築

## 準備
`models`下に下記で変換した`yolov6s.onnx`を配置
- [Convert YOLOv6 ONNX for Inference.ipynb](https://colab.research.google.com/drive/1pke1ffMeI2dXkIAbzp6IHWdQ0u8S6I0n?usp=sharing)

環境構築
- `docker build -t yolov6_onnx .`
- `docker compose up -d`

実行
- `cd ONNX-YOLOv6-Object-Detection`
- `python webcam_object_detection.py`

## 注意
- `yolov6s.onnx`を変換時、入力画像の解像度と設定を合わせないと精度が低下するので注意
  - 推奨: 640×480


# 参考
- [ibaiGorordo/ONNX-YOLOv6-Object-Detection](https://github.com/ibaiGorordo/ONNX-YOLOv6-Object-Detection)
