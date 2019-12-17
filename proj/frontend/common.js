function getQueryVariable(variable) {
  var query = window.location.search.substring(1);
  var vars = query.split('&');
  for (var i = 0; i < vars.length; i++) {
      var pair = vars[i].split('=');
      if (decodeURIComponent(pair[0]) == variable) {
          return decodeURIComponent(pair[1]);
      }
  }
  console.log('Query variable %s not found', variable);
}

function getHashParams() {
    var hash = window.location.hash.substring(1);
    var params = {}
    hash.split('&').map(hk => { 
      let temp = hk.split('='); 
        params[temp[0]] = temp[1] 
    });
    console.log(params);
    return params;
}


// returns a string or null.
function getToken() {
    var token = document.cookie.replace(/(?:(?:^|.*;\s*)token\s*\=\s*([^;]*).*$)|^.*$/, "$1");
    return token;
}


// the event handler on search button
function onSearch(e) {
    e.preventDefault();

    var s = $("#searchBox").val();
    
    window.location.href = "./search.html?s=" + encodeURIComponent(s);

}
