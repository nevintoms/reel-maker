import os
import cv2


def save_image(img, file_path):
    cv2.imwrite(file_path, img)
    print(f"Saved frame {os.path.basename(file_path)}")
