// var get_usr_info = "https://p4pv3uijkk.execute-api.us-east-1.amazonaws.com/Test";
var baseUrl = "https://api.moreforless.liuqx.net/v1";
// find token from session storage
var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzYzFkNzkyMS1lYmZkLTRmMjItYTlkMS1iNmM3Mjc1NWY4MWIiLCJldmVudF9pZCI6IjNlOGJhN2JiLWNiZmItNDM4NC05YjU5LWMwMTNjNjcxOTNiMCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzYzODk2MjAsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjM5MzIyMCwiaWF0IjoxNTc2Mzg5NjIwLCJ2ZXJzaW9uIjoyLCJqdGkiOiJkN2Y3MjliZS1jOGZjLTQyOGYtYWRiZC1hMDNjOGRlYTYxYzYiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiM2MxZDc5MjEtZWJmZC00ZjIyLWE5ZDEtYjZjNzI3NTVmODFiIn0.HHNvnDcyzciPajvbt5DvjI6IgeTTnlNEPXjGAdKGqKh2DJESZfJNVSF1bD8yHHmQDd5iZqTtj4F_WriWCMEd6GFI9wz8bX1iXY_OJ2eAACIHT1lnWaBYkm5agzupixkaJ7xC719q5eGzXmSyZ14xywx-LIUuTqk80P_rYawy9SYthkpQot-WmW2VatK9B-ARvHwqCumDPa_i3N7v6dpsc8NSAnWS53YaabQgcgfcZsUWyZno9od1kKTivopX3U_GIuUcU-Unhs9B5WgfbLCOTgUP5ZaiuT-r6jWbdz4CrGw_5Dw_7a9xDyU8OkS4UL305fKolHv7Cj_fJ1XtNYwxDw";
$(document).ready(function() {
    // call for /myhome GET API to get user info
    $.ajax({
        type: "GET",
        url: baseUrl + '/myhome',
        crossDomain: true,
        headers:{
            'access-token':token
        },
        dataType: "json",
        success: function(response){
            show_profile(response);
        },
        error: function(xhr, status, error){
            errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
            alert("alert-danger" + errMsg);
        }
    });


    // call for /orders GET API to get fininshed order info
    $.ajax({
        type: "GET",
        url: baseUrl + "/orders",
        crossDomain: true,
        headers:{
            'access-token':token
        },
        dataType: "json",
        success: function(response){
            show_orders(response);
        },
        error: function(xhr, status, error){
            errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
            alert("alert-danger" + errMsg);
        }
    });
});

function show_profile(response) {
    var email = response["email"];
    var name = response["userName"];
    var phone = response["phone"];
    var address = response["address"];
    var type = response["type"];
    $("#profile_user_name").text(name);
    $("#profile_user_email").text("Email: "+ email);
    $("#profile_user_phoneNumber").text("Phone: "+ phone);
    $("#profile_user_address").text("Address: "+ address);
    $("#profile_user_type").text(type);


    // $("#formAlert").remove();
    //
    // date = new Date();
    // time = date.toLocaleTimeString();
    // newElement =
    //     "<div id='formAlert' class='alert top-1 " + type + "' role='alert'>" +
    //     time + "<br>" + msg +
    //     "</div>";
    // $("#alertCol").append(newElement);

}

function update_user(event){
    event.preventDefault();
    console.log("update_user");
    var new_name = $("#profile_new_user_name").val();
    var new_email = $("#profile_new_user_email").val();
    var new_phoneNumber = $("#profile_new_user_phoneNumber").val();
    var new_address = $("#profile_new_user_address").val();
    var data = JSON.stringify({
        "userName": new_name,
        "address": new_address,
        "email": new_email,
        "phone": new_phoneNumber
    });

    // call for /myhome PUT API to update users
    $.ajax({
        type: "PUT",
        url: get_usr_info,
        crossDomain: true,
        data: data,
        dataType: "json",
        headers:{
            'Access-Token':token
        },
        success: function(response){
            alert("Update Successful!");
            document.location = "#";
        },
        error: function(xhr, status, error){
            errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
            alert("alert-danger" + errMsg);
        }
    });
}

function generate_item_html(item_imgurl, item_title, item_price, item_finish_time, order_status, order_id) {
    item_template = `<div class="row">
                                <div class="col-3">
                                    <img class="img-fluid" src="{item_imgurl}" alt="">
                                </div>
                                <div class="col-lg-9">
                                    Title:{item_title}
                                    <br>
                                    Price:{item_price}
                                    <br>
                                    Finished time:{item_finish_time}
                                    <br>
                                    Status:{order_status}
                                    <br>
                                    Order ID:{order_id}
                                </div>
                            </div>
                            <br>`;
    item_template = item_template.replace("{item_imgurl}",item_imgurl).replace("{item_title}",item_title)
        .replace("{item_price}",item_price).replace("{item_finish_time}",item_finish_time)
        .replace("{order_status}",order_status).replace("{order_id}",order_id);
    return item_template
}



function show_orders(response) {
    response = [{"prvPrice":23.4,"buyer":"3c1d7921-ebfd-4f22-a9d1-b6c72755f81b","seller":"123321","finishTime":"Sun Dec 15 04:16:40 2019","status":"finished","sellerInfo":{"userName":"Sao","address":"120 W 109th St, New York, NY, 10025"},"price":12.3,"id":"123321","items":["123","234","345"]},
        {"prvPrice":23.4,"buyer":"3c1d7921-ebfd-4f22-a9d1-b6c72755f81b","seller":"123321","finishTime":"Sun Dec 15 04:16:40 2019","status":"finished","sellerInfo":{"userName":"dasjhdgashdg","address":"asdasda120 W 109th St, New York, NY, 10025"},"price":12.3,"id":"123321","items":["123","234","345"]}]
    for (var index = 0; index < response.length; index++) {
        console.log(JSON.stringify(response[index]));
        var item_finish_time = response[index]["finishTime"];
        var order_id = response[index]["id"];
        var order_status = response[index]["status"];
        var items = response[index]["items"];
        for (var ind = 0; ind < items.length; ind++){
            var item_id = items[ind];
            var item_price = "";
            var item_title = "";
            var item_imgurl = "";

            var response1 =
                {
                    "id": "123456",
                    "title": "title",
                    "imageUrl": [
                        "https://dcist.com/wp-content/uploads/sites/3/2019/08/bunnies_web-1500x1000.jpg",
                        "https://dcist.com/wp-content/uploads/sites/3/2019/08/bunnies_web-1500x1000.jpg"
                    ],
                    "price": 150,
                    "prevPrice": 200
                };

            item_title = response1.title;
            item_price = response1.price;
            item_imgurl = response1.imageUrl[0];
            // $.ajax({
            //     type: "GET",
            //     url: baseUrl + "/items/" + item_id,
            //     crossDomain: true,
            //     dataType: "json",
            //     headers:{
            //         'access-token':token
            //     },
            //     success: function(response){
            //         item_title = response["title"];
            //         item_price = response["price"];
            //         item_imgurl = response["imageUrl"][0];
            //     },
            //     error: function(xhr, status, error){
            //         errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
            //         alert("alert-danger" + errMsg);
            //     }
            // });
            var item_content = generate_item_html(item_imgurl, item_title, item_price, item_finish_time, order_status, order_id);
            $("#profile_item_list").prepend(item_content);
        }
    }
    alert(JSON.stringify(response));
}
