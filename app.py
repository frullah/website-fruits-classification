from flask import Flask
from flask import request
from flask import render_template
import torch.nn as nn
from torchvision import transforms
import torch
import cv2
import numpy as np
import base64
from net import Net

app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEVICE = "cpu"
MODEL = None

def price_text(price):
    """Give price text to be rendered in HTML"""
    if price == 0:
        return "Gratis"

    return price


def get_price(freshness_percentage):
    return int(freshness_percentage/100*10000)


def get_freshness_percentage(image, model):
    mean = (0.7369, 0.6360, 0.5318)
    std = (0.3281, 0.3417, 0.3704)
    transformations_test = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean, std)
    ])
    img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (32, 32))
    img_as_tensor = transformations_test(img)
    batch = img_as_tensor.unsqueeze(0)
    out = model(batch)
    s = nn.Softmax(dim=1)
    result = s(out)
    return int(result[0][0].item()*100)


@app.route("/", methods=["GET", "POST"])
def upload_predict():
    if request.method == "GET":
        return render_template("index.html")

    image_file = request.files["image"]
    if image_file:
        recognized = recognize(image_file)
        image = recognized["image"]
        pred = recognized["result"]["freshness_level"]
        price = recognized["result"]["price"]
        price = price_text(price)

        # In memory
        image_content = cv2.imencode('.jpg', image)[1].tostring()
        encoded_image = base64.encodestring(image_content)
        to_send = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')
        return render_template(
            "payment.html",
            prediction=pred,
            image_loc=to_send,
            price=price
        )


@app.route('/purchase.html')
def purchase():
    return render_template("purchase.html")


@app.route("/api/recognize", methods=["POST"])
def api_recognize():
    return recognize(request.files["image"])["result"]


def recognize(image_file):
    if image_file:
        image = cv2.imdecode(np.fromstring(
            image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        MODEL = Net()
        MODEL.load_state_dict(torch.load(
            "FreshnessDetector.pt", map_location=torch.device(DEVICE)))
        freshness_percentage = get_freshness_percentage(image, MODEL)
        price = get_price(freshness_percentage)
        return {
            "image": image,
            "result": {
                "freshness_level": freshness_percentage,
                "price": price
            }
        }

