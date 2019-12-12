import boto3
import random
import string


def lambda_handler(event, context):
    message = event['message']
    user_id = random_generator()

    lex = boto3.client('lex-runtime', region_name='us-east-1')

    response = lex.post_content(
        botName='FindPhotos',
        botAlias='Find_Photos',
        userId=user_id,
        contentType="text/plain; charset=utf-8",
        inputStream=message
    )

    keywords = []
    for key, val in response['slots'].items():
        if (key == 'Animal' or key == 'Object') and val is not None:
            keywords += val.split(' ')
        if (key == 'City' or key == 'Country') and val is not None:
            keywords.append(val)

    done = True if len(keywords) > 0 else False

    return {
        'status': done,
        'keywords': keywords
    }


def random_generator(size=10, char=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(char) for i in range(size))
