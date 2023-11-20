  <div align="center">
    <img src="https://velog.velcdn.com/images/minokimm/post/453d7279-1a51-46a8-8098-055393c36690/image.jpeg" width="80%"/>
  </div>

</br>
<p align="center">
  <b>"GPT를 기반으로 사용자에게 민원 데이터 및 맞춤형 데이터를 학습한 </br> 대화형 AI 서비스를 제공합니다."</b></br>
  <a>제 5회 K-Digital Training 해커톤 고용노동부장관상 수상 <b>"OMG: Oh! My GPT"</b>입니다.</a>
</p>

<div align="center">
  <img src="https://velog.velcdn.com/images/minokimm/post/676b8d78-2bf1-4121-91ad-d5db522c8677/image.png" width="50%"/>
</div>



</br>

## 📝 목차

1. [**웹 서비스 소개**](#1)
2. [**개발 기간 및 일정**](#2)
3. [**기술 스택**](#3)
4. [**문서**](#4)
5. [**협업 방식**](#5)

</br>

<div id="1"></div>

## 🎥 웹 서비스 소개
---
### 서비스 개발 목표
<div align="center">
  <img src="https://velog.velcdn.com/images/minokimm/post/89c56971-7446-4d80-9a2d-4cfb9f606d27/image.png">
</div>

### 추후 개발 방향
  <div align="center">
    
   ![O M G  Oh my girl (7)](https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/assets/81272766/5ac7c00b-6809-4a9a-9d60-d5b44b73336a)

  </div>


<br />

<div id="2"></div>

## 🔖  Oh My GPT ERD
---

  ![image](https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/assets/107481916/f3eaaa98-e47d-4966-b27d-ee69fd522af2)

<br/>


<br />

<div id="3"></div>

## 📈 Git Branch 전략
---
<p>
  - 개발은 로컬 환경에서 작업 단위로 `feature` branch를 생성해서 개발 및 테스트 후, remote `feature` branch로 푸시하고 remote `develop` branch에 PR을 생성하여 코드 리뷰 후에 병합합니다. 그 후, `develop` 와 `main` branch 간 commit 수 차이가 10개 이상 벌어지면 `main` 브랜치에 PR을 생성하여 병합합니다.


- 기본 브랜치 : `main` 브랜치로 항상 존재하는 브랜치
- 보조 브랜치 : `각 목적에 맞게 사용`하며 기본 브랜치에 병합하고 더 이상 사용하지 않으면 삭제
    - feature(기능) / bugfix(버그 수정) / hotfix(긴급 버그 수정) / refactor(리팩토링) / docs(문서) / test(테스트) / conf(설정)
</p>

<br />

<div id="4"></div>

## 📅 개발 기간 및 일정
---
<p>
  2023.10.10(화) ~ 2023.11.28(화)<br/>
</p>

<br />

<div id="4"></div>

## 🛠 기술 스택
---
### Frontend  
<div align="center">  
<a href="https://en.wikipedia.org/wiki/HTML5" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/html5-original-wordmark.svg" alt="HTML5" height="100" /></a>  
<a href="https://www.w3schools.com/css/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/css3-original-wordmark.svg" alt="CSS3" height="100" /></a>  
<a href="https://www.javascript.com/" target="_blank"><img style="margin: 10px" src="https://profilinator.rishav.dev/skills-assets/javascript-original.svg" alt="JavaScript" height="100" /></a>  
</div>

</td><td valign="top" width="33%">


### Backend  
<div align="center">  
<a href="https://www.python.org/" target="_blank"><img style="margin: 100px" src="https://profilinator.rishav.dev/skills-assets/python-original.svg" alt="Python" height="100" /></a>  
<a href="https://www.djangoproject.com/" target="_blank"><img style="margin: 100px" src="https://profilinator.rishav.dev/skills-assets/django-original.svg" alt="Django" height="100" /></a>  
<a href="https://www.postgresql.org/" target="_blank"><img style="margin: 100px" src="https://profilinator.rishav.dev/skills-assets/postgresql-original-wordmark.svg" alt="PostgreSQL" height="100" /></a>  
<a href="https://aws.amazon.com/" target="_blank"><img style="margin: 100px" src="https://profilinator.rishav.dev/skills-assets/amazonwebservices-original-wordmark.svg" alt="AWS" height="100" /></a>  
</div>

</td><td valign="top" width="33%">
</br>

<div id="5"></div>

## 📜 문서
---

<div>
  <a href='http://oreumi.site:1217/docs#/'>Fast API Docs</a>
</div>
<div>
  <a href='https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/wiki/Oh-My-GPT-API-Reference'>Oh-My-GPT-API-Reference</a>
</div>
<div>
  <a href='https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/wiki/Oh-My-GPT-%EA%B8%B0%EB%8A%A5-%EB%AA%85%EC%84%B8%EC%84%9C'>Oh-My-GPT 기능 명세서</a>
</div>

</br>

<div id="5"></div>

## 👨‍👨‍👦‍👦 협업 방식
---

- 역할 별로 브랜치를 나눈 후, 도맡아 진행되었습니다.
<table align="center">
  <tr>
    <td align="center">
      <a>
        <b>김나영</b>
      </a>
    </td>
    <td align="center">
      <a>
        <b>김민호</b>
      </a>
    </td>
    <td align="center">
      <a>
        <b>노경민</b>
      </a>
    </td>
    <td align="center">
      <a>
        <b>이준형</b>
      </a>
    </td>
    <td align="center">
      <a>
        <b>김유진</b>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
<a>
  
![nayung](https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/assets/81272766/30c295c4-c1b7-40a7-aa82-ff3ce6fd5f12)

</a>      
    </td>
    <td align="center">
<a>
  
![mino](https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/assets/81272766/154d3e95-de09-4505-94e2-45ee63011761)

</a>
    </td>
    <td align="center">
<a>
  
![kyungmin](https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/assets/81272766/8cdbb850-b302-4031-a34e-ca6d2ce2b05c)

</a>
    </td>
    <td align="center">
<a>
  
![lee](https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/assets/81272766/40b58f31-7d55-44bb-82f6-8f0302b58149)

</a>
    </td>
    <td align="center">
<a>

![super](https://github.com/wonjo-oh-my-girl/kdt-oh-my-gpt/assets/81272766/6be43dca-5490-4f82-99d1-159f4001bad6)

</a>
    </td>
  </tr>
</table>

- 코드 컨벤션, 깃 컨벤션을 따라 작업했습니다.
- google sheet에서 각자 일정 및 업무를 정하였습니다.
- 각자 공부하거나 참고할만한 자료를 올려 다함께 공유했습니다. 
