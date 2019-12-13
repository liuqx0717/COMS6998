const baseUrl = "https://api.hw3.liuqx.net/v1/";
const api_upload = baseUrl + "upload/";

// const tmpurl = "https://p4pv3uijkk.execute-api.us-east-1.amazonaws.com/Test";
const tmpurl = "https://ha5vfpjbhf.execute-api.us-east-1.amazonaws.com/v1";


function loadPhoto(json_str) {
  var results = json_str["results"];
  for (var i = 0; i < results.length; i++){
    var obj = results[i];
    var photoSrc = obj["url"];
    var labels = obj["labels"];
    if(photoSrc != null){
      var newElement = 
        "<img class='img-fluid w-100' src='" + photoSrc + "' alt='Failed to open image: " + photoSrc + "'>" 
      $("#imageCol").prepend(newElement);
    }
  }
}

function submitForm(e) {
  e.preventDefault();
  $("#imageCol").empty();
  var labels = $("#labelBox").val();
  var data = {"q": labels};

  $.ajax({
    type: "GET",
    url: tmpurl,
    crossDomain: true,
    data: data,
    dataType: "json",
    success: function(response){
      loadPhoto(response);
    },
    error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
      alert("errMsg");
    }
  });
}

function upload(e) {
  e.preventDefault();
  var image = document.getElementById('images').files[0];
  var random_num = (Math.floor(Math.random() * 899999) + 100000).toString();
  var filename = image.name;
  var extension = image.type;
  console.log(filename);
  console.log(extension);
  console.log(random_num);
  $.ajax({
     url: api_upload + random_num + "-" + filename,
     type: 'PUT',
     data: image,
     dataType: 'html',
    //  headers: {"X-API-Key": "CXsDgIB38w3Ny950vlAzR9IOAkHEuEXr7IjW0Phf"},
     headers: {"X-API-Key": "FasEh7WYoP3dilu2oRF0L9YlfDHz4NPrpdVej1y6"},
     processData: false,
     contentType: extension,
     success: function (response) {
      alert("Successful");
     },
     error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
      alert("errMsg");
      }
  });
}


