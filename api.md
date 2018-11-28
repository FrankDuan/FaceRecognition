
1. Upload/update original photos:

POST https://32cr6t0aoh.execute-api.us-east-1.amazonaws.com/default/lambda-create-user
content-type: application/json
{
  "name": "alice",
  "type": "jpg", 
  "data": ""  //need to be base64-encoded image bytes  
}

2. Upload a new photo to match

GET https://32cr6t0aoh.execute-api.us-east-1.amazonaws.com/default/lambda-get-user
content-type: application/json
{
  "type": "jpg", 
  "data": ""
}

response:
{
  "name": "alice", 
}

3. Remove original photos

DELETE https://32cr6t0aoh.execute-api.us-east-1.amazonaws.com/default/lambda-create-user
content-type: application/json
{
  "name": "alice"
}


