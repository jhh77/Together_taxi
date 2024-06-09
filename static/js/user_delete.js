$('.form').on('submit', function(event) {
    if (!$('#flexCheckDefault').is(':checked')) {
        event.preventDefault();
        $('#flexCheckDefault').focus();
        $('.error').text('유의사항을 모두 확인했는지 체크해주세요.');
    }
})