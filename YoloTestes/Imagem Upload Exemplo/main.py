import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import cv2
import numpy

UPLOAD_FOLDER = 'ficheiros'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "s"

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
       
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        if file and allowed_file(file.filename):
            # filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            caras(request)

    return '''
    <!doctype html>
    <h1>Carrega Ficheiro</h1>
    
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Carrega>
    </form>
    '''

def caras(request):
    img = cv2.imdecode(numpy.fromstring(request.files['file'].read(), numpy.uint8), cv2.IMREAD_UNCHANGED)
    print(img)
    # Processa a Imagem aqui
    cv2.imwrite("ficheiroPNGporqueSim.png", img) # Guarda a imagem processada na bd por exemplo

if __name__ == "__main__":
    app.run(debug=True, port=5000)
