import os
from flask import Flask, send_file
from werkzeug.utils import secure_filename
from werkzeug.datastructures import ImmutableMultiDict
from datetime import datetime
from cloudinary.uploader import upload

def validate_file_format(app, new_file):
    file_name = secure_filename(new_file.filename)
    exten = file_name.replace(' ', '').rsplit('.')
    
    if (exten[1].lower()=='jpg' or exten[1].lower()=='png' or exten[1].lower()=='jpeg' ):
        #validacion si el nombre de la imagen ya existe en db
        # url_Img = file_name
        # if os.path.exists('./src/img/' + file_name):
        #     now = datetime.now()
        #     url_Img = str(now).replace(' ', '') + file_name 
           
        upload_image = upload(new_file)
        
        return upload_image['url']
    else: 
        print("pero no entré en el if")
        return None
