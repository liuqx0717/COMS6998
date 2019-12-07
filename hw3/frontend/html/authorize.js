var baseUrl = "https://api.hw2.liuqx.net/v1/";
var api_authorize = baseUrl + "authorize";



function submitForm(e) {
  e.preventDefault();

  var otp = $("#otpInputBox").val();

  var data = "";

  $.ajax({
    type: "GET",
    url: api_authorize + "/" + encodeURIComponent(otp),
    crossDomain: true,
    data: data,
    dataType: "json",
    success: function(response){
      name = response.name;
      showAlert("alert-success", "Welcome, " + name + "!");
    },
    error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText;
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
