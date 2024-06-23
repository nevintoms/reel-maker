import os
import cv2


def save_image(img, file_path, logger):
    cv2.imwrite(file_path, img)
    logger.info(f"Saved frame {os.path.basename(file_path)}")
