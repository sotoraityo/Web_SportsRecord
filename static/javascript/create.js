//バーのIDを取得
var elem1 = document.getElementById('sihyo1');
//数字のID取得
var target1 = document.getElementById('sihyovalue1');
//バーを動かしたときの処理
var rangeValue = function (elem1, target1) {
    return function(evt){
    target1.innerHTML = elem1.value;
    }
}
elem1.addEventListener('input', rangeValue(elem1, target1));

var elem2 = document.getElementById('sihyo2');
var target2 = document.getElementById('sihyovalue2');
var rangeValue = function (elem2, target2) {
    return function(evt){
    target2.innerHTML = elem2.value;
    }
}
elem2.addEventListener('input', rangeValue(elem2, target2));

var elem3 = document.getElementById('sihyo3');
var target3 = document.getElementById('sihyovalue3');
var rangeValue = function (elem3, target3) {
    return function(evt){
    target3.innerHTML = elem3.value;
    }
}
elem3.addEventListener('input', rangeValue(elem3, target3));

var elem4 = document.getElementById('sihyo4');
var target4 = document.getElementById('sihyovalue4');
var rangeValue = function (elem4, target1) {
    return function(evt){
    target4.innerHTML = elem4.value;
    }
}
elem4.addEventListener('input', rangeValue(elem4, target4));

var elem5 = document.getElementById('sihyo5');
var target5 = document.getElementById('sihyovalue5');
var rangeValue = function (elem5, target5) {
    return function(evt){
    target5.innerHTML = elem5.value;
    }
}
elem5.addEventListener('input', rangeValue(elem5, target5));

/*
#
チェックボックスのその他
#
*/
function change() {
    var element;
    if(document.getElementById("checkBox").checked) {
        // チェックが入っていたら、送信ボタンのdisabledを外す
        element = document.getElementById("health_sonota");
        element.disabled = false;
    }else {
        // チェックが外れていたら、送信ボタンにdisabledを付ける
        element = document.getElementById("health_sonota");
        element.disabled = true;
    }
}

function sonotafunction(){
    //チェックとフォームの要素取得
    element = document.getElementById("health_sonota");
    form=document.getElementById("sonotaform")
    //チェックのvalueにフォームのvalueを代入
    if(form==null)form="その他";
    element.value=form.value;
}




