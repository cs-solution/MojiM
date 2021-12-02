
// 性格表示
const setSeikakuValue = (val) => {
    let seikakVal="";
    switch(val){
        case '1': seikakVal="優しい　　"; break;
        case '2': seikakVal="やや優しい"; break;
        case '3': seikakVal="ノーマル　"; break;
        case '4': seikakVal="ややきつい"; break;
        case '5': seikakVal="きつい　　"; break;
        default: break;
    }
    document.getElementById('seikaku-value').innerText = seikakVal;
}
const rangeOnChange = (e) =>{
    setSeikakuValue(e.target.value);
}


window.onload = () => {
    if(document.getElementById('id_tgtSeikaku') != null){
        document.getElementById('id_tgtSeikaku').addEventListener('input', rangeOnChange); // スライダー変化時にイベントを発火
        setSeikakuValue(document.getElementById('id_tgtSeikaku').value); // ページ読み込み時に値をセット
    }
    if(document.getElementById('id_imgUrl') != null){
        if (isSmartPhone() == false){
            document.getElementById('id_imgUrl').className = "result-Img-2"
        }
    }
}

// 画像プレビュー
$("#id_tgtImg").on("change", function() {
    if($("#id_tgtImg").length>0){
        var fileReader = new FileReader();
        fileReader.onload = (function () {
            var canvas = document.getElementById('preview');
            var ctx = canvas.getContext('2d');
            var image = new Image();
            image.src = fileReader.result;
            image.onload = (function () {
                canvas.width = image.width;
                canvas.height = image.height;
                ctx.drawImage(image, 0, 0);
            });
        });
        fileReader.readAsDataURL(document.getElementById('id_tgtImg').files[0]);
        document.querySelector("button").disabled = false;
    }    
});

// スマホかPCか
function isSmartPhone() {
    if (navigator.userAgent.match(/iPhone|Android.+Mobile/)) {
      return true;
    } else {
      return false;
    }
}
