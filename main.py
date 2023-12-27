# pip install flask flask_qrcode pyngrok
from flask import Flask,render_template,request
from flask_qrcode import QRcode
from werkzeug.utils import secure_filename
import os

app = Flask(__name__,static_folder="static", static_url_path="/static",template_folder="templates")
qrcode = QRcode(app)
port_number = 5000
shared_url = "http://127.0.0.1:"+str(port_number)

@app.route("/upload",methods=['POST', 'GET'])
def upload():
    if request.method == "POST":
        request_file = request.files['file']
        filename  = secure_filename(request_file.filename)
        basepath = os.path.dirname(__file__)  # now file path
        upload_path = os.path.join(basepath, 'static\\upload', filename)
        request_file.save(upload_path)
        # if upload sucessed goto the show html
        return render_template("qr.html", url = shared_url,filename = filename)
    return render_template("upload.html")

@app.route("/show")
def show():
    filename = request.args.get("filename")
    return render_template("show.html", url=shared_url,filename=filename)

from pyngrok import ngrok
ngrok_auth_key = "your_ngrok_key"
if __name__ == '__main__':
    if ngrok_auth_key!="":
        ngrok.set_auth_token(ngrok_auth_key)
        public_url = ngrok.connect(port_number).public_url
        print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port_number))
        shared_url = public_url
    app.run()