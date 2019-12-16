var baseUrl = "https://api.moreforless.liuqx.net/v1";

// find token from session storage. This token will expire every 60 mins
// var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOTQ4MGI3NC0zNzg3LTRjNjQtYmMxYi03ZWZiODEyOWFhNDciLCJldmVudF9pZCI6ImZjMDkyZDZhLTZiOGItNGFkYi04ZjFkLTJjNjIwYmE3NDAxNyIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY1MzIzMzAsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjUzNTkzMCwiaWF0IjoxNTc2NTMyMzMwLCJ2ZXJzaW9uIjoyLCJqdGkiOiI2ZmMzZjkwNi02OWMwLTRjZTktYWU4MS00OTgwMGJlZjEwMzciLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiMjk0ODBiNzQtMzc4Ny00YzY0LWJjMWItN2VmYjgxMjlhYTQ3In0.KybOqJZNCfQVAdGcwdHAtONn2TLkT70Xvpwy7Bm1QtZlyRJNOQYWZrSXz36zD03noTcxSe3paGTP7gYuUNz8PpI4bJHL3RrOb6zyiGCM7AEhEoschZmbsZTxTfd1kANLfp29YoL4pRMaIRu6I_h7HTKgbYCIgrRmVZMJ1rJjlHFm3uPQk69Abm6mc5dNpfnA3nu9RRCeu9it0KeCUrIaIvIYjFE6AJIqcRPToOQFMi8IscRqrdaWpOmb4ZqZjPcfgv_wrTPW20gbuBNylkOZa9-iKiodGN9R2JnIvzb7NrhJmA_2P40JLuNT_wGFDgtYHTFRvyW176hHgd0Rw-YYLg";
// var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzNjI3YjNlMS04MDg1LTQ3MDMtYjdhNC1kYzFlY2EzODczZWYiLCJldmVudF9pZCI6IjUyNGM4OTU2LWQzMzEtNDIyOS1iMWJkLWVlMjYyNWIzOGM1OCIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY1MzMyODcsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjUzNjg4NywiaWF0IjoxNTc2NTMzMjg3LCJ2ZXJzaW9uIjoyLCJqdGkiOiJiODliNjQ2OC0xOTA2LTQzODAtYTAxNi1lZTAxNGRjNDU5MDUiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiMzYyN2IzZTEtODA4NS00NzAzLWI3YTQtZGMxZWNhMzg3M2VmIn0.ntHvVE5-BDVVMPO3izIOnut7dzGGd9sQnmmQeyKoDAC0CNw3UdmCeMi1VSFFy7LkSVZh9u1KuXXsBq8_GJIR9O8Os2O74bQDf3XxkwlgmB-FdygWZb7v_GFRxnAL1oD33AH0SFboFAb1NjzVG2TrDFHkurFlFXVIQfOd2PVCA-SXi_BT1P4tICMnOOqfh6ihFhXl0Pp2UqJswFZAIw9fJuRWshYlNSwqgpNCKQTLjiYZVEn_X93hJCWHXZip21DkJj8AzMxn_R8meME9PKTyJ8SjmAT_mtlHg_AN2VFEcy-iGs6SfQ_5YCWlg57cpoqLbbDTLvqW4VWkUjpxKQEz2w";
var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOTQ4MGI3NC0zNzg3LTRjNjQtYmMxYi03ZWZiODEyOWFhNDciLCJldmVudF9pZCI6Ijk5ZGJmOWI4LWUwMzEtNGFhZS1hNjI1LWZhMmI3ZTM3ZDU5MSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY1MzYwMzgsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjUzOTYzOCwiaWF0IjoxNTc2NTM2MDM4LCJ2ZXJzaW9uIjoyLCJqdGkiOiJmYzk1YTM4YS03YWUzLTRmOGQtOGNlZi00MWZjOTk2OTJjMWIiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiMjk0ODBiNzQtMzc4Ny00YzY0LWJjMWItN2VmYjgxMjlhYTQ3In0.TgT0RJvtiZcEdgyF86ezbYo5vD-s_Ay1vHGIX0L37F1oTtJ1zCvamv9JKF7lbSOUc3rq0zdYN71i92-Fk7hxeYitUOYPT0hWS4hoUBLYxIwSlV_JPEOpwbCClOLuiQE-edkRqMR4EXtjne4Ctk2Uwf6187VCFPstCWOyxqVVgSCInScgFEWm_Iuaf2pgQa3SNzVwtBpnNsJRRfATz-uSqMP6csQddU1885ExEtu1DSnoGsRPSZzBSHqG0ruV4e3VcyoX2dP1Stu7XyHW4ZxRwZi7HJlXCZjlUCnq5YP-deCn_w7JcjG1MhZRgkm4nqt4fELV90PyHaO-BZoQLueqVw";
// var token = sessionStorage.getItem('access-token');
$(document).ready(function() {
    // call for /myhome GET API to get user info
    var new_user = false;
    $.ajax({
        type: "GET",
        url: baseUrl + '/myhome',
        crossDomain: true,
        headers:{
            'access-token':token
        },
        dataType: "json",
        async:false,
        success: function(response, textStatus, xhr){
            if (xhr.status === 204){
                new_user = true;
                alert("Please upload your user type. Seller or buyer")
            } else {show_profile(response);}
        },
        error: function(xhr, status, error){
            errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
            alert("/myhome function" + errMsg);
        }
    });


    // call for /orders GET API to get fininshed order info
    if (!new_user) {
        $.ajax({
            type: "GET",
            url: baseUrl + "/orders",
            crossDomain: true,
            headers: {
                'access-token': token
            },
            dataType: "json",
            success: function (response) {
                show_orders(response);
            },
            error: function (xhr, status, error) {
                errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
                alert("/orders function" + errMsg);
            }
        });
    }
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
    var new_name = $("#profile_new_user_name").val();
    // var new_email = $("#profile_new_user_email").val();
    var new_phoneNumber = $("#profile_new_user_phoneNumber").val();
    var new_address = $("#profile_new_user_address").val();
    var new_paypalUrl = $("#profile_new_user_paypalUrl").val();
    var user_type = $("#profile_user_type").text();
    if (user_type === ""){
        user_type = $("#profile_new_user_type").val();
    }
    var data = JSON.stringify({
        "userName": new_name,
        "address": new_address,
        // "email": new_email,
        "phone": new_phoneNumber,
        "type": user_type,
        "paypalUrl": new_paypalUrl
    });
    console.log(data);
    // call for /myhome PUT API to update users
    $.ajax({
        type: "PUT",
        url: baseUrl + '/myhome',
        crossDomain: true,
        data: data,
        dataType: "json",
        headers:{
            'Access-Token':token
        },
        success: function(response){
            alert("Update Successful!");
            document.location = "profile.html";
        },
        error: function(xhr, status, error){
            errMsg = "Failed.<br>" + xhr.responseText + "<br>" + status + "<br>" + error;
            alert("/myhome PUT function" + errMsg);
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
                    alert("/items/ GET function" + errMsg);
                }
            });
            var item_content = generate_item_html(item_imgurl, item_title, item_price, item_finish_time, item_seller_name, item_seller_address, order_status, order_id);
            $("#profile_item_list").prepend(item_content);
        }
    }
}
