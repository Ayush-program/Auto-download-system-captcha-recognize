import os, json, zipfile
import cv2
import numpy as np
import torch
import torch.nn as nn


class CaptchaCNN(nn.Module):
    def __init__(self, num_classes):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            nn.Conv2d(32, 32, 3, padding=1), nn.BatchNorm2d(32), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), nn.Dropout2d(0.25),

            nn.Conv2d(32, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            nn.Conv2d(64, 64, 3, padding=1), nn.BatchNorm2d(64), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), nn.Dropout2d(0.25),

            nn.Conv2d(64, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            nn.Conv2d(128, 128, 3, padding=1), nn.BatchNorm2d(128), nn.ReLU(inplace=True),
            nn.MaxPool2d(2, 2), nn.Dropout2d(0.25),
        )

        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(128 * 8 * 4, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(0.5),
            nn.Linear(512, num_classes),
        )

    def forward(self, x):
        return self.classifier(self.features(x))


class CaptchaOCR:

    def __init__(self, zip_path):

        extract_dir = "./captcha_model_files"
        os.makedirs(extract_dir, exist_ok=True)

        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(extract_dir)

        config_path = os.path.join(extract_dir, "captcha_config.json")

        with open(config_path) as f:
            cfg = json.load(f)

        self.charset = cfg["charset"]
        self.num_classes = cfg["num_classes"]
        self.captcha_len = cfg["captcha_len"]
        self.img_w = cfg["img_w"]
        self.img_h = cfg["img_h"]
        self.char_h = cfg["char_h"]
        self.char_w = cfg["char_w"]

        self.idx_to_c = {i: c for i, c in enumerate(self.charset)}

        model_path = os.path.join(extract_dir, "captcha_model.pth")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        checkpoint = torch.load(model_path, map_location=self.device)

        self.model = CaptchaCNN(self.num_classes).to(self.device)
        self.model.load_state_dict(checkpoint["model_state"])
        self.model.eval()


    def _preprocess(self, img_path):

        img = cv2.imread(img_path)

        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        blue = cv2.inRange(hsv, np.array([85,50,30]), np.array([145,255,255]))
        img[blue > 0] = [255,255,255]

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        _, binary = cv2.threshold(gray,0,255,
        cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))
        clean = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

        result = cv2.bitwise_not(clean)

        return cv2.resize(result,(self.img_w,self.img_h))


    def predict(self, img_path):

        processed = self._preprocess(img_path)

        slot = self.img_w // self.captcha_len

        crops = []

        for i in range(self.captcha_len):

            crop = processed[:, i*slot:(i+1)*slot]

            crop = cv2.resize(crop,(self.char_w,self.char_h))

            crop = crop.astype(np.float32)/255.0

            crops.append(crop)

        tensor = torch.tensor(
            np.array(crops)[:,None,:,:],
            dtype=torch.float32
        ).to(self.device)

        with torch.no_grad():

            preds = self.model(tensor)

            preds = torch.argmax(preds,1).cpu().numpy()

        return "".join(self.idx_to_c[p] for p in preds)


# 🚀 LOAD MODEL ONLY ONCE
#ocr = CaptchaOCR(r"C:\Users\DELL\Downloads\main_code\main_code_result\Captcha_solver\captcha_ocr_final.zip")


"""def predict_captcha(img_path):

    return ocr.predict(img_path)

"""
# example
#print(predict_captcha(r"C:\Users\DELL\Downloads\main_code\main_code\Captcha_solver\temp_img\captcha_0009.png"))