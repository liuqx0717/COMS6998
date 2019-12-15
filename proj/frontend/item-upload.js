const baseUrl = "https://api.hw3.liuqx.net/v1";
// find token from session storage
var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzYzFkNzkyMS1lYmZkLTRmMjItYTlkMS1iNmM3Mjc1NWY4MWIiLCJldmVudF9pZCI6IjNlOGJhN2JiLWNiZmItNDM4NC05YjU5LWMwMTNjNjcxOTNiMCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzYzODk2MjAsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjM5MzIyMCwiaWF0IjoxNTc2Mzg5NjIwLCJ2ZXJzaW9uIjoyLCJqdGkiOiJkN2Y3MjliZS1jOGZjLTQyOGYtYWRiZC1hMDNjOGRlYTYxYzYiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiM2MxZDc5MjEtZWJmZC00ZjIyLWE5ZDEtYjZjNzI3NTVmODFiIn0.HHNvnDcyzciPajvbt5DvjI6IgeTTnlNEPXjGAdKGqKh2DJESZfJNVSF1bD8yHHmQDd5iZqTtj4F_WriWCMEd6GFI9wz8bX1iXY_OJ2eAACIHT1lnWaBYkm5agzupixkaJ7xC719q5eGzXmSyZ14xywx-LIUuTqk80P_rYawy9SYthkpQot-WmW2VatK9B-ARvHwqCumDPa_i3N7v6dpsc8NSAnWS53YaabQgcgfcZsUWyZno9od1kKTivopX3U_GIuUcU-Unhs9B5WgfbLCOTgUP5ZaiuT-r6jWbdz4CrGw_5Dw_7a9xDyU8OkS4UL305fKolHv7Cj_fJ1XtNYwxDw";

const tmpurl = "https://p4pv3uijkk.execute-api.us-east-1.amazonaws.com/Test";

function get_seller_info() {
  $.ajax({
    type: "GET",
    url: baseUrl + '/myhome',
    crossDomain: true,
    headers:{
      'access-token':token
    },
    dataType: "json",
    success: function(response){
      return response;
    },
    error: function(xhr, status, error){
      errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
      alert("alert-danger" + errMsg);
      return "";
    }
  });
}

// call smart street API
function get_location() {
  return {"lat":1, "lon":2};
}



function upload() {
  var image_array = [];
  var image_files = document.getElementById('images').files;
  for (var i = 0; i < image_files.length; ++i){
    var image = image_files[i];
    // var random_num = (Math.floor(Math.random() * 899999) + 100000).toString();
    // var filename = image.name;
    var extension = image.type;
    // console.log(filename);
    console.log(extension);
    // console.log(random_num);
    $.ajax({
      url: baseUrl + "/pictures",
      type: 'POST',
      data: image,
      dataType: 'json',
      headers:{
        'access-token':token
      },
      processData: false,
      contentType: extension,
      success: function (response) {
        // response is the image url
        image_array.push(response);
        // alert("Successful");
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
  var category = [$("#category").val()];
  var decription = $("#descriptionBox").val();
  var price = $("#priceBox").val();
  var prvprice = $("#prvPriceBox").val();
  var stocks = $("#stocksBox").val();
  var available = $("#availableBox").val();
  var seller_info = get_seller_info();
  var seller_id = seller_info["id"];
  var location = get_location();
  // var tag -- This should be get by /picture

  var data = JSON.stringify({
    "available": available,
    "sellerId": seller_id,
    "sellerInfo": seller_info,
    "title": title,
    "category": category,
    "decription": decription,
    "imageUrl": img_url_list,
    "price": price,
    "prvPrice": prvprice,
    "stocks": stocks,
    "location": location
  });

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
