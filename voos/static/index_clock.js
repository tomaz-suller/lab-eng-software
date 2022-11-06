function showTime(){
    var d = new Date();
    var year = d.getFullYear();
    var month = d.getMonth();
    var date = d.getDate();
    var day =d.getDay();
    var hour = d.getHours();
    var min = d.getMinutes();
    var sec = d.getSeconds();

    hour = ("0" + hour).slice(-2);
    min = ("0" + min).slice(-2);
    sec = ("0" + sec).slice(-2);

    document.getElementById("data").innerHTML = "Data: "+date+"/"+month+"/"+year;
    document.getElementById("hora").innerHTML = "Hora: "+hour+":"+min+":"+sec;
}
setInterval(showTime,1000);