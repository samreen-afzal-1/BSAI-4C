setInterval(function(){
    fetch('/latest_alert')
    .then(response => response.json())
    .then(data => {
        if(data.type !== ""){
            alert("ALERT: " + data.type);
        }
    });
}, 5000);