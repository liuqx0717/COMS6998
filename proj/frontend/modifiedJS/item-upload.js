const baseUrl = "https://api.moreforless.liuqx.net/v1";

// find token from session storage
// var token = sessionStorage.getItem('access-token');
var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOTQ4MGI3NC0zNzg3LTRjNjQtYmMxYi03ZWZiODEyOWFhNDciLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNTc2NTM3ODEwLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9ESE80ODFzSGsiLCJleHAiOjE1NzY1NDE0MTAsImlhdCI6MTU3NjUzNzgxMCwidmVyc2lvbiI6MiwianRpIjoiNWIzYTc1ODctMTkzMi00NjVlLWE1MTYtZDVlMjRjZTM5YTM3IiwiY2xpZW50X2lkIjoiMmVpN2RodnJqaHFnNzFrdnRxdmo4dW12ZGEiLCJ1c2VybmFtZSI6IjI5NDgwYjc0LTM3ODctNGM2NC1iYzFiLTdlZmI4MTI5YWE0NyJ9.Y0yGvKfDIb13H3d_3BStlq4cVuVhBaprXRZFmaVqUyutpktQh9dvpmZ59tjmKGQLTcJpLCVxfpJbjHJtGcI40A4_B1hMLiVgP9M2wyQnCsqaS-qm9HUov_6pNR0YUWlZq3-Jx0dJum7IOadWujRX9U2oBmf_iSuc-5h3EiOR5k44VRrOGgYneucLg5Tj51168Psn8MtwJCg3PXcRBQI9E-1TXNqCwDn63QFa6EJJOpqku6hY_xnwuKgTylf6648IkgYX6lqVxorIv3AMhg8QlvVxe8XEhlCylEE6DOzgnyK7oW2IQqwd5B_IqEyut4P8WbI8v5nfIpaMBFq6mV1_7g";

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
    },
    error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
      alert("errMsg");
    }
  });
}
