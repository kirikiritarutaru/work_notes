# --------------------------------------------------------
# DINOv: Visual In-Context Prompting
# ドラッグでマスクを作成し、推論を実行するコード
# --------------------------------------------------------

import argparse
import os

import cv2
import numpy as np
import torch
from demo import task_openset
from dinov import build_model
from dinov.BaseModel import BaseModel
from PIL import Image
from utils.arguments import load_opt_from_config_file


def parse_option():
    parser = argparse.ArgumentParser('DINOv Inference', add_help=False)
    parser.add_argument('--conf_files', default="configs/dinov_sam_coco_swinl_train.yaml", metavar="FILE", help='設定ファイルへのパス')
    parser.add_argument('--ckpt', default="", metavar="FILE", help='チェックポイントへのパス', required=True)
    parser.add_argument('--target_image', required=True, help='ターゲット画像へのパス')
    parser.add_argument('--visual_prompt_images', nargs='+', help='ビジュアルプロンプト画像へのパス', required=True)
    parser.add_argument('--visual_prompt_masks', nargs='+', help='ビジュアルプロンプト画像へのパス', required=True)
    parser.add_argument('--text_size', default=640, type=int, help='画像リサイズのテキストサイズ')
    parser.add_argument('--hole_scale', default=100, type=int, help='hole_scale パラメータ')
    parser.add_argument('--island_scale', default=100, type=int, help='island_scale パラメータ')
    parser.add_argument('--output', default='output.png', help='出力画像の保存先パス')
    args = parser.parse_args()
    return args


def create_mask_with_drag(image_path, mask_save_path):
    # 画像の読み込み
    image = cv2.imread(image_path)
    clone = image.copy()

    # マスク画像の初期化（黒色）
    mask = np.zeros(image.shape[:2], dtype=np.uint8)

    drawing = False  # マウスが押されているかどうかのフラグ
    ix, iy = -1, -1  # マウスの初期位置

    # マウスイベント時に呼ばれるコールバック関数
    def draw_shape(event, x, y, flags, param):
        nonlocal drawing, ix, iy

        if event == cv2.EVENT_LBUTTONDOWN:
            drawing = True
            ix, iy = x, y

        elif event == cv2.EVENT_MOUSEMOVE:
            if drawing:
                # 直線を描画（表示用）
                cv2.line(image, (ix, iy), (x, y), color=(0, 255, 0), thickness=5)
                # マスク画像にも線を描画（白色）
                cv2.line(mask, (ix, iy), (x, y), color=255, thickness=5)
                ix, iy = x, y

        elif event == cv2.EVENT_LBUTTONUP:
            drawing = False
            # 最後の線を描画
            cv2.line(image, (ix, iy), (x, y), color=(0, 255, 0), thickness=5)
            cv2.line(mask, (ix, iy), (x, y), color=255, thickness=5)

    # ウィンドウの作成とコールバック関数の設定
    cv2.namedWindow("image")
    cv2.setMouseCallback("image", draw_shape)

    print("画像ウィンドウ上でドラッグしてマスクを描画します。終了するには 'q' キーを押してください。")

    while True:
        # 画像の表示
        cv2.imshow("image", image)
        key = cv2.waitKey(1) & 0xFF

        # 'r' キーでリセット
        if key == ord("r"):
            image = clone.copy()
            mask = np.zeros(image.shape[:2], dtype=np.uint8)
            print("画像とマスクをリセットしました。")

        # 'q' キーで終了
        elif key == ord("q"):
            break

    # ウィンドウの破棄
    cv2.destroyAllWindows()

    # マスク画像の保存
    cv2.imwrite(mask_save_path, mask)
    print(f"マスク画像を {mask_save_path} に保存しました。")


def load_visual_prompt_mask(image_path, mask_path):
    # 画像の読み込み
    image = Image.open(image_path).convert("RGB")
    # マスク画像の読み込み（グレースケール）
    mask = Image.open(mask_path).convert("L")
    # マスク画像をRGBに変換
    mask = mask.convert("RGB")
    return image, mask


def main():
    args = parse_option()

    # モデルの構築
    opt = load_opt_from_config_file(args.conf_files)
    model = BaseModel(opt, build_model(opt)).from_pretrained(args.ckpt).eval().cuda()

    # ターゲット画像の読み込み
    image_tgt = Image.open(args.target_image).convert("RGB")

    # ビジュアルプロンプトの読み込みとマスクの生成
    visual_prompt_images = args.visual_prompt_images
    visual_prompt_masks = args.visual_prompt_masks

    in_context_examples = []
    for img_path, mask_path in zip(visual_prompt_images, visual_prompt_masks):
        # 画像とマスクを読み込む
        image, mask = load_visual_prompt_mask(img_path, mask_path)
        in_context_examples.append({'image': image, 'mask': mask})

    # in_context_examples を8つの要素にパディング
    while len(in_context_examples) < 8:
        in_context_examples.append(None)

    # 推論の実行
    with torch.no_grad():
        with torch.autocast(device_type='cuda', dtype=torch.float16):
            result = task_openset(
                model,
                in_context_examples[0],
                in_context_examples[1],
                in_context_examples[2],
                in_context_examples[3],
                in_context_examples[4],
                in_context_examples[5],
                in_context_examples[6],
                in_context_examples[7],
                image_tgt=image_tgt,
                text_size=args.text_size,
                hole_scale=args.hole_scale,
                island_scale=args.island_scale
            )

    # 結果の保存
    result_image = Image.fromarray(result)
    result_image.save(args.output)
    print(f"結果が {args.output} に保存されました")


if __name__ == '__main__':
    main()
