var IMP = window.IMP; 
IMP.init("imp11624762"); 

var today = new Date();   
var hours = today.getHours(); // 시
var minutes = today.getMinutes();  // 분
var seconds = today.getSeconds();  // 초
var milliseconds = today.getMilliseconds();
var makeMerchantUid = hours +  minutes + seconds + milliseconds;

var merchantt = new Date().getTime();


function requestPay() {
    IMP.request_pay({
        pg : 'kakaopay.TC0ONETIME',
        pay_method : 'card',
        merchant_uid: "IMP"+merchantt, 
        name : '당근 1kg',
        amount : 100,
        buyer_email : 'Iamport@chai.finance',
        buyer_name : '아임포트 기술지원팀',
        buyer_tel : '010-1234-5678',
        buyer_addr : '서울특별시 강남구 삼성동',
        buyer_postcode : '123-456'
    }, function (rsp) { // callback
        if (rsp.success) {
            console.log(rsp);
        } else {
            console.log(rsp);
        }
    });
}