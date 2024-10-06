import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from sam2.build_sam import build_sam2
from sam2.sam2_image_predictor import SAM2ImagePredictor

checkpoint = "../checkpoints/sam2.1_hiera_large.pt"
model_cfg = "configs/sam2.1/sam2.1_hiera_l.yaml"
predictor = SAM2ImagePredictor(build_sam2(model_cfg, checkpoint))

# 画像を読み込み
image_path = "gh_sample.jpg"  # ここを実際の画像のパスに置き換えてください
image = np.array(Image.open(image_path))

# 入力プロンプトを定義（例としてポイントを使用）
input_points = np.array([[1532, 1126]])  # 画像内の座標 飛行機
input_points = np.array([[2690, 1094]])  # 画像内の座標 PBB
input_points = np.array([[587, 1423]])  # 画像内の座標 oil
input_points = np.array([[982, 1285]])  # 画像内の座標 BL
input_points = np.array([[2810, 1477]])  # 画像内の座標 towing
input_points = np.array([[2896, 438]])  # 画像内の座標 towing
input_labels = np.array([1])  # 1は正のポイント、0は負のポイント

with torch.inference_mode(), torch.autocast("cuda", dtype=torch.bfloat16):
    predictor.set_image(image)
    masks, _, _ = predictor.predict(
        point_coords=input_points, point_labels=input_labels, multimask_output=True
    )

# 結果を保存
plt.figure(figsize=(10, 10))
plt.imshow(image)
for mask in masks:
    # マスクを半透明で重ねる
    plt.imshow(mask, alpha=0.5)
plt.axis("off")
plt.savefig("output.png", bbox_inches="tight", pad_inches=0)
plt.close()
