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



