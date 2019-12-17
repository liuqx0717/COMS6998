var baseUrl = "https://api.moreforless.liuqx.net/v1";

// find token from session storage. This token will expire every 60 mins
// var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzYzFkNzkyMS1lYmZkLTRmMjItYTlkMS1iNmM3Mjc1NWY4MWIiLCJldmVudF9pZCI6ImNlOTExZDdmLWViNTItNDRjYS04NDRkLTI3NDkwM2Y4YjhkZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY1MzkxMTksImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjU0MjcxOSwiaWF0IjoxNTc2NTM5MTE5LCJ2ZXJzaW9uIjoyLCJqdGkiOiI0YTc0NDk3Ny1kNDM5LTQ1Y2MtOTA1Yy1lNzVkNWY5MWNlZGMiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiM2MxZDc5MjEtZWJmZC00ZjIyLWE5ZDEtYjZjNzI3NTVmODFiIn0.qKC9vS5dHLFejcGPefwSHy7110ilzcxIxjaOKGp1fVtqElHu0XzTQpkFG-WZ2zPFglqGuioCOMbkddlhN4NeFnI0B1ZUwVR2L31cUyQxn2gbeLwUbg9j6XEHD5p_Y4OTZnc6jU-J_cL5letNd5sQB3KO4--opdSvnMJKclZiEOAB8Fd_IPcyNyOW0jClfyqMm3eLd5eIkSc1Y3s_Si0LhO-_HOMYGnvwu9NyOL4R-4jhpIFR647G7LGYJdXi_vZBhCbKvdKJsVUK9A3yUcZnVO0qYhst2Ef9gUw0Coe2FjJVBH2xQiziyQwICV2t1UENiWDrKP1jiyaX3o4XqAUJCA";
var token = "eyJraWQiOiJJT2VcL3p1VXU1SlFaQklkTHlxdmdhdHk2VmpCZjlWT2ZXaWFva0R4dWsyRT0iLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIyOTQ4MGI3NC0zNzg3LTRjNjQtYmMxYi03ZWZiODEyOWFhNDciLCJldmVudF9pZCI6ImRmZDZhZGY4LTM5MjAtNDM5ZC05MTg3LTRhMjM2MzMxNjMwZSIsInRva2VuX3VzZSI6ImFjY2VzcyIsInNjb3BlIjoiYXdzLmNvZ25pdG8uc2lnbmluLnVzZXIuYWRtaW4gcGhvbmUgb3BlbmlkIHByb2ZpbGUgZW1haWwiLCJhdXRoX3RpbWUiOjE1NzY1NDA3NDIsImlzcyI6Imh0dHBzOlwvXC9jb2duaXRvLWlkcC51cy1lYXN0LTEuYW1hem9uYXdzLmNvbVwvdXMtZWFzdC0xX0RITzQ4MXNIayIsImV4cCI6MTU3NjU0NDM0MiwiaWF0IjoxNTc2NTQwNzQyLCJ2ZXJzaW9uIjoyLCJqdGkiOiJkYTRmZjFiNi1hOWI3LTRlZWQtODQ2Zi0zZTg3NzZkZDg5ZmIiLCJjbGllbnRfaWQiOiIyZWk3ZGh2cmpocWc3MWt2dHF2ajh1bXZkYSIsInVzZXJuYW1lIjoiMjk0ODBiNzQtMzc4Ny00YzY0LWJjMWItN2VmYjgxMjlhYTQ3In0.tPX0dVPJgBhgZJhEcG97J0bHsyWr7Ur6v8-U8kI-cI8XMmR82aTr8zPWoPfUiak3HTZpWdwr-2aeyKFUrQNRID0Bvifq6eJ0Rr7H09kn3OSw0eQuKpOAlg0sec36s8kg_-1FmT0s-F5WUoTyLp-3A6aUYG_chHRC-nY8nLeDT5ryRqjPt8lBwMND5p4d8OG5CohqIXGPcfomJo7DEZ1W84Xv9-t48CXxEcasd4F_PUlXs49MBNE7XYMeDNfT1mmJU8F_i8x9A8MsrrT6DGltGD6FBa7SzwrNxcM6VZmxY5v5gpeIU3_cND1hetALKfRcBRzx5B4ZcqOn6rMex0Yk9A";
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

    var upload_button_template = `<aside class="single_sidebar_widget author_widget">
        <div>
        <a class="primary-btn submit_btn" href="seller_upload.html">Create items</a>
        </div>
        </aside>`;
    if (type==="seller"){
        $("#right_side_profile").prepend(upload_button_template);
    }


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

function generate_item_html(item_imgurl, item_id, item_title, item_price, item_finish_time, item_seller_name, item_seller_address, order_status, order_id) {
    item_template = `<div class="row">
                                <div class="col-3">
                                    <img class="img-fluid" src="{item_imgurl}" alt="">
                                </div>
                                <div class="col-lg-9">
                                    <a href="single-product.html?item_id={item_id}">Title:{item_title}</a>
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
        .replace("{item_seller_name}", item_seller_name).replace("{item_seller_address}", item_seller_address)
        .replace("{item_id}", item_id);
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
            var item_content = generate_item_html(item_imgurl, item_id, item_title, item_price, item_finish_time, item_seller_name, item_seller_address, order_status, order_id);
            $("#profile_item_list").prepend(item_content);
        }
    }
}
