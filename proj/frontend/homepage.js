const baseUrl = "https://api.moreforless.liuqx.net/v1/";

function loadHomepage(){
    //token = getQueryVariable("access_token");
    token = getHashParams().access_token;
    if(token != null){
        var oneDay = 24*60*60;
        document.cookie = "token=" + token + ";path=/;max-age=" + oneDay;
    }
    //alert(token);
    //alert(getToken());
    refreshRecomm();
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(refreshRecomm);
    }
}

function refreshRecomm(position = null){
    var queryStr = "";
    if(position != null){
        queryStr = "?lat=" + position.coords.latitude + "&lon=" + position.coords.longitude;
        //alert(queryStr);
    }

    var data = "";
    $.ajax({
        type: "GET",
        url: baseUrl + "recommendation" + queryStr,
        crossDomain: true,
        data: data,
        dataType: "json",
        success: function(response){
            $("#recomm").empty();
            for(var i = 0, l = response.length; i < l; i++){
                var item = response[i];
                // TODO
                var itemLink = "./single-product.html?item_id=" + item.id;
                addRecommItem(item.title, item.imageUrl[0], itemLink, item.price, item.prevPrice);
            }
        },
        error: function(xhr, status, error){
            errMsg = "Failed.<br>" + xhr.responseText;
            alert(errMsg);
        }
    });
    

    //response = [
    //    {
    //        "id": "123456",
    //        "title": "title",
    //        "imageUrl": [
    //            "1.png",
    //            "2.png"
    //        ],
    //        "price": 150,
    //        "prevPrice": 200
    //    },
    //    {
    //        "id": "123457",
    //        "title": "title2",
    //        "imageUrl": [
    //            "2.png",
    //            "1.png"
    //        ],
    //        "price": 1500,
    //        "prevPrice": 2000
    //    }
    //];

}

function addRecommItem(title, imgUrl, link, price, prevPrice = 0){
    htmlStr = 
    '<div class="col">' +
       ' <div class="f_p_item">' +
            '<div class="f_p_img">' +
                '<img class="img-fluid" src="' + imgUrl + '" alt="">' +
                '<div class="p_icon">' +
                    '<a href="' + link + '">' +
                        '<i class="lnr lnr-heart"></i>' +
                    '</a>' +
                    '<a href="' + link + '">' +
                        '<i class="lnr lnr-cart"></i>' +
                    '</a>' +
                '</div>' +
            '</div>' +
            '<a href="' + link + '">' +
                '<h4>' + title + '</h4>' +
            '</a>';
    if(prevPrice != 0) {
        htmlStr = htmlStr +
            '<del>' + prevPrice + '</del>' ;
    }
    htmlStr = htmlStr +
            '<h5>' + price + '</h5>' +
        '</div>' +
    '</div>';

    $("#recomm").append(htmlStr);
}

