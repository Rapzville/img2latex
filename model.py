from PIL import Image
from pix2tex.cli import LatexOCR

def predict(img_path):
    model = LatexOCR()
    img = Image.open(img_path)
        
    res = model(img)

    return res