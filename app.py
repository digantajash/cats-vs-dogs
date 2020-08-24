from flask import Flask,redirect,request,url_for
from flask import render_template as ren
import os
from werkzeug.utils import secure_filename
import uuid
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.models import load_model

app = Flask(__name__)

UPLOAD_PATH = 'uploads'
app.config['UPLOAD_PATH'] = UPLOAD_PATH

def modelcall(filepath):
    model = load_model("cats_vs_dogs_model-v1.h5")
    image = load_img(filepath, target_size = (128, 128))
    sample_image = img_to_array(image)
    prediction = model.predict(sample_image.reshape(-1, *sample_image.shape))[0][0]
    return prediction
@app.route("/")
def home():
    return ren("index.html")



@app.route('/upload-new',methods=['GET','POST'])
def upload_file():
     if request.method == 'POST':

        
        if request.files:

            image = request.files['image']
            id = uuid.uuid1()
            print(image)
            if image:

                filename = image.filename
                # ext =  filename.rsplit(".",1)[1]
                # filename = id.hex + "." + ext  ######### FileName of uploaded file ############
                filename = secure_filename(image.filename)

                file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
                image.save(file_path)
                # return send_from_directory(app.config['UPLOAD_PATH'],
                #                filename)
                label = modelcall(file_path) #Call your model here and return a string or binary
                name = "name"
                if label==1.0:
                    name = 'Dog'
                elif label==0.0:
                    name = 'Cat'
                os.remove(file_path)
                return ren("index.html",label=name)

                
if __name__ == '__main__':
     app.run(debug=True)