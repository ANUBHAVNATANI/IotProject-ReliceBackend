"""Testing code for the backend API and database
"""
from utils import face_compare,get_face_details
fid1 = get_face_details("https://i.imgur.com/dICEa1R.jpg")[0]['faceId']
fid2 = get_face_details("https://i.imgur.com/TuHZ2Z6.jpg")[0]['faceId']
tempRes = face_compare(fid1,fid2)
print(tempRes)