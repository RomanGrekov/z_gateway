function get_state(){
    $.get("/network/get_state/", function(data) {
        network_btn(data.state);
    });
}

$( document ).ready(function() {
    get_state();
});

function get_timeout(){
    $.get("/network/get_timeout/", function(data) {
        if (data.timeout == '0'){
            document.getElementById("progress_bar_div").hidden = true;
            return 0
        }
        $("#progress_content").html("exp: "+data.timeout);
     });
    $.get("/network/get_start_status/", function(data) {
        if (data.status == '0'){
            document.getElementById("progress_bar_div").hidden = true;
            get_home_id()
            return 0
        }
    });
    window.setTimeout(function() {
        get_timeout()
    }, 1000);
}

function start_network(){
    document.getElementById("progress_bar_div").hidden = false;
    $.get("/network/start_network/", function(data) {
        $("#progress_content").html("exp: "+data.resp);
        network_btn("on")
        get_timeout()
    });
}

function stop_network(){
    $.get("/network/stop_network/", function(data) {
        if(data.state == "off"){
            document.getElementById("progress_bar_div").hidden = true;
            network_btn("off")
        }
    });
}

function get_home_id(){
    $.get("/network/get_home_id/", function(data) {
        $("#home_id").html(data.home_id);
    });
}

function network_btn(onoff){
    if(onoff == "on"){
        document.getElementById("on").checked = true;
        document.getElementById("off").checked = false;
    }
    if(onoff == "off"){
        document.getElementById("on").checked = false;
        document.getElementById("off").checked = true;
    }

}
