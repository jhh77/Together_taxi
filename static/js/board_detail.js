//textarea 높이 조절, 글자 수 카운트해서 표시하기
$('#comment-area').on('input', function() {
    //높이 조절(내부 콘텐츠 만큼 height가 늘어나도록)
    $(this).css('height', 'auto');
    $(this).css('height', $(this)[0].scrollHeight + 'px');

    //글자 수 카운트
    let textLength = $(this).val().length;
    $('#text-count').text(textLength + ' / 100');

    if (textLength > 100) { //글자 수 150을 초과하지 않도록 설정 (maxlength는 한 글자가 초과되는 것이 발생)
        $(this).value =  $(this).slice(0, 100);
    }
});
//-------------------------

//수정하기, 삭제하기 버튼 뜨고 사라지게 하기
$('#dots-btn').on('click', function() { //...점 버튼 눌렀을 때
    if ($('.edit-btn').is(':hidden')) { //버튼이 안 보이는 상태면
        $('.delete-btn').slideDown(function() { //버튼이 뜨도록
            $('.edit-btn').slideDown();
        });
    } else {
        $('.edit-btn').slideUp('fast', function() { //버튼이 떠있으면 사라지도록
            $('.delete-btn').slideUp('fast');
        });
    }
});
//-------------------------

//모달창 뜨게 하기
const modal = $('#modal'); //모달 변수에 저장

$('.delete-btn').on('click', function() { //삭제하기 버튼 누르면 모달창 뜨기
    modal.slideDown(); 
});

$('.closePopup').on('click', function() { // 아니오를 누르면 모달창이 사라지기
    modal.slideUp();
});

$('.btn-close').on('click', function() { // X를 누르면 모달창이 사라지기
    modal.slideUp();
});
//-------------------------

//정산하기 창 뜨게 하기
$('.state-btn').on('click', function() { //모임 게시글의 버튼을 눌렀을 때
    if ($(this).text() == '정산하기') { //만약 정산하기 버튼이라면 정산하기 창 뜨게 하기
        $('.settle-modal').slideDown(); 
    }
});

$('.cancel-btn').on('click', function() { //취소를 누르면 정산하기 모달이 사라지게 하기
    $('.settle-modal').slideUp(); 
});

// 택시 모임 금액 0이나 음수로 입려하면 제출 막기
$('.yes-btn').on('click', function(event) {
    amount = $('#user_id').val();
    if (amount <= 0) {
        event.preventDefault();
        $('.error').text('금액을 확인해주세요.');
    }
});

//높이 조절
$(document).ready(function() {
    let height = $(document).height();
    $('body, html').css('height', height + 150 + 'px');
});