# ----------------- Write your code below this line. -------------------- #
import os
from io import BytesIO
from flask import Flask, render_template, request
from config import config
from hotdogclassifier import HotDogClassifier

# Creating an instance means that we’re saying app is an object of Flask and can use any of its methods.
app = Flask(__name__)

model = HotDogClassifier()
model.load_model(config["model_weight"])

# we told Flask that we wanted to URL "/"", or the homepage.
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html", flag=False, project_description=config["project_description"])
# setting the flag = False will make sure that the image only shows up when it’s been uploaded.

@app.route("/", methods=["POST"]) # We use “POST” because the user is sending (“posting”) information to our servers.
def classift():
    uploaded_file = request.files["files"]
    data = BytesIO(uploaded_file.read())
    ''' To be safe, let’s add code that’ll check if an empty file was uploaded. If that’s the case, no prediction should be made.
    If an image was uploaded, then it should predict if the image has a hotdog or not: '''
    if uploaded_file.filename != "":
        img, predicted = model.predict(data)
    else:
        predicted, img = '',''
    return render_template("index.html", predicted=predicted, img=img, flag=True, project_description=config["project_description"], project_name=config["project_name"])

# ----------------- You do NOT need to understand what the code below does. -------------------- #

if __name__ == '__main__':
    PORT = os.environ.get('PORT') or 8080
    DEBUG = os.environ.get('DEBUG') != 'TRUE'
    app.run(host='0.0.0.0', port=PORT, debug=DEBUG)
