from key import subscription_key,face_api_url,face_api_url_verify,headers
import requests

def get_face_details(image_url):
    """
    This function take the face id of the preson from the image url
    Args:
        image_url: image_url from the blob storage of the person
    Returns:
        face_details : It returns the details of the face using the azuer api
        as as json response
    """
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks':'true',
        'returnFaceAttributes': 'age,gender',
        'returnRecognitionModel':'true',
        'recognitionModel':'recognition_02'
    }
    response = requests.post(face_api_url, params=params,
                         headers=headers, json={"url": image_url})
    return response.json()


def face_compare(id_1, id_2):
    """ Determine if two faceIDs are for the same person   
    Args:
        id_1: faceID for person 1
        id_2: faceID for person 2
        
    Returns:
        json response: Full json data returned from the API call
        
    """
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key
    }

    body = {"faceId1": id_1, "faceId2": id_2}

    params = {}
    response = requests.post(face_api_url_verify,
                             params=params,
                             headers=headers,
                             json=body)
    return response.json()

def landmark_calc(resp):
    """ A Comparison of Face Veriﬁcation with Facial Landmarks and Deep Features
        This paper is incoporated we are not using the landmarks for the detection of the images
        We are mainly using the feature to find the relevent images which can be a match and it is used
        with several other factors.

    Arguments:
        resp[dict]: Dict response given to the function containg the facial features

    Returns:
        returns the calculated centroid value using the points
    """
    return 0
