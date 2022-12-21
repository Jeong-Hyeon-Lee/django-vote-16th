# django-vote-16th
신촌 창업 IT 동아리 ceos의 16기 개발팀(Back-End / Front-End) 파트장 투표 및 Demo Day 투표를 위한 서비스

## 개발 환경
django, Docker, nginx, MySQL, EC2, RDS route53

## 기능 소개
### 주요 기능 목록
- 사용자 관련 기능
    - 회원가입
    - 로그인
    - 로그아웃
- 파트장 투표
- 데모데이 투표
### 회원가입

- id, password, team, email, part, name 입력
- access token, refresh token 반환
- refresh token 쿠키에 저장
- password는 re 모듈을 이용하여 8자 이상의 영문 대/소문자, 숫자, 특수문자 조합으로 유효성 검사
- part는 choices를 이용해 미리 선택 가능한 목록 구성
    
    ```python
    PART_CHOICES = {
        ('front', 'Front-end'),
        ('back', 'Back-end'),
        ('design', 'Design'),
        ('plan', 'Plan')
    }
    ```
    
- team은 DB에 미리 저장해놓은 정보를 FK로 활용
    
    ```python
    TEAM_CHOICES = {
        ('teample', 'Teample'),
        ('finble', 'Finble'),
        ('prefolio', 'Pre:folio'),
        ('diametes', 'diaMEtes'),
        ('recipeasy', 'recipeasy'),
    }
    ```
    

### 로그인

- id, password 입력
- django의 authenticate 기능 활용
- access token, refresh token 반환
- refresh token 쿠키에 저장
- access token 만료시에 refresh token으로 재발급 요청 가능

### 로그아웃

- 로그인 상태에서만 실행 가능
- 쿠키에 있던 refresh token 삭제

### 파트장 투표 반영

- 로그인 상태에서만 실행 가능
- User의 `part_voted` 필드를 통해서 투표 여부를 판별하여 아직 투표하지 않은 사용자만 투표 가능
- `results/<str:part>/` url에 입력된 part(back, front)가 로그인한 사용자의 part 정보와 일치하는 경우에만 투표 반영

### 파트장 투표 결과 확인

- `results/<str:part>/` url에 part명(back, front) 입력하면 해당 파트의 결과만 출력
- 투표 수 기준으로 내림차순 정렬
- 사용자와 후보 테이블을 구분하여 모든 사용자가 회원가입을 하기 전에도 후보로 확인 및 투표 가능

### 데모데이 투표 반영

- 로그인 상태에서만 실행 가능
- User의 `demo_voted` 필드를 통해서 투표 여부를 판별하여 아직 투표하지 않은 사용자만 투표 가능
- request body의 team이 로그인한 사용자의 team 정보와 일치하지 않는 경우에만 투표 반영

### 데모데이 투표 결과 확인

- 투표 수 기준으로 내림차순 정렬

## Database 구조 (ERD)
![image](https://user-images.githubusercontent.com/86969518/208895467-10ac3b87-956a-4ece-905b-7f193cd432d5.png)
#### Team: 팀을 저장하기 위한 테이블  
id: 자동 생성  
name: 팀 이름  
description: 한 줄 소개  
vote_num: 득표수 (default = 0)

미리 DB에 저장해두고 서비스에서 불러옴  
![image](https://user-images.githubusercontent.com/86969518/208897156-99bf73bf-8b62-44c3-855c-aeaed1600d74.png)

#### Candidate: 파트장 투표시 후보들을 저장하기 위한 테이블
id: 자동 생성  
name: 이름  
part: 소속 파트 (front, back)  
team: 소속 팀 (team 테이블 참조)  
vote_num: 득표수 (default = 0) 

미리 DB에 저장해두고 서비스에서 불러옴

![image](https://user-images.githubusercontent.com/86969518/208898097-c4d6a4f3-c78a-495c-8d93-00a54d95950c.png)

#### User: 회원 테이블
id: 회원가입 시 유저가 직접 입력  
password: 회원가입 시 유저가 직접 입력  
team: 소속 팀 (team 테이블 참조)  
email: 이메일  
part: 소속 파트(front, back, design, plan)  
name: 이름  
part_voted: 파트장 투표 여부 (default = False)   
demo_voted: 데모데이 투표 여부 (default = False)  

회원가입 요청 시 새 레코드 생성

## API 명세서
![image](https://user-images.githubusercontent.com/68368633/208912503-81801319-baf9-4dd0-871a-3e9f5dabb6cb.png)
[API 문서](https://www.notion.so/API-073c3d88ef384c889a9590e08bbf3184)
- notion 활용
- URI, method, header, request body, response body
- 접근 권한에 따라 token 필요 여부가 달라져서 해당 설명 추가

## 오류 해결 
- 겹치는 url 

    파트장 투표 관련 API와 데모데이 투표 관련 API를 다음과 같은 url로 받았었는데 분명 database에 팀 데이터가 들어가있는데도 
results/demo/에 요청을 보내면 빈 데이터셋만 리턴되었다.  

    알고보니 url이 겹쳐서 demo가 results/<str: part>/의 part 인자로 전달되고 있었고, 후보는 front 또는 back만 part로 가지므로 
그런 결과가 나온 것이었다.
    ```python
    path('results/<str:part>/', VoteResult.as_view()),
    path('results/demo/', DemoVoteResult.as_view()),
    ```

    다음과 같이 url을 수정해 오류를 해결했다.
    ```python
    path('results/<str:part>/', VoteResult.as_view()),
    path('demo-results/', DemoVoteResult.as_view()),
    ```

- 화면에 css가 적용이 되지 않음  

    drf가 기본으로 제공하는 테스트 화면이 css가 적용되지 않고 밑 화면처럼 깨진 화면으로 보였다.  
![image](https://user-images.githubusercontent.com/86969518/208905032-7ce0833e-14f1-4fd6-a4b7-9884299d016d.png)

    폴더 구조 때문에 static 파일의 경로가 잘못된 것이었고, 전체적으로 경로를 맞추어 해결했다.  
Dockerfile.prod를 비롯해 배포에 사용된 파일들, 그리고 코드 파일들은 deploy.yml을 제외하고 전부 finble 폴더 안에 있는데 
deploy.yml에서 .env 파일을 최상단에 만들었기 때문에  
.env 파일을 이용하기 위해 docker-compose.prod.yml에서 .env를 절대경로로 참조했다.


- DB migration이 안되는 문제  

    가장 오래 겪었던 문제 중 하나이다. API 요청을 보내면 Server Error (500)이 떴는데 workbench로 확인해보니 연결해둔 rds에 db 스키마가 없었다.  
지난번 과제에서도 이 부분에서 고생을 많이 했기 때문에 왜 같은 방식으로 한 것 같은데 이번에는 안되지? 생각을 많이 했다.  

    두 가지 방법으로 해결을 했다..  
1. migration 파일을 올리기 -> rds 생성 -> rds에 migration 내용이 자동 적용됨  
 
    gitignore에 추가를 해둬서 처음에는 migrations 파일들은 서버에 올리지 않았었는데 이 부분에 대해서 조사를 해보다가
makemigrations 명령어 대신 migrations 파일을 올려서 배포할 수도 있다는 글을 보았다.

    스키마가 아직 존재하지 않는 새 rds를 연결하고 migrations 파일과 함께 배포하면 자동 migrate가 된다.  
그러나 이미 생성되고 연결된 rds가 있을 때 migrations 파일을 올리게 되면 적용이 되지 않는다.  
entrypoint.prod.sh에 migrate 명령어를 적었는데도 왜 migrate가 안되는지는 아직도 잘 모르겠다..  

    그래서 수정된 스키마를 적용하기 위해 rds를 꽤 여러번 다시 만들었다.  
처음에는 다른 방법을 못 찾아서 이렇게 했었는데 할 때마다 DB 내용도 날아가고 번거로웠기 때문에 수정을 자주 하다 보니 뭔가 아닌 것 같았다..  

2. 로컬에 있는 .env 파일에 임시로 서버 주소를 연결하고 파이참 터미널에서 migration 명령어 입력  

    1번 방법을 이용했던 이유 중 하나는 웹 컨테이너 안에 코드가 담겨있어서 서버 배포 후에 cli 창에서 python manage.py makemigrations나
python manage.py migrate 같은 명령어를 치게 되면 컨테이너 밖이라 django 관련 코드를 실행할 수 없었다는 것이다.  

    그래서 그냥 로컬환경과 연결되어 있던 .env 파일을 배포 때 사용되는 .env 파일처럼 잠시 수정한다음 파이참 터미널에서 명령어를 입력했다.  
그러니 DB를 날릴 필요없이 migration을 진행할 수 있었다.

    이 방법 말고 보편적으로 사용하는 더 좋은 방법이 있다면 알고 싶다.

- 503 Service Unavailable Error

    target의 EC2 인스턴스 연결문제였다. 다시 잘 연결하고 서브넷도 동일하게 바꿔서 해결했다.


- 400 Bad Request Error

    github secrets ENV_VARS에서 ALLOWED_HOSTS를 EC2 주소에서 domain 주소로 수정해서 해결했다. 이때 HOST는 EC2 주소 그대로 둬야한다!

### 회고
👩🏻‍💻혜진: 도메인까지 구입해서 배포한거는 처음이라 너무 신기했다. 심지어 우리팀 도메인은 `.com`이 없어서 `.xyz`인데 완전 크립토 인싸 같다.
인스턴스끼리 연결하고 로드밸런서 만들고 보안 설정이나 서브넷 설정이나 고려할 부분이 너무 많아서 애를 많이 먹었다.
가장 문제는 에러가 떠도 도통 어디에서 잘못된건지 파악이 안된다는 점이다ㅜㅠ 많은 도움 주신 아연님, 민준님 감사합니다 :) 헤헤
그래도 이번 배포로 되게 많은걸 알아가는 것 같아서 좋다! 본 프로젝트에서도 이번에 배운 내용을 써먹을 수 있을 것 같다. 정현아 같이 잘해보자구 🤓  

👩🏻‍💻정현: 간단한 프로젝트였지만 이것저것 삽질을 하면서 배우는 게 많았다!
특히 이번에도 배포를 하면서 어려움을 꽤 겪었는데 본 프로젝트에서는 지금보다 수월하게 할 수 있을 것 같아 앞으로가 더 기대된다.
이렇게 완전한 프로젝트 하나를 끝내고 제대로 배포하는 것은 처음인데 배포까지 성공해서 너무 뿌듯하다.😁