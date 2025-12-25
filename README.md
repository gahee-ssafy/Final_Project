# 첫 적금 메이트 JJuns 🐷💰  
사회초년생의 첫 적금 선택을 돕는 스마트 금융 파트너  

---

## 📌 프로젝트 개요
- **프로젝트명**: 첫 적금 메이트 JJuns  
- **설명**: 금융 지식이 부족한 사회초년생을 위해 예·적금 상품을 쉽고 직관적으로 비교하고, AI 기반 추천을 제공하는 금융 서비스  
- **기간**: 2025.12.19. ~ 2025.12.26.  

---

## 🎯 문제 정의 & 타겟 사용자

### 😵 문제 상황
- 예·적금 상품이 너무 많아 선택이 어려움  
- 우대조건, 가입채널, 적립방식 등 조건이 복잡  
- 개인 상황에 따라 유리한 상품이 달라 비교가 번거로움  

### 👤 타겟 사용자
- 사회초년생 (첫 월급, 첫 저축)  
- 금융 용어와 상품 구조가 익숙하지 않은 사용자  
- “뭐가 좋은지 모르겠어요” 단계의 사용자  

---

## ⭐ 서비스 특징
- 일상적인 언어로 소통하는 **AI 맞춤 추천 기능**  
- 예·적금 정보, 경제 지표, 금융 콘텐츠를 **한 화면에서 통합 제공**  
- 복잡한 금융 정보를 직관적인 UI로 시각화  

---

## ⚙️ 주요 기능

- 회원가입 / 로그인  
- 예·적금 상품 조회 및 검색·필터·정렬  
- 상품 비교 및 즐겨찾기  
- AI 상품 추천 및 추천 사유 제공  
- 근처 은행 검색 (카카오맵 API)  
- 커뮤니티 기능 (게시글/댓글 CRUD)  
- 가입 상품 금리 비교 및 회원 정보 수정  
- 금융 학습용 유튜브 영상 제공  

---

## 🦾 팀 소개
| 이름 |
| --- |
| 전연수 |
| 전가희 |

---
<br />

## 🏗️기술 스택


### Backend
![Django](https://img.shields.io/badge/Django-092E20.svg?style=for-the-badge&logo=django&logoColor=white)&nbsp;
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)&nbsp;
![sqlite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=nodedotjs&logoColor=white)&nbsp;


### Frontend
![Vue.js](https://img.shields.io/badge/vue.js-4FC08D?style=for-the-badge&logo=vuedotjs&logoColor=white)&nbsp;


### DevOps
![Git](https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white)&nbsp;
![Github](https://img.shields.io/badge/Github-000000?style=for-the-badge&logo=github&logoColor=white)&nbsp;


### Tools
![Notion](https://img.shields.io/badge/Notion-000000?style=for-the-badge&logo=Notion&logoColor=white)&nbsp;
![VS code](https://img.shields.io/badge/Visual%20Studio%20Code-007ACC?style=for-the-badge&logo=visualstudiocode&logoColor=white)&nbsp;
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)&nbsp;


<br />

---

## 📁 프로젝트 폴더 구조

### Backend (Django)
```
backend
├─ accounts
├─ community
├─ products
└─ project
```

### Frontend (Vue.js)
```
frontend
├─ public
└─ src
    ├─ assets
    ├─ components
    ├─ router
    ├─ stores
    └─ views
        ├─ community
        ├─ youtube
        └─ etc
```

---

## 🔍 기능 상세 설명

### 예·적금 조회 및 필터
- 금융감독원 API를 통해 수집한 상품 데이터를 가공하여 제공  
- 은행명, 저축 기간, 상품명 기반 검색 지원  
- `prefetch_related`를 활용한 DB 성능 최적화  

### 커뮤니티 기능
- 게시글 / 댓글 CRUD 구현  
- 작성자만 수정·삭제 가능하도록 권한 제어 적용  

### 마이페이지 & 회원 정보 관리
- 가입 상품 리스트 및 금리 비교 시각화  
- 회원 정보 부분 수정(PATCH) 지원  

### 🤖 AI 상품 추천
- 사용자 입력을 임베딩하여 상품 벡터와 유사도 계산  
- 코사인 유사도 기반 상위 3개 상품 추천  
- 추천 상품별 최고 우대 금리와 추천 사유 제공  

---

## 📚 학습 내용
- Django REST Framework와 Vue.js 연동 구조 이해  
- 프론트엔드–백엔드 데이터 흐름 설계 경험  
- API 키를 환경변수로 관리하는 보안 방식 학습  
- Git 브랜치 전략과 Merge 충돌 해결 경험  
- 사용자 중심 UI/UX 설계의 중요성 체감  

---

## 💡 느낀 점


전연수

짧은 기간 동안 기획부터 구현, 협업까지 프로젝트 전 과정을 경험하며
단순한 기능 구현을 넘어 **협업과 구조 설계의 중요성**을 깊이 체감할 수 있었습니다.

특히 Merge 충돌 해결과 프론트엔드–백엔드 연동 과정에서
실무와 유사한 문제를 직접 마주하고 해결하며 개발 역량을 한 단계 끌어올릴 수 있었습니다.
이를 통해 “동작하는 서비스”를 넘어서,
사용자에게 실제로 가치 있는 서비스를 만드는 관점을 갖게 된 점이 가장 큰 수확이었습니다.

---

전가희

초기 단계에서 리드 개발자가 기본 개발 환경과 공통 구조를 선구축한 뒤
기능 단위로 역할을 분담하는 방식이 협업 효율을 크게 높일 수 있다는 점을 체감했습니다.

또한 개발 과정에서 발생하는 논의와 의사결정 내용을
즉시 문서로 기록하고 공유하는 것이 매우 중요하다는 것을 배웠습니다.
사람의 기억에는 한계가 있지만, 기록은 팀의 작업 흐름을 명확히 하고
모든 팀원이 같은 방향으로 나아가도록 돕는다는 점에서
**‘기억보다 기록이 더 중요하다’**는 교훈을 얻은 프로젝트였습니다.


---

## 🚀 향후 개선 방향
- 머신러닝 기반 개인화 추천 고도화  
- 클라우드 배포 및 성능 모니터링  
- CI/CD 파이프라인 구축  
- 사용자 피드백 기반 UI/UX 개선  

---


