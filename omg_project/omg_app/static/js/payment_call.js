// csrf 쿠키
function getCookie(name) {
    /* 이름값의 cookie 값 가져오기 */

    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {

        const cookies = document.cookie.split(';');

        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// fetch 함수 정의
function setFetchData(method, body){
    /* Fetch data 셋팅 */

    let csrftoken   = getCookie('csrftoken');

    const data = {
        method: method,
        headers: {
            'content-type': 'application/json',
            'X-CSRFToken' : csrftoken,        
        },
        body: JSON.stringify(body)
    }

    return data
}

let uuidCode = ([1e7]+-1e3+-4e3+-8e3+-1e11).replace(/[018]/g, c =>
(c ^ crypto.getRandomValues(new Uint8Array(1))[0] & 15 >> c / 4).toString(16));

// 결제하기 버튼
// Oh my Gpt Pro
const omgPro = document.getElementById('omgpro')
omgPro.addEventListener('click', requestPaygptPro)

// Oh my Gpt Pro Plus
const omgProPlus = document.getElementById('omgproplus')
omgProPlus.addEventListener('click', requestPaygptProPlus)


// Oh my Gpt EnterPrise
const omgEnterPrise = document.getElementById('omgenterprise')
omgEnterPrise.addEventListener('click', requestPaygptEnterPrise)



// 가맹 식별 코드
var IMP = window.IMP; 
IMP.init("imp11624762"); 

// Oh My GPT 상품 목록 가져오기
const subScripTionList = await getSubscriptionList();

// 상품 목록 변수
const gptPro = subScripTionList[0]
const gptProPlust = subScripTionList[1]
const gptEnterPrise = subScripTionList[2]

// 주문번호
var merchantt = new Date().getTime();

// 결제창 호출

// 프로
function requestPaygptPro() {

    if (confirm("결제 하시겠습니까?")) {

        IMP.request_pay({
            pg : 'html5_inicis',
            pay_method : 'card',
            merchant_uid: uuidCode, 
            name : gptPro.item_name,
            amount : gptPro.amount,
            buyer_email : 'Iamport@chai.finance',
            buyer_name : '아임포트 기술지원팀',
            buyer_tel : '010-1234-5678',
            buyer_addr : '서울특별시 강남구 삼성동',
            buyer_postcode : '123-456',
        }, function (rsp) { // callback
            if (rsp.success) {
                console.log(rsp);
                console.log('결제가 완료되었습니다.');
                const itemcode = 1
                    storeImpIdInDB(rsp.merchant_uid, rsp.paid_amount, rsp.status, itemcode);
            } else {
                console.log(rsp);
            }
        });
    }
}

// 프로 플러스
function requestPaygptProPlus() {

    if (confirm("결제 하시겠습니까?")) {

        IMP.request_pay({
            pg : 'html5_inicis',
            pay_method : 'card',
            merchant_uid: uuidCode, 
            name : gptProPlust.item_name,
            amount : gptProPlust.amount,
            buyer_email : 'Iamport@chai.finance',
            buyer_name : '아임포트 기술지원팀',
            buyer_tel : '010-1234-5678',
            buyer_addr : '서울특별시 강남구 삼성동',
            buyer_postcode : '123-456',
            itemcode : 2
        }, function (rsp) { // callback
            if (rsp.success) {
                console.log(rsp);
                console.log('결제가 완료되었습니다.');
                const itemcode = 2
                    storeImpIdInDB(rsp.merchant_uid, rsp.paid_amount, rsp.status, itemcode);
            } else {
                console.log(rsp);
            }
        });
    }
}

// 엔터프라이즈
function requestPaygptEnterPrise() {

    if (confirm("결제 하시겠습니까?")) {

        IMP.request_pay({
            pg : 'html5_inicis',
            pay_method : 'card',
            merchant_uid: uuidCode, 
            name : gptEnterPrise.item_name,
            amount : gptEnterPrise.amount,
            buyer_email : 'Iamport@chai.finance',
            buyer_name : '아임포트 기술지원팀',
            buyer_tel : '010-1234-5678',
            buyer_addr : '서울특별시 강남구 삼성동',
            buyer_postcode : '123-456',
            itemcode : 3
        }, function (rsp) { // callback
            if (rsp.success) {
                console.log(rsp);
                console.log('결제가 완료되었습니다.');
                const itemcode = 3
                    storeImpIdInDB(rsp.merchant_uid, rsp.paid_amount, rsp.status, itemcode);
            } else {
                console.log(rsp);
            }
        });
    }
}


// 결제 완료 후, 포트원에서 보낸 결제번호를 DB에 저장
async function storeImpIdInDB(merchant_id, amount, status, subscription_product_id) {
    
    const data = setFetchData('POST', {
        merchant_id: merchant_id,
        amount: amount,
        status: status, 
        subscription_product_id : subscription_product_id

    })
    const response = await fetch('http://52.78.40.84:80/api/validation', data)

    if (response.status === 200) {

        alert('결제가 완료됐습니다.');

    } else if (response.status === 423) {

        alert("이미 결제된 상품 입니다.");

    } else if (response.status === 418) {

        alert("이미 구독중인 상품이 있습니다.");

    } else {

        alert("문제가 발생했습니다. 다시 시도해주세요.");

    }
}

async function getSubscriptionList() {
    const response = await fetch('http://52.78.40.84:80/api/subscription');
    const data = await response.json();
    return data;
  }

