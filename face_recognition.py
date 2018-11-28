from __future__ import print_function # Python 2/3 compatibility
import base64
import boto3
import json
import decimal


print('Loading function')

BUCKET_NAME = 'face-recognition-2018'
TABLE_NAME = 'face-recognition-2018'
REGION = 'us-east-1'
COMPARE_THRESHOLD = 85

dynamo = boto3.resource('dynamodb')
table = dynamo.Table(TABLE_NAME)

s3 = boto3.resource('s3')
bucket = s3.Bucket(BUCKET_NAME)

rekognition = boto3.client("rekognition", REGION)


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
        },
    }


def lambda_handler(event, context):
    '''Demonstrates a simple HTTP endpoint using API Gateway. You have full
    access to the request and response payload, including headers and
    status code.

    To scan a DynamoDB table, make a GET request with the TableName as a
    query string parameter. To put, update, or delete an item, make a POST,
    PUT, or DELETE request respectively, passing in the payload to the
    DynamoDB API as a JSON body.
    '''
    print("Received event: " + json.dumps(event, indent=2))

    operations = {
        'DELETE': del_record,
        'GET': get_record,
        'POST': create_record,
        'PUT': update_record,
    }

    operation = event['httpMethod']

    if operation in operations:
        payload = json.loads(event['body'])
        return respond(None, operations[operation](payload))
    else:
        return respond(ValueError('Unsupported method "{}"'.format(operation)))


def del_record(body):
    obj = bucket.Object(body['name'])
    obj.delete()
    table.delete_item(Key={'name': body['name']})


def update_record(body):
    response = table.scan()

    result = []
    for i in response['Items']:
        result.append(i['name'])

    return result


def create_record(body):
    '''
    If the name is not contained in the body, we will use the data to match
    all the images in the lib and find one matches the input data.
    Else, we will create a record according to the the data and the name
    '''
    if 'name' not in body:
        return get_record(body)
    
    obj = bucket.Object(body['name'])
    data = base64.b64decode(body['data'])
    obj.put(Body=data)
    
    table.put_item(
        Item={
            'name': body['name']
        }
    )
    return {'result': 'succeed'}

def get_record(msg_body):
    src = base64.b64decode(msg_body['data'])
    response = table.scan()
    max_similarity = 0
    result = None

    for i in response['Items']:
        similarity = compare_faces(src, i['name'])
        if max_similarity < similarity:
            max_similarity = similarity
            result = i['name']

    return {'name': result}


def compare_faces(src_bytes, target_object):
    response = rekognition.compare_faces(
        SourceImage={
            'Bytes': src_bytes,
        },
        TargetImage={
            "S3Object": {
                "Bucket": BUCKET_NAME,
                "Name": target_object,
            }
        },
        SimilarityThreshold=COMPARE_THRESHOLD)

    print(response)
    if not response['FaceMatches']:
        result = 0
    else:
        result = response['FaceMatches'][0]['Similarity']
    return result
