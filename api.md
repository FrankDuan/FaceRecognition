
POST https://32cr6t0aoh.execute-api.us-east-1.amazonaws.com/default/lambda-create-user
content-type: application/json
{
  "name": "alice",
  "type": "jpg", 
  "data": ""
}

POST https://32cr6t0aoh.execute-api.us-east-1.amazonaws.com/default/lambda-get-user
content-type: application/json
{
  "type": "jpg", 
  "data": ""
}

{
  "name": "jpg", 
}
