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
def home():
    return render_template('home.html')

@app.route("/store",methods=["POST"])
def store_images():
    try:
        resp = request.json()
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
        return jsonify({'resp':"chid added"})
    except:
        #for checking the app errors
        return jsonify({'resp':traceback.format_exc()})

@app.route("/check",methods=["POST"])
def check_images():
    try:
        resp = request.json()
        im_url = resp['im_url']
        im_details = get_face_details(im_url)
        im_land_centroid = landmark_calc(im_details[0]['faceLandmarks'])
        fid = im_details[0]['faceId']
        gender = im_details[0]['faceAttributes']['gender']
        age = im_details[0]['faceAttributes']['age']
        #first do a selective serach through the database
        images_to_match = Child.query.filter(filter_by=gender)
        #select the relative images from the database
        for i in images_to_match:
            #compare those using the faceverify functionlity
            temp_res = face_compare(i.c_fid,fid)
            #chcek
            #param to be finetuned depending on the requirement of the accuracy of the user
            if(temp_res['cofidence']>0.6):
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
        return jsonify({'resp':"chid matched"})
    except:
        #for checking the app errors
        return jsonify({'trace':traceback.format_exc()})

@app.route("getinfo",methods=["GET"])
def get_info():
    try:
        #retrive each child from the list get the id of child 
        #collect the matches from the child and show it to the user
        child_list = Child.query.all()
        res = {}
        for child in child_list:
            match_list = Match.query.filter_by(c_m_fid = child.c_fid)
            try:
                if(len(match_list)==0):
                    res[(child.name,child.image_url)] = []
                else:
                    res[(child.name,child.image_url)] = [j.image_url for j in match_list]
            except:
                return jsonify({'resp':"error"})
        return jsonify(res)
    except:
        #for checking the app errors
        return jsonify({'trace':traceback.format_exc()})

