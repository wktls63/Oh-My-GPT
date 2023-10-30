/* ----------------------- 화면 ------------------------- */

const container = document.getElementById('container');

// 로그인 관련
const signInButton = document.getElementById('signIn');

signInButton.addEventListener('click', function() {
  container.classList.remove("right-panel-active");
});


// 회원가입 관련
const signUpButton = document.getElementById('signUp');

signUpButton.addEventListener('click', function() {
  container.classList.add("right-panel-active");
});




/* ----------------------- 기능 ------------------------- */

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


// 로그인 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

// 로그인 등록 버튼
const loginButton = document.querySelector('#sign-in-btn')
loginButton.addEventListener('click', function(event) {
  event.preventDefault();
  login();
})

// 로그인 이벤트
async function login() {
    // email, password, password
    console.log(document.querySelector('#sign-in-email'));
    console.log(document.querySelector('#sign-in-password'));
    const email = document.querySelector('#sign-in-email').value;
    const password = document.querySelector('#sign-in-password').value;

    const data = setFetchData("post", {
        "email" : email,
        "password" : password,
    })

    const login_response = await fetch('http://52.78.40.84:80/api/auth', data);

    if(login_response.status == 200) {
        alert('로그인 성공!')
        location.href = 'http://52.78.40.84:80/'
    } else {
        alert("사용자명과 비밀번호를 확인해 주세요.")
    }
}