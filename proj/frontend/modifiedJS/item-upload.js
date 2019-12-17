const baseUrl = "https://api.moreforless.liuqx.net/v1";
var token = getToken();
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
      document.location = "single-product.html?item_id=" + response;
    },
    error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
      alert("errMsg");
    }
  });
}
