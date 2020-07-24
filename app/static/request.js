function postCall(url, data, type) {

    let request = new XMLHttpRequest();

    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json");
    request.send(JSON.stringify(data));

    request.onreadystatechange = function() {

        let data = request.responseText

        if (request.readyState == 4 && request.status == 200) {
            if (type == 'login') {
                window.localStorage.setItem('token',data.access_token)
            }
        } else {
            alert(request.responseText.message);
        }
    }
}