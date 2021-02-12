import os
from flask import Flask, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime

def validate_file_format(app, new_file):
    file_name = secure_filename(new_file.filename)
    print(new_file, new_file.filename, file_name, "///////////////////")
    #validar la extension de la foto .jpg o .png
    exten = file_name.rsplit('.')
    print(exten, "@@@@@@@@@@@@@@@@@@@")
    if (exten[1].lower()=='jpg' or exten[1].lower()=='png' or exten[1].lower()=='jpeg' ):
        #validacion si el nombre de la imagen ya existe en db
        if os.path.exists('./src/img/' + file_name):
            now = datetime.now()
            url_Img = str(now).replace(' ', '') + file_name 
            print(url_Img, "####################")
        new_file.save(os.path.join('./src/img/', url_Img))
        url = app.config['HOST'] + url_Img
        print(url,"===================")
        return url
    else: 
        print("pero no entré en el if")
        return None
