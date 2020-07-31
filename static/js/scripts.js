function count_checked(){
    baseElement = document.querySelector("#single-checks");
    document.getElementById("check-count").innerHTML = baseElement.querySelectorAll('input[type="Checkbox"]:checked').length;
    document.getElementById("super-check").checked = false;
}

function check_all(source){
    checkboxes = document.getElementsByName('copy_id');
    for(var i = 0; i < checkboxes.length; i++){
        checkboxes[i].checked = source.checked;
    }
    baseElement = document.querySelector("#single-checks");
    var count = baseElement.querySelectorAll('input[type="Checkbox"]').length;
    if(baseElement.querySelectorAll('input[type="Checkbox"]:checked').length == count){
        document.getElementById("check-count").innerHTML = count;
    }
    else{
        document.getElementById("check-count").innerHTML = 0;
    }
}

function copy2clip(){
    var text = document.getElementById("check-count");

    text.select();
    text.setSelectionRange(0, 99999);

    document.execCommand("copy");
}

function populate_div(index){
    $.getJSON('http://localhost:5000/json', function(data) {
        var text = `${data[parseInt(index)].text}`;
        var item_len = `${data[parseInt(index)].length} characters`;
        console.log(text);
        $("#item_details").text(text);
        $("#item_length").text(item_len);

        var dummy = document.createElement("textarea");
        document.body.appendChild(dummy);
        dummy.value = text;
        dummy.select();
        document.execCommand("copy");
        document.body.removeChild(dummy);

    });
}