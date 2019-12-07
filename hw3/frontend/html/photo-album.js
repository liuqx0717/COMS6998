var baseUrl = "https://api.hw2.liuqx.net/v1/";
var api_visitors = baseUrl + "visitors";



function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split('&');
  for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split('=');
      if (decodeURIComponent(pair[0]) == variable) {
          return decodeURIComponent(pair[1]);
      }
  }
  console.log('Query variable %s not found', variable);
}

function loadPhoto() {
  var photoSrc = getQueryVariable("photo");
  if(photoSrc != null){
    var newElement = 
      "<img class='img-fluid w-100' src='" + photoSrc + "' alt='Failed to open image: " + photoSrc + "'>" 
    $("#imageCol").prepend(newElement);
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

  var id = $("#idInputBox").val();
  var name = $("#nameInputBox").val();
  var phone = $("#phoneInputBox").val();

  var data = JSON.stringify({
    name: name,
    phoneNumber: phone
  });

  $.ajax({
    type: "PUT",
    url: api_visitors + "/" + encodeURIComponent(id),
    crossDomain: true,
    data: data,
    dataType: "json",
    success: function(response){
      showAlert("alert-success", "Uploaded successfully.");
    },
    error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
      showAlert("alert-danger", errMsg);
    }
  });
}

// type: the alert type of bootstrap.
function showAlert(type, msg) {
  $("#formAlert").remove();

  date = new Date();
  time = date.toLocaleTimeString();
  newElement = 
    "<div id='formAlert' class='alert top-1 " + type + "' role='alert'>" +
    time + "<br>" + msg +
    "</div>";
  $("#alertCol").append(newElement);

}
