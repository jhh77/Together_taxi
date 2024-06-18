//textarea 높이 조절, 글자 수 카운트해서 표시하기
$('#write-text').on('input', function() {
    //높이 조절(내부 콘텐츠 만큼 height가 늘어나도록)
    $(this).css('height', 'auto');
    $(this).css('height', $(this)[0].scrollHeight + 'px');

    //글자 수 카운트
    let textLength = $(this).val().length;
    $('#text-count').text(textLength + ' / 150');

    if (textLength > 150) { //글자 수 150을 초과하지 않도록 설정 (maxlength는 한 글자가 초과되는 것이 발생)
        $(this).value =  $(this).slice(0, 150);
    }
});

//페이지 로딩 시 textarea에 focus 주기 + 원래 컨텐츠 길이 표시하기
$(document).ready(function() {
    const write = $('#write-text');
    write.focus();
    const textLength = write.val().length;
    console.log(textLength);
    $('#text-count').text(textLength + ' / 150');
});

//경로를 하나도 선택하지 않으면 폼 제출 막기
$('#submit-btn').on('click', function(evt) {
    if ($('.form-check-input:checked').length === 0) {
        // 만약 하나도 선택되지 않았다면 submit을 막음
        evt.preventDefault();
        $('.form-check-input')[0].focus();
        
    }
});
