import base64
import requests
import json

import compare_face as cf

URL = 'https://32cr6t0aoh.execute-api.us-east-1.amazonaws.com/default/lambda-create-user'

def test_create_record1():
    image_file = open("/Users/duan/Pictures/2018-11-27/1.png", "rb")
    #encoded_string = base64.b64encode(image_file.read())
    encoded_string = image_file.read()
    body = {"name": "Alice520", "data": encoded_string}
    cf.create_record(body)


def test_create_record2():
    image_file = open("/Users/duan/Pictures/2018-11-27/7.png", "rb")
    #encoded_string = base64.b64encode(image_file.read())
    encoded_string = image_file.read()
    body = {"name": "Mary", "data": encoded_string}
    cf.create_record(body)


def test_get_record():
    image_file = open("/Users/duan/Pictures/2018-11-27/2.png", "rb")
    encoded_string = base64.b64encode(image_file.read())
    body = {"data": encoded_string}

    print(cf.get_record(body))


def test_del_record(name):
    body = {"name": name}
    cf.del_record(body)

def test_update_record():
    #test_get_record()
    print(cf.update_record(None))


def test_compare_face():
    response = cf.rekognition.compare_faces(
        SourceImage={
            "S3Object": {
                "Bucket": cf.BUCKET_NAME,
                "Name": 'Mary',
            }
        },
        TargetImage={
            "S3Object": {
                "Bucket": cf.BUCKET_NAME,
                "Name": 'Alice520',
            }
        },
        SimilarityThreshold=cf.COMPARE_THRESHOLD)

    if not response['FaceMatches']:
        result = 0
    else:
        result = response['FaceMatches']['Similarity']
    return result


def test_compare_face2():
    image_file = open("/Users/duan/Pictures/2018-11-27/7.png", "rb")
    #encoded_string = base64.b64encode(image_file.read())
    encoded_string = image_file.read()
    result = cf.compare_faces(encoded_string, 'Alice520')
    print(result)


def test_put():
    #header = {'Content-type': 'application/json'}
    payload = {
        'name': 'Alice'
        #'grant_type': 'authorization_code',
        #'code': request.args['code'],
        #'state': request.args['state'],
        #'redirect_uri': 'http://xxx.xyz.com/request_listener',
    }

    response = requests.put(URL, data=json.dumps(payload))
    print(response.content)


def test_post():
    image_file = open("/Users/duan/Pictures/2018-11-27/2.png", "rb")
    encoded_string = base64.b64encode(image_file.read())
    # body = {"data": encoded_string}
    # data = image_file.read()

    payload = {
        'name': 'Alice210',
        'data': encoded_string.decode('utf-8')
        #'grant_type': 'authorization_code',
        #'code': request.args['code'],
        #'state': request.args['state'],
        #'redirect_uri': 'http://xxx.xyz.com/request_listener',
    }

    response = requests.post(URL, data=json.dumps(payload))
    print(response.content)


def test_get():
    image_file = open("/Users/duan/Pictures/2018-11-27/4.png", "rb")
    encoded_string = base64.b64encode(image_file.read())

    payload = {
        'data': encoded_string.decode('utf-8')
        #'grant_type': 'authorization_code',
        #'code': request.args['code'],
        #'state': request.args['state'],
        #'redirect_uri': 'http://xxx.xyz.com/request_listener',
    }

    response = requests.get(URL, data=json.dumps(payload))
    print(response.content)


test_get()

