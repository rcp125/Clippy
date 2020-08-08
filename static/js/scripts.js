// returns number of checked boxes
function count_checked(){
    baseElement = document.querySelector("#single-checks");
    document.getElementById("check-count").innerHTML = baseElement.querySelectorAll('input[type="Checkbox"]:checked').length;
    document.getElementById("super-check").checked = false;
}

// checks all boxes when master box is clicked
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

// populates details div and copies text to clipboard
function populate_div(index){
    var offset = new Date().getTimezoneOffset() * 60 * 1000;
    $.getJSON('http://localhost:5000/json', function(data) {
        var text = `${data[parseInt(index)].text}`;
        var raw_date = data[parseInt(index)].date;
        var date_obj = new Date(Date.parse(raw_date) + offset);
        var formatted_date = date_obj.dateFormatter("#DD#/#MM#/#YYYY# #hh#:#mm#:#ss#");

        var item_len = `${data[parseInt(index)].length} characters | ${formatted_date}`;
        console.log(text);
        $("#item_details").text(text);
        $("#item_length").text(item_len);

        $('[id=copied-tag]').eq(index).show().delay(1500).fadeOut();

        var dummy = document.createElement("textarea");
        document.body.appendChild(dummy);
        dummy.value = text;
        dummy.select();
        document.execCommand("copy");
        document.body.removeChild(dummy);

    });
}

// Download Copied Text
function download() {
    var text = document.getElementById("item_details").innerText;
    var hidden = document.createElement('a');
    hidden.href = 'data:attachment/text,' + encodeURI(text);
    hidden.target = '_blank';
    hidden.download = 'copied.txt';
    hidden.click();
}

// Updates New Tags 
function is_new() {
    var refresh_date = JSON.parse(localStorage.getItem('lastRefresh'));
    var offset = new Date().getTimezoneOffset() * 60 * 1000;
    $.getJSON('http://localhost:5000/json', function(data) {
        $.each(data, function(i) {
            var py_date = `${data[i].date}`;
            if(Date.parse(py_date) + offset > refresh_date){
                $('[id=new-tag]').eq(i).show();
            }
        });
    });
}