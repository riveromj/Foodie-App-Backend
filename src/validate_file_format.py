import os
from flask import Flask, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime

def validate_file_format(app, new_file):
    file_name = secure_filename(new_file.filename)
    #validar la extension de la foto .jpg o .png
    exten = file_name.rsplit('.')
    if (exten[1].lower()=='jpg' or exten[1].lower()=='png'):
        #validacion si el nombre de la imagen ya existe en db
        if os.path.exists('./src/img/' + file_name):
            now = datetime.now()
            url_Img = str(now).replace(' ', '') + file_name 
        new_file.save(os.path.join('./src/img/', url_Img))
        url = app.config['HOST'] + url_Img
        return url
    else: return None