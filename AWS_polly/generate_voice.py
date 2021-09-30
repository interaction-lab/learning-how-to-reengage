import boto3
import json
import os

# put in the access_key_id and secret_access_key
polly_client = boto3.Session(
                aws_access_key_id='aws_access_key_id',
                aws_secret_access_key='aws_secret_access_key',
                region_name='us-west-2').client('polly')

with open('data.json') as f:
    input_dict = json.load(f)

for element in input_dict:
    for number in input_dict[element]:
        print(number + ":", end=" ")
        print(input_dict[element][number])
        curr = input_dict[element][number]
        VoiceId = curr['VoiceId']
        OutputFormat = curr['OutputFormat']
        TextType = curr['TextType']
        Text = curr['Text']
        Engine = curr['Engine']
        response = polly_client.synthesize_speech(
            VoiceId=VoiceId,
            OutputFormat=OutputFormat,
            TextType=TextType,
            Text=Text,
            Engine=Engine)
        isExist = os.path.exists('result/')
        if not isExist:
            os.makedirs('result')
        path = "result/" + element + "#" + number + ".mp3"
        file = open(path, 'wb')
        file.write(response['AudioStream'].read())
        file.close()
