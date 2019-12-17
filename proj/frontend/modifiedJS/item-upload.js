const baseUrl = "https://api.moreforless.liuqx.net/v1";
var token = getToken();
// var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOTQ4MGI3NC0zNzg3LTRjNjQtYmMxYi03ZWZiODEyOWFhNDciLCJldmVudF9pZCI6IjNhYjc1ZWQ2LThmYWItNDNhMS1iYzkzLTNmZTk0N2QxZDVlNSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY1NjMzMzUsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjU2NjkzNSwiaWF0IjoxNTc2NTYzMzM1LCJ2ZXJzaW9uIjoyLCJqdGkiOiI1NTU1NzJjZi0wYjk2LTQ2Y2ItODBkYi03MjQ3MWU1OTIzMDMiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiMjk0ODBiNzQtMzc4Ny00YzY0LWJjMWItN2VmYjgxMjlhYTQ3In0.r1KwJ0Ht0pjG2zi2Fkf_Q81U6Cwd-h1LiratdKHMB-kevY0Sckaasy889NTXOh2Pmmmg5PM7cNkfH1qZp2OdMi9xku9HqFlMT4qViP_4Ckn-TTiAYK6R_YZzSgdA5dhBUgSIfs_DqHdWBkyegBt9KkdvkBm4CHWG0aHSgdZhITYX_FEmrIbpI8V89E8ZItqswon-Ytm2Ic0_xxcCX4pVR_cP85fFtdDk62WH-qRoBFTE6pKWMBKi05QnPqstfU1Snt0TthF4m_SxIjBVIjGx03vRpKhMVSxMhau006Yk7MDGnrj8iSrfEwjw2iWknAkBZmEYySS6Zri3H5-sGfomXw";
function upload() {
  var image_array = [];
  var image_files = document.getElementById('images').files;
  for (var i = 0; i < image_files.length; ++i){
    var image = image_files[i];
    // var extension = image.type;
    $.ajax({
      url: baseUrl + "/pictures",
      type: 'POST',
      data: image,
      async:false,
      dataType: 'json',
      headers:{
        'access-token':token
      },
      processData: false,
      // contentType: extension,
      contentType: "application/octet-stream",
      success: function (response) {
        // response is the image url
        image_array.push(response);
      },
      error: function(xhr, status, error){
        errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
        alert("errMsg");
      }
    });
  }
  return image_array;
}




function submitForm(e) {
  e.preventDefault();
  var img_url_list = upload();
  var title = $("#titleBox").val();
  var category = [$("#categoryBox").val()];
  console.log(category);
  var decription = $("#descriptionBox").val();
  var price = parseFloat($("#priceBox").val());
  var prvprice = parseFloat($("#prvPriceBox").val());
  var stocks = parseInt($("#stocksBox").val());
  var available = parseInt($("#availableBox").val());
  // var seller_info = get_seller_info();
  // var seller_id = seller_info["id"];
  // var location = get_location();

  var data = JSON.stringify({
    "available": available,
    // "sellerId": seller_id,
    // "sellerInfo": seller_info,
    "title": title,
    "category": category,
    "decription": decription,
    "imageUrl": img_url_list,
    "price": price,
    "prvPrice": prvprice,
    "stocks": stocks
  });
  console.log(data);

  $.ajax({
    type: "POST",
    url: baseUrl + '/items',
    crossDomain: true,
    data: data,
    dataType: "json",
    contentType: "application/json",
    headers:{
      'access-token':token
    },
    success: function(response){
      alert("Successful");
      window.location.href = "single-product.html?item_id=" + response;
    },
    error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
      alert("errMsg");
    }
  });
}
