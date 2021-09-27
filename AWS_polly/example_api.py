import boto3

polly_client = boto3.Session(
                aws_access_key_id='access_key_here',                     
    aws_secret_access_key='secret_access_key_here',
    region_name='us-west-2').client('polly')

response = polly_client.synthesize_speech(VoiceId='Joanna',
                OutputFormat='mp3', 
                Text = 'This is a sample text to be synthesized.',
                Engine = 'neural')

file = open('speech.mp3', 'wb')
file.write(response['AudioStream'].read())
file.close()