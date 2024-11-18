import onnxruntime as rt
import numpy as np
import cv2
from tqdm import tqdm
import shutil
import json

class RecognitionModel:
    def __init__(self):
        providers = ['CPUExecutionProvider']
        self.model = rt.InferenceSession('./model.onnx', providers=providers)
        self.output_name = self.model.get_outputs()[0].name
        self.input_name = self.model.get_inputs()[0].name
        self.ltx_index = json.load((open('keys.json')))

    def predict(self, img_path, w, h):
        img = self.load(img_path, w, h)
        res = self.model.run([self.output_name], {self.input_name: img})[0][0]
        res = np.argmax(res, axis=1)

        l = ''.join([self.ltx_index[str(x - 1)] if x != 0 else ' ' for x in res])

        return l
    
    def resize(self, img, w=256, h=256):
        p = max(img.shape[:2] / np.array([h, w]))
        s = img.shape[:2]
        r = s / p
        
        img = cv2.resize(img, (int(r[1]), int(r[0])))

        re = np.zeros((h, w, 3))
        offset = np.array((np.array(re.shape[:2]) - np.array(img.shape[:2])) / 2, dtype=np.int32)
        re[offset[0]:offset[0] + img.shape[0], offset[1]:offset[1] + img.shape[1]] = img
        return re

    def load(self, image_file, w, h):
        i = cv2.imread(image_file)[...,::-1]
        input_image = self.resize(i, w, h) / 255
        return input_image[None].astype(np.float32)