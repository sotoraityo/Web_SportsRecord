document.getElementById("menuformbox").style.display ="none";
document.getElementById("setformbox").style.display ="none";
document.getElementById("menuformbox").style.height = "0%";
document.getElementById("setformbox").style.height = "0%";
function clickbutton(category){
    //各要素のインスタンス？を入手
    var button_form = document.getElementById(category+"button_form");
    var formbox=document.getElementById(category+"formbox")

    //フォームがあるときにボタンを押す：新規作成で非表示化
    if(formbox.style.display=="block"){
        formbox.style.display ="none";
        button_form.value="新規作成";
    //フォームがないときにボタンを押す：辞めるにして表示化
    }else{
        formbox.style.display ="block";
        button_form.value="キャンセル";
    }
}

//バーのIDを取得
var elem = document.getElementById('menuLevel');
//数字のID取得
var target = document.getElementById('levelvalue');
//バーを動かしたときの処理
var rangeValue = function (elem, target) {
    return function(evt){
    target.innerHTML = elem.value;
    }
}
elem.addEventListener('input', rangeValue(elem, target));


