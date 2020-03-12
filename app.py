import os
import sqlite3
import Main
import uuid
import shutil

# window testing
import io


from flask import (Flask, jsonify, request, session, g, redirect,
                   url_for, abort, render_template, flash)

from utils import get_project_root

app = Flask(__name__)  # create the application instance

APP_ROOT = get_project_root()

app.config.from_object(__name__)  # load config from this file , flaskr.py
app.config.update(
    # In order to use session in flask you need to set the secret key in your application settings.
    # Secret key is a random key used to encrypt your cookies and save, send them to the browser.
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    # User Name and Password for Login Page saved then as session variale
    USERNAME='admin',
    PASSWORD='default',
)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


@app.route('/', methods=['GET', 'POST'])
def StartApp():
    if request.method == "POST":
        engText = request.form["engText"]
        punjText = request.form["punjText"]
        Output_path_Prefix, Data_path_Prefix = SaveData(engText, punjText)
        output, EngLineCount, PunjLineCount = StartProcessing(
            Output_path_Prefix, Data_path_Prefix)
        return render_template('res.html', Eng_PunjOUTPUT=output, PunjOUTPUT=punjText, EngOUTPUT=engText, EngLineCount=EngLineCount, PunjLineCount=PunjLineCount)
    else:
        return render_template('form.html', Eng_PunjOUTPUT='', PunjOUTPUT='', EngOUTPUT='', EngLineCount='', PunjLineCount='')


def StartProcessing(Output_path_Prefix, Data_path_Prefix):
    output, EngLineCount, PunjLineCount = Main.ComlipreAll(
        Output_path_Prefix, Data_path_Prefix)
    return output, EngLineCount, PunjLineCount


def SaveData(engData, punjData):
    # create Unique Dir for each user
    TEMPDIR = str(uuid.uuid4())
    #TEMPDIR="TEMPFOLDER"
    os.mkdir('./Data/'+TEMPDIR)
    os.mkdir('./Output/'+TEMPDIR)

    #open('./Data/'+TEMPDIR+'/PunjText.pa', 'w').write(punjData)
    #open('./Data/'+TEMPDIR+'/EngText.en', 'w').write(engData)

    # window testing
    io.open('./Data/'+TEMPDIR+'/PunjText.pa', mode="w", encoding="utf8").write(punjData)
    io.open('./Data/'+TEMPDIR+'/EngText.en', mode="w", encoding="utf8").write(engData)


    if os.path.exists('./Data/LangOne.en'):
        os.remove('./Data/LangOne.en')
    Output_path_Prefix = "/Output/"+TEMPDIR
    Data_path_Prefix = "/Data/"+TEMPDIR
    return Output_path_Prefix, Data_path_Prefix



@app.route('/clear', methods=['GET', 'POST'])
def clear():
    result = 1
    folder = os.path.join(APP_ROOT, 'data')
    for the_file in os.listdir(folder):
       file_path = os.path.join(folder, the_file)
       try:
          if os.path.isfile(file_path):
            os.unlink(file_path)
          elif os.path.isdir(file_path):
            shutil.rmtree(file_path)  
       except Exception as e:
          result =0
    
    folder = os.path.join(APP_ROOT, 'output')
    for the_file in os.listdir(folder):
       file_path = os.path.join(folder, the_file)
       try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
       except Exception as e:
          result =0
    
    
    data = {
       'result' : result
    }
    return jsonify(data)
  
