from model import RecognitionModel
import matplotlib.pyplot as plt


def img2latex(img_path):
    model = RecognitionModel()

    l = model.predict('uploaded/2.png',  w=1024, h=192)
    return l