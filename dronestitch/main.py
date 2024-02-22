import os
from flask import Flask, flash, render_template, request, redirect, url_for, session
from flask_session import Session
from urllib.parse import quote as url_quote
from werkzeug.utils import secure_filename
from imageStitching import image_stitch

UPLOAD_FOLDER = './static/input'
OUTPUT_FOLDER = './static/output'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['SESSION_PERMANET'] = False
app.config['SESSION_TYPE']="filesystem"
Session(app)

def allowed_files(filename):
    """ Function to see if the file name is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route("/", methods=['GET', 'POST'])
def index():
    """Function for mainpage and uploading files"""
    if request.method == 'POST':
        if 'fileInput' not in request.files:
            flash('No file part')
            return redirect(url_for('index'))
                
        files = request.files.getlist("fileInput")
        for file in files:
            if file and allowed_files(file.filename):
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                filetype = file.filename.rsplit('.', 1)[1].lower()
                flash('Unaccepted file type '+ filetype +' uploaded. Approved file types are png, jpg and jpeg.')
                return redirect(url_for('index'))

        crop = request.form.get("crop")

        stitched_image = image_stitch(crop, app.config['UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER'])

        #Remove Files
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            os.remove(os.path.join(app.config['UPLOAD_FOLDER'], file))
        
        if stitched_image == False:
            flash('Unable to stitch')
            return redirect(url_for('index'))
             
        return render_template("success.html", output_folder=app.config['OUTPUT_FOLDER'])

    
    for file in os.listdir(app.config['OUTPUT_FOLDER']):
        os.remove(os.path.join(app.config['OUTPUT_FOLDER'], file))
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)