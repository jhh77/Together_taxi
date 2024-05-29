//비밀번호 보이게 하는 기능
// attr() 메서드는 요소의 속성을 가져오거나 설정
$('#passwd-icon').click(function() {
    const fieldType = $('#password').attr('type');
    const passwordField = $('#password');

    console.log(fieldType);
    console.log($('#passwd-icon img').attr('src'));

    if (fieldType === 'password') {
        passwordField.attr('type', 'text'); // 텍스트로 변경하여 비밀번호가 가려지지 않게 함
        $('#passwd-icon img').attr('src', '../../static/image/eye-open.png'); // 이미지 경로 변경하여 아이콘 변경
    } else {
        passwordField.attr('type', 'password'); // 비밀번호 입력 필드의 타입을 다시 password로 변경하여 비밀번호를 가리게 함
        $('#passwd-icon img').attr('src', '../../static/image/eye-close.png'); // 이미지 경로 변경하여 아이콘 변경
    }
});