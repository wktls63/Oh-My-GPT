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

    const login_response = await fetch('http://127.0.0.1:8000/api/auth', data);

    if(login_response.status == 200) {
        alert('로그인 성공!')
        location.href = 'http://127.0.0.1:8000/'
    } else {
        alert("사용자명과 비밀번호를 확인해 주세요.")
    }
}

// 로그인되어있을 때 로그인 버튼 비활성화 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


// 로그아웃 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

const proFileLogout = document.getElementById('logout-buttons')

proFileLogout.addEventListener('click', logout)


async function logout() {
    const logout_response = await fetch('http://127.0.0.1:8000/instragram/api/logout')

    if(logout_response.status == 200) {
        alert('로그아웃 되었습니다.')
        location.href = 'http://127.0.0.1:8000/'
    }
}

// 회원가입 - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

const signUpBtn = document.querySelector('#sign-up-btn');
signUpBtn.addEventListener('click', function(event) {
  event.preventDefault(); // 기본 제출 동작 중지
  signUp(); // signUp 함수 호출
});

async function signUp(){
  let email       = document.getElementById('sign-up-email').value;
  let password    = document.getElementById('sign-up-password').value;

  const data = setFetchData("post", {
    email : email,
    password : password,
  });

  const signup_response = await fetch('http://127.0.0.1:8000/api/register', data);
  const response_data = await signup_response.json();

  if (signup_response.status === 200) {
    alert('회원 가입이 성공적으로 완료되었습니다.');
    location.href = 'http://127.0.0.1:8000/user/login/';
  } else {
    // 예: 서버에서 "이미 존재하는 이메일 주소입니다."와 같은 메시지를 반환할 수 있습니다.
    alert(response_data.error);
  }
}