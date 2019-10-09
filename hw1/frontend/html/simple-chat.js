var me = {};
me.avatar = "https://lh6.googleusercontent.com/-lr2nyjhhjXw/AAAAAAAAAAI/AAAAAAAARmE/MdtfUmC0M4s/photo.jpg?sz=48";

var you = {};
you.avatar = "https://a11.t26.net/taringa/avatares/9/1/2/F/7/8/Demon_King1/48x48_5C5.jpg";

function formatAMPM(date) {
    var hours = date.getHours();
    var minutes = date.getMinutes();
    var ampm = hours >= 12 ? 'PM' : 'AM';
    hours = hours % 12;
    hours = hours ? hours : 12; // the hour '0' should be '12'
    minutes = minutes < 10 ? '0'+minutes : minutes;
    var strTime = hours + ':' + minutes + ' ' + ampm;
    return strTime;
}            

//-- No use time. It is a javaScript effect.
function insertChat(who, text, time){
    if (time === undefined){
        time = 0;
    }
    var control = "";
    var date = formatAMPM(new Date());
    
    if (who == "server"){
        control = '<li style="width:100%">' +
                        '<div class="msj macro">' +
                        '<div class="avatar"><img class="img-circle" style="width:100%;" src="'+ me.avatar +'" /></div>' +
                            '<div class="text text-l">' +
                                '<p>'+ text +'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '</div>' +
                    '</li>';                    
    }else{
        control = '<li style="width:100%;">' +
                        '<div class="msj-rta macro">' +
                            '<div class="text text-r">' +
                                '<p>'+text+'</p>' +
                                '<p><small>'+date+'</small></p>' +
                            '</div>' +
                        '<div class="avatar" style="padding:0px 0px 0px 10px !important"><img class="img-circle" style="width:100%;" src="'+you.avatar+'" /></div>' +                                
                  '</li>';
    }
    setTimeout(
        function(){ 
            $("ul").append(control).scrollTop($("ul").prop('scrollHeight'));
        }, time);
    
}

function resetChat(){
    $("ul").empty();
}

$("#inputbox").on("keydown", function(e){
    if (e.which == 13){
        var text = $(this).val();
        if (text !== ""){
            insertChat("me", text);              
            $(this).val('');
            sendMsg(text);
        }
    }
});

$("#button-send").click(function(){
    $("#inputbox").trigger({type: 'keydown', which: 13, keyCode: 13});
})

//-- Clear Chat
resetChat();



var baseUrl = "https://api.hw1.liuqx.net/v1/";
var api_message = baseUrl + "message";
var api_session = baseUrl + "session";
var sessionid = "NULL";


getSessionid();


// The return value will reside in variable "sessionid".
function getSessionid(){
    $.ajax({
        type: "GET",
        url: api_session,
        crossDomain: true,
        data: "",
        //data:"SDfsfsddf",
        dataType: "json",
        success: function(response){
            //alert("received.");
            // No need to use JSON.parse(), because dataType set to "json".
            sessionid = response.sessionid;
        },
        error: function(xhr, status, error){
            alert("getSessionid() failed.\n" + xhr.responseText + "\n" + status + "\n" + error);
        }
    });
}

function sendMsg(text){
    //alert(apiUrl);
    if(sessionid == "NULL") {
        alert("No available session id.");
        return;
    }
    $.ajax({
        type: "POST",
        url: api_message,
        crossDomain: true,
        data: JSON.stringify({
            sessionid: sessionid,
            content: text
        }),
        //data:"SDfsfsddf",
        dataType: "json",
        success: function(response){
            //alert("received.");
            // No need to use JSON.parse(), because dataType set to "json".
            recvMsg(response.content);
        },
        error: function(xhr, status, error){
            alert("sendMsg() failed.\n" + xhr.responseText + "\n" + status + "\n" + error);
        }
    });
}

function recvMsg(text){
    insertChat("server", text);
}