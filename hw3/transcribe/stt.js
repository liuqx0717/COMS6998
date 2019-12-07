// Start a job
function uuid4() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
    });
  }
let JobName = uuid4()

let transcribeservice = new AWS.TranscribeService();

let MediaFileUri = 'https://s3.us-east-1.amazonaws.com/speeches1/speech1.mp3'

let job_params = {
    "LanguageCode": "en-US",
    "Media": {
      "MediaFileUri": MediaFileUri
    },
    "TranscriptionJobName": JobName,
    "MediaFormat": "mp3",
  };
transcribeservice.startTranscriptionJob(job_params, function(err, data) {
if (err) console.log(err, err.stack); // an error occurred
else     console.log(data);           // successful response
});


// Get the result of the job
params = {
    "TranscriptionJobName": JobName
};

response = {
    "TranscriptionJob": {
        "TranscriptionJobStatus": ""
    }
}

while(response['TranscriptionJob']['TranscriptionJobStatus'] !== 'COMPLETED'){
    setTimeout(function(){
        transcribeservice.getTranscriptionJob(params, function(err, data) {
            if (err) console.log(err, err.stack); // an error occurred
            else     console.log(data);           // successful response
            });
    }, 10000);
}


// Parse the result
let TranscriptFileUri = data['TranscriptionJob']['Transcript']['TranscriptFileUri']

let request = new XMLHttpRequest();
request.open('GET', TranscriptFileUri, true);
request.send(null);
data = JSON.parse(request.responseText)

text = data['results']['transcripts'][0]['transcript']
