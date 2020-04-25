from flask import render_template,request,abort,current_app as app,jsonify
from .models import Image,db
import traceback
"""
Routes for the backend api
"""
@app.route("/")
def home():
    return render_template('home.html')

@app.route("/store")
def store_images():
    try:
        #get the image url
        #get other details store them in the child database
        #get image details store them in the image database
    except:
        #for checking the app errors
        return jsonify({'trace':traceback.format_exc()})

@app.route("/check")
    try:
        #first do a selective serach through the database
        #select the relative images from the database
        #compare those using the faceverify functionlity
        #return the result if images matces store it in the database otherwise reject the image
        

    except:
        #for checking the app errors
        return jsonify({'trace':traceback.format_exc()})


