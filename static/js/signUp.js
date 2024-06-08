//비밀번호 보이게 하는 기능
// attr() 메서드는 요소의 속성을 가져오거나 설정
$('#passwd-icon').click(function() {
    const fieldType = $('#password1').attr('type');
    const passwordField = $('#password1');

    console.log(fieldType);
    console.log($('#passwd1-icon img').attr('src'));

    if (fieldType === 'password') {
        passwordField.attr('type', 'text'); // 텍스트로 변경하여 비밀번호가 가려지지 않게 함
        $('#passwd-icon img').attr('src', '../../static/image/eye-open.png'); // 이미지 경로 변경하여 아이콘 변경
    } else {
        passwordField.attr('type', 'password'); // 비밀번호 입력 필드의 타입을 다시 password로 변경하여 비밀번호를 가리게 함
        $('#passwd-icon img').attr('src', '../../static/image/eye-close.png'); // 이미지 경로 변경하여 아이콘 변경
    }
});

//아이디 중복검사 서버에 요청하기
$('#idCheckBtn').click(function () {
    let userId = $('#user_id').val(); //아이디 값 가져오기
    if (userId) { //값이 있으면
        $.ajax({ //서버로 요청
            url: '/accounts/signUp/id-check/',
            type: 'POST',
            data: {
                'user_id': userId, //아이디값 주기
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val() //보안을 위해
            },
            success: function (data) {
                if (data.is_taken) {
                    $('#idCheckSuccess').val("false"); // 중복 검사 실패
                    $('#idCheckResponse').text('이미 사용 중인 아이디입니다.');
                    $('#idCheckResponse').css('color', '#E07070');
                    $('#user_id').focus()

                } else {
                    $('#idCheckSuccess').val("true"); // 중복 검사 성공
                    $('#idCheckResponse').text('사용 가능한 아이디입니다.');
                    $('#idCheckResponse').css('color', '#5D6DBE');
                }
            }
        });
    } else {
        $('#idCheckResponse').text("아이디를 입력해주세요.");
    }
});

// 폼 제출 시, 중복 검사가 성공적으로 이뤄졌는지 확인
$('.submit-btn').click(function (e) {
    const isIdChecked = $('#idCheckSuccess').val();
    if (isIdChecked !== "true") {
        $('#idCheckResponse').text("아이디 확인 후 중복 검사를 해주세요.");
        $('#idCheckResponse').css('color', '#E07070');
        return false; // 폼 제출 방지
    }
});
