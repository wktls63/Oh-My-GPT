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


// window.addEventListener("load", userSubscription);

// async function userSubscription() {

//     const UserSub = await getUserSubscriptionList();
//     const userSubTest = document.querySelector('#main-button')
//     console.log(UserSub[0].subscription_product)

//     if (UserSub[0].subscription_product === 0) {

//         let userHtml = `
//                                 <p>구독중인 상품 : OMG-BASIC</p>
//                             `
//         userSubTest.innerHTML = userHtml

//     } else if (UserSub[0].subscription_product === 1) {

//         let userHtml = `
//                                 <p>구독중인 상품 : OMG-PRO</p>
//                             `
//         userSubTest.innerHTML = userHtml
//     } else if (UserSub[0].subscription_product === 2) {

//         let userHtml = `
//                                 <p>구독중인 상품 : OMG-PROPLUS</p>
//                             `
//         userSubTest.innerHTML = userHtml

//     } else if (UserSub[0].subscription_product === 3) {

//         let userHtml = `
//                                 <p>구독중인 상품 : OMG-ENTERPRISE</p>
//                             `
//         userSubTest.innerHTML = userHtml;
//     }

// }



async function getUserSubscriptionList() {
    const response = await fetch('http://52.78.40.84:80/api/usersubscription');
    const data = await response.json();
    return data;
  }

