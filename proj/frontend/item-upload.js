const baseUrl = "https://api.moreforless.liuqx.net/v1";

// find token from session storage
var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzNjI3YjNlMS04MDg1LTQ3MDMtYjdhNC1kYzFlY2EzODczZWYiLCJ0b2tlbl91c2UiOiJhY2Nlc3MiLCJzY29wZSI6ImF3cy5jb2duaXRvLnNpZ25pbi51c2VyLmFkbWluIHBob25lIG9wZW5pZCBwcm9maWxlIGVtYWlsIiwiYXV0aF90aW1lIjoxNTc2NTI4MTMxLCJpc3MiOiJodHRwczpcL1wvY29nbml0by1pZHAudXMtZWFzdC0xLmFtYXpvbmF3cy5jb21cL3VzLWVhc3QtMV9ESE80ODFzSGsiLCJleHAiOjE1NzY1MzE3MzEsImlhdCI6MTU3NjUyODEzMSwidmVyc2lvbiI6MiwianRpIjoiYmY4YzExN2UtN2JiMy00MmZiLWI4NDYtZDM1ZjVjZDRhY2NiIiwiY2xpZW50X2lkIjoiMmVpN2RodnJqaHFnNzFrdnRxdmo4dW12ZGEiLCJ1c2VybmFtZSI6IjM2MjdiM2UxLTgwODUtNDcwMy1iN2E0LWRjMWVjYTM4NzNlZiJ9.DxPGaa6Q4gcVW-54zVw1SbcAotTcFVP6ZAIK2yF9MlilwtE7_H45EgsTuAU6WSZ02bjYLd0f7_YgUzEWTDEkXqY0Mdz19wvcRjFSmTf6_B5nUKq_35Ca-cq3WerpSLL_OEd-3Gkpmv3pZuc-R98oZAJxvRAs0gJkd-a1fl25rexw1rRbZZEi94QgYQlU0FuuuOPnnOUjygOo2805mEoNaUxEeT01PhmsvnAq3apAnAny_M98TLeeOYSuvAIXXWbRbwwqgQo37UHWrQgKBWaf2i_yaQaQ_Uugt-xSjdsr04EmGH6xqSHqMvJiTRCN34rc6o8HVg-bSbkH68ZJqwdSlg";
// var token = sessionStorage.getItem('access-token');

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
