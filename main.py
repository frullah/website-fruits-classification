import os
from flask import Flask
from flask import request
from flask import render_template
import torch.nn.functional as F
import torch.optim as optim
import torch.nn as nn
from torchvision import transforms
import torch
import cv2
import numpy as np
import base64



app = Flask(__name__)
UPLOAD_FOLDER = "static"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
DEVICE = "cpu"
MODEL = None

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(3,16,kernel_size=3,padding=1)
        self.conv2 = nn.Conv2d(16,8,kernel_size=3,padding=1)
        self.fc1 = nn.Linear(8*8*8,32)
        self.fc2 = nn.Linear(32,2)
    def forward(self,x):
        out = F.max_pool2d(torch.tanh(self.conv1(x)),2)
        out = F.max_pool2d(torch.tanh(self.conv2(out)),2)
        out = out.view(-1,8*8*8)
        out = torch.tanh(self.fc1(out))
        out = self.fc2(out)
        return out


def predict(image, model):
    mean = (0.7369, 0.6360, 0.5318)
    std = (0.3281, 0.3417, 0.3704)
    transformations_test = transforms.Compose([
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean,std)
                                      ])
    img = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    img = cv2.resize(img,(32,32))
    img_as_tensor = transformations_test(img)
    s = nn.Softmax(dim=1)
    batch = img_as_tensor.unsqueeze(0)
    out = model(batch)
    print(model)
    fresh_percent = s(out)

    return int(fresh_percent[0][0].item()*100)

def price(image, model):
    mean1 = (0.7369, 0.6360, 0.5318)
    std1 = (0.3281, 0.3417, 0.3704)
    transformations_test1 = transforms.Compose([
                                      transforms.ToTensor(),
                                      transforms.Normalize(mean1,std1)
                                      ])
    img1 = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    img1 = cv2.resize(img1,(32,32))
    img_as_tensor1 = transformations_test1(img1)
    s1 = nn.Softmax(dim=1)
    batch1 = img_as_tensor1.unsqueeze(0)
    out1 = model(batch1)
    print(model)
    fresh_percent1 = s1(out1)
    value = int(fresh_percent1[0][0].item()*100)
    if value != 0 :
        return int(value/100*10000)
    elif value == 99 :
        return "Masih Fresh"
    elif value == 0 :
        return "Gratis"


@app.route("/", methods=["GET", "POST"])
def upload_predict():
    if request.method == "POST":
        image_file = request.files["image"]
        if image_file:
            recognized = recognize(image_file)
            image = recognized["image"]
            pred = recognized["result"]["freshness_level"]
            prices = recognized["result"]["price"]
            
            # In memory
            image_content = cv2.imencode('.jpg', image)[1].tostring()
            encoded_image = base64.encodestring(image_content)
            to_send = 'data:image/jpg;base64, ' + str(encoded_image, 'utf-8')
            return render_template("payment.html", prediction=pred, image_loc=to_send, fullprice=prices)
    return render_template("index.html")

@app.route('/purchase.html')
def purchase():
    return render_template("purchase.html")

@app.route("/api/recognize", methods=["POST"])
def api_recognize():
    return recognize(request.files["image"])["result"]

def recognize(image_file):
    if image_file:
        image = cv2.imdecode(np.fromstring(image_file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        MODEL = Net()
        MODEL.load_state_dict(torch.load("FreshnessDetector.pt", map_location=torch.device(DEVICE)))
        freshness_level = predict(image, MODEL)
        prices = price(image, MODEL)
        return {
            "image": image,
            "result": {
             "freshness_level": freshness_level,
             "price": prices 
            }
        }

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
