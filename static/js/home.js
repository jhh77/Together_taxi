// $(".pay-detail img").click(function(){
//     var imgSrc = $(this).attr("src");
//     if(imgSrc === "../static/image/check.png") {
//         $('this').attr("src", "../static/image/not-check.png");
//     } else {
//         $('this').attr("src", "../static/image/check.png");
//     }
// });

$(".pay-detail").click(function(){ //정산 부분 체크버튼 누르면
    const imgSrc = $(this).find('img').attr("src"); //img src 저장
    if(imgSrc === "../static/image/check.png") { //check 이미지면 uncheck 이미지로
        $(this).find('img').attr("src", "../static/image/not-check.png");
    } else { //uncheck 이미지 이면 check 이미지로
        $(this).find('img').attr("src", "../static/image/check.png");
    }
});