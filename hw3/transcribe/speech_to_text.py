import boto3
import uuid
import time
import urllib.request, json

ACCESS_KEY_ID = 'AKIAZ7JA4ZXTH3735TUB'
SECRET_KEY = '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'
REGION = 'us-east-1'

# Input a URL of audio.
MediaFileUri = 'https://s3.us-east-1.amazonaws.com/speeches1/speech1.mp3'

start_time = time.time()

# Client has Access to transcribe and s3.
client = boto3.client('transcribe', aws_access_key_id=ACCESS_KEY_ID,
                      aws_secret_access_key=SECRET_KEY, region_name=REGION)

JobName = str(uuid.uuid4())

client.start_transcription_job(
    TranscriptionJobName=JobName,
    LanguageCode='en-US',
    # MediaSampleRateHertz=44000,
    MediaFormat='mp3',
    Media={
        'MediaFileUri': MediaFileUri
    },
    # OutputBucketName='transcripts01',
    # OutputEncryptionKMSKeyId='string',
    # Settings={
    #     'VocabularyName': 'string',
    #     'ShowSpeakerLabels': True|False,
    #     'MaxSpeakerLabels': 123,
    #     'ChannelIdentification': True|False,
    #     'ShowAlternatives': True|False,
    #     'MaxAlternatives': 123
    # }
)

response = {
    "TranscriptionJob": {
        "TranscriptionJobStatus": ""
    }
}

while response['TranscriptionJob']['TranscriptionJobStatus'] != 'COMPLETED':
    time.sleep(10)
    response = client.get_transcription_job(
        TranscriptionJobName=JobName
    )

TranscriptFileUri = response['TranscriptionJob']['Transcript']['TranscriptFileUri']
# print(TranscriptFileUri)

# TranscriptFileUri = 'https://s3.amazonaws.com/aws-transcribe-us-east-1-prod/685653151206/2de71582-4f9c-4e73-8d3e-1fec310a973b/db9e13d3-e5ba-4829-a8e4-995f7cca4320/asrOutput.json?X-Amz-Security-Token=IQoJb3JpZ2luX2VjEKj%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEaCXVzLWVhc3QtMSJHMEUCIQCVWVx70O56hFlN5uPQkTosSNNRAu4FXAxL0ZSt6R0P0wIgI2HE%2Bdr60O1RL57y8tIz6%2F8v9NbiedW%2BWiO4%2BdNc4%2F4q2AII4P%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FARABGgwyNzY2NTY0MzMxNTMiDEEh8m2aAnWjJ4d5oCqsAlWt4LP%2FhSRgy5AYmJIhAf4PgwovddiL0E3TAUjbhRtjcfVIL9puIov7edbMxETrE1j%2FQsW38uys%2BYWreFvfq4qUfUXY8tqCrbvKm%2Fvu5PfQaiBHzFHmrMRJB8%2BHQugCtY8pHIKjZX2de9zvDlpzCz8FBzswcAsnq7%2BPgNt70DHdbT87N0LdmBUHJxumo0mI1xRE9mWgASvAs02ZxINovY75%2Bq8O1dy2siD9LQmaO%2BRJ9dI3M4UCXabSgKIYNcw4hzQzqwzC%2F41qmMfvxOiB0NOjYrdTRgFYWKYT0BqCSOIWwPrIYPlNA7v7zalO8JVznf8c7QdZg1cWGq2b1h1tL6nw3F5DrBVmw%2FLY1xixioKtQLNnkRZojvCugKODTZB4SC24OBI7%2FCDU82Hb8DCa7ovvBTrQAg97Geaz9BlD%2Fv5nYJ7DdWGOtazhv%2Fi6mXmS2zXfHqSSd%2BqvAUucIxvyzKOJbrlnNyfA1fREbjphBY%2B3pwal2y9tcCKOcV63SWWCmcD8KZKKtRotXX4JkZEDJI3vM15XuU1jrLLdkh7A3yYSvTPTe2clUFOVNPArHIspE2%2BZfchF12h%2FwieCfUWpKyP12vPTURNf0iKB7Nr4dKuL4fbUplDw%2FJFyghESLfL1o4ED897LGdiJaS93zt%2FP5CeNb9FZvUcmkthNTDNyapSxsCYKR07R0Yp8uQ7eH2tN5tu1sr%2Bi2jM1veITvqRk%2FfvhNp5eLBJodpu1vrvm3z0yj6cSAgq1nF6tlwqsMh%2FEe7pBM1r6FcILWnJmamh3i1rauhRD7TJMDg%2Fivh6dIwlS8BHXPLg%2FbmHI72cd6z3G%2BA1w6hZqV342WYZxJ2VrBxH%2BWI7ltg%3D%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20191130T235918Z&X-Amz-SignedHeaders=host&X-Amz-Expires=899&X-Amz-Credential=ASIAUA2QCFAA4SV6KUH2%2F20191130%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Signature=d5eb372c02c11368f0123e5e84eef085f7ae0ed3bffb2a3194db4f9ffe9ad84a'
with urllib.request.urlopen(TranscriptFileUri) as url:
    data = json.loads(url.read().decode())
    # print(data)

text = data['results']['transcripts'][0]['transcript']

print(text)
print("--- %s seconds ---" % (time.time() - start_time))

