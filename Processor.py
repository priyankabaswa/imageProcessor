import json
import boto3
from botocore.config import Config

def lambda_handler(event, context):

    # ACCESS_KEY_ID and ACCESS_SECRET_KEY can be obtained from AWS account
    ACCESS_KEY_ID = ''
    ACCESS_SECRET_KEY = ''

    # Accessing S3 through boto client
    s3 = boto3.client('s3',
                      aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=ACCESS_SECRET_KEY,
                      config=Config(signature_version='s3v4'))
    BucketName = ''
    FileName = 'NaturePic.jpg'
    KeyFileName = "MyPics/Nature/{0}".format(FileName)

    # Image file storing into the S3
    s3.upload_file(FileName, BucketName, KeyFileName)

    # Context File Storing in the S3 as index file
    list = [{"id": 1, "key": "NaturePic12.jpg","tags": [{"class": "Tree", "subclass": "Bench"}, {"class": "redCat", "subclass": "grey"}]},
            {"id": 2, "key": "Pic234.jpg", "tags": [{"class": "flowers", "subclass": "beach"}]},
            {"id": 3, "key": "Building.jpg", "tags": [{"class": "stairs", "subclass": "lift"}]}]
    json_object = json.dumps(list)
    print(json_object)

    # Creates out.json file to load the data
    with open('out.json', 'w') as outfile:
        outfile.write(json_object)
    s3.put_object(Key='MyPics/Nature/out.json', Bucket=BucketName, Body=json_object)
    print("Json Object is created")

    # Finding the next free ID value
    latest_value = (list[-1]['id'])
    print("LatestIDValue",latest_value)
    print("Next ID value added to be ", latest_value + 1)

    # Generating new Image and Context file to the list
    NewImageKey = "Scenary.jpg"
    NewContextFile = {"tags":[{"class":"animals", "subclass":"dogs"}]}
    NewContextFile['id'] = latest_value + 1
    NewContextFile['NewImageKey'] = NewImageKey

    # IMAGE file storing into the S3
    BucketName = ""
    KeyFileName = "MyPics/Nature/{0}".format(NewImageKey)
    s3.upload_file(NewImageKey, BucketName, KeyFileName)

    # Appending new item to the list
    newItem = {"id": NewContextFile['id'], "key": NewImageKey, "tags": [{"class": "animals", "subclass": "dogs"}]}
    list.append(newItem)
    print(list)
    out = json.dumps(list)
    print("New Item has been appended to the list")

    # Index file storing to the S3
    with open("out_updated.json", "w") as new:
        new.write(out)
    s3.put_object(Key='MyPics/Nature/out_updated.json', Bucket=BucketName, Body=out)
    print("updated INDEX file stored in S3")

    # Retrieving the Image classes
    with open("out_updated.json") as json_file:
        data = json.load(json_file)
        #print([i for i in data if i['tags'][0]['subclass'] == 'dogs'])
        for i in data:
            if i['tags'][0]['subclass'] == 'dogs':
                print(i)

lambda_handler (None, None)
