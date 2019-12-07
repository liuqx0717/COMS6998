var baseUrl = "https://api.hw3.liuqx.net/v1/";
var api_visitors = baseUrl + "visitors";


function submitForm(e) {
  e.preventDefault();
  var image = document.getElementById('images').files[0];
  var random_num = (Math.floor(Math.random() * 899999) + 100000).toString();
  var filename = image.name;
  var extension = image.type;
  console.log(filename);
  console.log(extension);
  console.log(random_num);
  $.ajax({
     url: baseUrl + "upload/" + random_num + "-" + filename,
     type: 'PUT',
     data: image,
     dataType: 'html',
     headers: {"X-API-Key": "CXsDgIB38w3Ny950vlAzR9IOAkHEuEXr7IjW0Phf"},
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
