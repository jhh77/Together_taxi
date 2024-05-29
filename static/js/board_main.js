//kakao 자동차 길찾기 API
let REST_API_KEY = '5566c4b3fc243e60269fd1df4d99d5d6';
let origins = ['127.0382022,37.5608549', '127.0437075, 37.5546025', '127.0430252, 37.5659677'];

let fees = $('.fee');

$('#api-btn').click(function() {
//     let loading = `<div class="spinner-border spinner-border-sm text-warning" role="status">
//     <span class="visually-hidden">Loading...</span>
//   </div>`;
//   $('.fee').html(loading);
  callAPI();
});

// function callAPI() {
//     $.each(origins, function (index, value) {
//         let origin = value;
//         let destination = '127.0492745,37.558276';
//         $.ajax({
//             url: 'https://apis-navi.kakaomobility.com/v1/directions',
//             method: 'GET',
//             // dataType: 'json',
//             headers: {
//                 'Authorization': `KakaoAK ${REST_API_KEY}`,
//                 'Content-Type': 'application/json',
//             },
//             data: {
//                 origin: origin,
//                 destination: destination
//             }
//         }).done(function (data) {
//             let taxi_fee = data.routes[0].summary.fare.taxi;
//             console.log(taxi_fee);
//             console.log($(fees[index]), $(fees[index]).text());
//             $(fees[index]).text(taxi_fee + "원");
//         });
//     });
// }

async function callAPI() {
    for (let i = 0; i < origins.length; i++) {
        let origin = origins[i];
        let destination = '127.0492745,37.558276';
        try {
            let data = await $.ajax({
                url: 'https://apis-navi.kakaomobility.com/v1/directions',
                method: 'GET',
                // dataType: 'json',
                headers: {
                    'Authorization': `KakaoAK ${REST_API_KEY}`,
                    'Content-Type': 'application/json',
                },
                data: {
                    origin: origin,
                    destination: destination
                }
            });
            console.log(data.routes[0].summary);
            let taxi_fee = data.routes[0].summary.fare.taxi;
            console.log(taxi_fee);
            console.log($(fees[i]), $(fees[i]).text());
            $(fees[i]).text(taxi_fee + "원");
        } catch (error) {
            console.error('Error occurred:', error);
        }
    }
}
