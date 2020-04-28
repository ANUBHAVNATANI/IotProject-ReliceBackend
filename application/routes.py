from flask import render_template,request,abort,current_app as app,jsonify
import traceback
import json
from utils import get_face_details,landmark_calc,face_compare
from .models import Child,Match
from . import db

"""
Routes for the backend api
"""

@app.route("/")
@cross_origin(supports_credentials=True)
def home():
    return render_template('home.html')

@app.route("/store",methods=["POST"])
@cross_origin(supports_credentials=True)
def store_images():
    try:
        resp = request.json
        #get the image url
        im_url = resp['im_url']
        #get other details store them in the child database
        name = resp['name']
        age = resp['age']
        gender = resp['gender']
        #get image details store them in the image database
        im_details = get_face_details(im_url)
        im_land_centroid = landmark_calc(im_details[0]['faceLandmarks'])
        fid = im_details[0]['faceId']
        new_child = Child(c_fid=fid,im_land_centroid=im_land_centroid,name=name,age=age,image_url=im_url,
        gender=gender)
        db.session.add(new_child)
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'resp':e})
        finally:
            db.session.close()
        return jsonify({'resp':"CADDED"})
    except:
        #for checking the app errors
        return jsonify({'resp':traceback.format_exc()})

@app.route("/check",methods=["POST"])
@cross_origin(supports_credentials=True)
def check_images():
    try:
        resp = request.json
        im_url = resp['im_url']
        im_details = get_face_details(im_url)
        #print(im_details)
        im_land_centroid = landmark_calc(im_details[0]['faceLandmarks'])
        fid = im_details[0]['faceId']
        gender = im_details[0]['faceAttributes']['gender']
        age = im_details[0]['faceAttributes']['age']
        #first do a selective serach through the database
        images_to_match = Child.query.filter_by(gender=gender)
        #select the relative images from the database
        for i in images_to_match:
            #compare those using the faceverify functionlity
            #print(i.c_fid,fid)
            temp_res = face_compare(i.c_fid,fid)
            #chcek
            #param to be finetuned depending on the requirement of the accuracy of the user
            #print(temp_res)
            if(temp_res['confidence']>0.6):
                new_match = Match(m_fid=fid,im_land_centroid=im_land_centroid,age=age,image_url=im_url,gender=gender,c_m_fid=i.c_fid)
                db.session.add(new_match)
                try:
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    return jsonify({'resp':e})
                finally:
                    db.session.close()
        #return the result if images matces store it in the database otherwise reject the image
        return jsonify({'resp':"CMATCHED"})
    except:
        #for checking the app errors
        return jsonify({'trace':traceback.format_exc()})

@app.route("/getinfo",methods=["GET"])
@cross_origin(supports_credentials=True)
def get_info():
    try:
        #retrive each child from the list get the id of child 
        #collect the matches from the child and show it to the user
        child_list = Child.query.all()
        res = {}
        for child in child_list:
            match_list = Match.query.filter_by(c_m_fid = child.c_fid)
            try:
                res[child.image_url] = (child.name,[match.image_url for match in match_list])
            except:
                return jsonify({'resp':"error"})
        return jsonify(res)
    except:
        #for checking the app errors
        return jsonify({'trace':traceback.format_exc()})

"""
Routes only for the testing purpose 
"""
"""
@app.route("/checkdata",methods=["GET"])
def get_data():
    try:
        child = Child.query.all()
        for i in child:
            print(i.c_fid)
            print(i.im_land_centroid)
            print(i.image_url)
            print(i.matches)
        match = Match.query.all()
        for j in match:
            print(j.m_fid)
            print(j.im_land_centroid)
            print(j.image_url)
            print(j.age)
            print(j.gender)
            print(j.c_m_fid)    
        return jsonify({'resp':"success"})
    except:
        return jsonify({'trace':traceback.format_exc()})
"""

@app.route("/cleardatabase",methods=["GET"])
def get_data():
    try:
        child = Child.query.delete()
        match = Match.query.delete()
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'resp':e})
        finally:
            db.session.close()
        return jsonify({'resp':"success"})
    except:
        return jsonify({'trace':traceback.format_exc()})