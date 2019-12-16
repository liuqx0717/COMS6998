var baseUrl = "https://api.moreforless.liuqx.net/v1";

// find token from session storage. This token will expire every 60 mins
var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzYzFkNzkyMS1lYmZkLTRmMjItYTlkMS1iNmM3Mjc1NWY4MWIiLCJldmVudF9pZCI6Ijg1Y2M0NjI4LWQ0ZDgtNGVmOC05NDg3LTM3NmQ2MmRiOGI1MiIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY1Mjk1NzEsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjUzMzE3MSwiaWF0IjoxNTc2NTI5NTcyLCJ2ZXJzaW9uIjoyLCJqdGkiOiIwOTliODliMi0yMTY2LTQzMmItODcyOC1kMjk5NGVjZjY5MTgiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiM2MxZDc5MjEtZWJmZC00ZjIyLWE5ZDEtYjZjNzI3NTVmODFiIn0.niw236YpX9bYe6D1ny8b0SqBfd1Z8k5keQgIIBYcNjb3i8Zuu627UJHIJzaqCCX_QqNfSH1YfbdiCz1S6uJyZK5YYxFK5H6M3b-SrJ_SGjvv6DWFzOeeO3KKH2SHjB6ltxDyGlnQkGXnMNvSbWmhQCC5B6YPXVbVSbHfZTf3sIkDjCnwA3Q0jmW2oEBrtDr7BPGICFsEIwEkjbJa53t4jWV7R1Xe2d7QBdHmsTuVM-xV14DB9I3ERdgKDFUjogyyUUHOSyNQpFA9HpNeNqRQ44SmufmTHBI7Lnd-H9r8_0Aes1uV5Mvlvcq3JKrqLRLa4kQpuxzezlJXMkegUI2NVg";
// var token = sessionStorage.getItem('access-token');
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

function generate_item_html(item_imgurl, item_title, item_price, item_finish_time, item_seller_name, item_seller_address, order_status, order_id) {
    item_template = `<div class="row">
                                <div class="col-3">
                                    <img class="img-fluid" src="{item_imgurl}" alt="">
                                </div>
                                <div class="col-lg-9">
                                    <a href="#">Title:{item_title}</a>
                                    <br>
                                    Price:{item_price}
                                    <br>
                                    Finished time:{item_finish_time}
                                    <br>
                                    Seller:{item_seller_name}
                                    <br>
                                    Seller Address:{item_seller_address}
                                    <br>
                                    Status:{order_status}
                                    <br>
                                    Order ID:{order_id}
                                </div>
                            </div>
                            <br>`;
    item_template = item_template.replace("{item_imgurl}",item_imgurl).replace("{item_title}",item_title)
        .replace("{item_price}",item_price).replace("{item_finish_time}",item_finish_time)
        .replace("{order_status}",order_status).replace("{order_id}",order_id)
        .replace("{item_seller_name}", item_seller_name).replace("{item_seller_address}", item_seller_address);
    return item_template
}



function show_orders(response) {
    for (var index = 0; index < response.length; index++) {
        console.log(JSON.stringify(response[index]));
        var item_finish_time = response[index]["finishTime"];
        var order_id = response[index]["id"];
        var order_status = response[index]["status"];
        var item_seller_address = response[index]["sellerInfo"]["address"];
        var item_seller_name = response[index]["sellerInfo"]["userName"];
        var items = response[index]["items"];
        for (var ind = 0; ind < items.length; ind++){
            var item_id = items[ind];
            var item_price = "";
            var item_title = "";
            var item_imgurl = "";

            $.ajax({
                type: "GET",
                url: baseUrl + "/items/" + item_id,
                crossDomain: true,
                dataType: "json",
                async:false,
                headers:{
                    'access-token':token
                },
                success: function(response){
                    item_title = response["title"];
                    item_price = response["price"];
                    item_imgurl = response["imageUrl"][0];
                },
                error: function(xhr, status, error){
                    errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
                    alert("alert-danger" + errMsg);
                }
            });
            var item_content = generate_item_html(item_imgurl, item_title, item_price, item_finish_time, item_seller_name, item_seller_address, order_status, order_id);
            $("#profile_item_list").prepend(item_content);
        }
    }
    alert(JSON.stringify(response));
}
