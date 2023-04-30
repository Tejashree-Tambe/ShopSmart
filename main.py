from flask import Flask, render_template, Response,redirect,request
from camera import VideoCamera
import os
import sys
import json
from recommend import extract_img_features,model, features_list, recommend, img_files_list

app = Flask(__name__)

products = ["1.png", "2.png", "3.png", "4.png"]

product_list = {
     "products": [
     {
        "name": "1.png",
        "description": "Pink",
        "price": 'Rs. 121',
     },

     {
        "name": "2.png",
        "description": "Pink",
        "price": 'Rs. 145',
     },

     {
        "name": "3.png",
        "description": "Pink",
        "price": 'Rs. 130',
     },

     {
        "name": "4.png",
        "description": "Pink",
        "price": 'Rs. 160',
     }
     ]
}
price = ["Rs.121", "Rs.131", "Rs.141", "Rs.121"]

CART=[]

def path_in_static(prev_path):
    return "static/"+prev_path

@app.route('/checkOut')
def checkOut():
    return render_template('checkout.html')

""" @app.route('/tryon/<file_path>',methods = ['POST', 'GET'])
def tryon(file_path):
    file_path = file_path.replace(',','/')
    os.system('python tryOn.py ' + file_path)
    return redirect('http://127.0.0.1:5000/',code=302, Response=None) """

@app.route('/tryall',methods = ['POST', 'GET'])
def tryall():
        CART = request.form['mydata'].replace(',', '/')
        os.system('python test.py ' + CART)
        return render_template('checkout.html', message='')

@app.route('/recommend',methods = ['POST', 'GET'])
def recommendation():
    #print(request.files["img"].mimetype)

    # save image
    # mime_to_ext={"image/png":".png", "image/jpg":".jpg", "image/jpeg":".jpeg"}
    # img_file=request.files["img"]
    # file_name=img_file.name + mime_to_ext[img_file.content_type]
    # file_path=os.path.join("uploader", file_name)
    # img_file.save(file_path)

    
    file_path=request.json.get("img_path")

    #feature extraction
    features = extract_img_features(file_path, model)

    # #recommend
    img_indices = recommend(features, features_list)
    
    #render
    items=[]
    for i in range(0,4):
        items.append(path_in_static(img_files_list[img_indices[0][i]]))
    print(items)

    return items
    # return render_template('product.html', product_list=product_list, items=items)


@app.route('/')
def indexx():
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/product')
def product():
    return render_template('product.html', product_list=product_list)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route("/cart/<file_path>",methods = ['POST', 'GET'])
def cart(file_path):
    global CART
    file_path = file_path.replace(',','/')
    print("ADDED", file_path)
    CART.append(file_path)
    return render_template("checkout.html")

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    if not os.path.exists("uploader"):
        os.makedirs("uploader")
    app.run(debug=True)