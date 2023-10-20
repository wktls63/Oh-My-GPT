// 결제하기 버튼
const PayBtn = document.getElementById('order')
PayBtn.addEventListener('click', requestPay)

// 가맹 식별 코드
var IMP = window.IMP; 
IMP.init("imp11624762"); 

// Oh My GPT 상품 목록 가져오기
const subscriptionList = await getSubscriptionList();


const GPTPro = subscriptionList[0]
const GPTProPlust = subscriptionList[1]
const GPTEnterPrise = subscriptionList[2]

// 주문번호
var merchantt = new Date().getTime();

// 결제창 호출
function requestPay() {

    if (confirm("결제 하시겠습니까?")) {

        IMP.request_pay({
            pg : 'html5_inicis',
            pay_method : 'card',
            merchant_uid: "IMP"+merchantt, 
            name : GPTPro.item_name,
            amount : GPTPro.amount,
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
}





async function getSubscriptionList() {
    const response = await fetch('http://127.0.0.1:8000/api/subscription');
    const data = await response.json();
    return data;
  }

