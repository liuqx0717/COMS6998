var baseUrl = "https://api.hw3.liuqx.net/v1/";
var api_visitors = baseUrl + "visitors";


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

function loadId() {
  var id = getQueryVariable("id");
  if(id != null){
    $("#idInputBox").val(id);
  }
}

function submitForm(e) {
  e.preventDefault();
  $("#imageCol").empty();
  var labels = $("#labelBox").val();
  var data = {"q": labels};

  $.ajax({
    type: "GET",
    url: "https://p4pv3uijkk.execute-api.us-east-1.amazonaws.com/Test",
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
