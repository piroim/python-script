Python 자동화 스크립트
- api_scan.py
- param_search.py

======
전체적으로 수정 필요
linkfinder 참고해서 정규표현식으로 가져오게 하는게 좋을 것 같음 

form 방식의 GET, POST는 가져오고
script나 js 파일에 있는 경로들은 '/a/b' 이렇게 되어 있는경우가 있으니 다 가져와서 GET요청해서 검증하는 방식으로 수정

=====
업데이트 방향성

1. wordlist를 기반으로, 전체 조회한 결과를 가져오도록 하는 코드 추가
예시

wordlist.txt
https://example1.com/
https://example2.com/
https://example3.com/

>> 3개의 도메인이 있을 때, 각각 한 줄씩 실행한 결과를 출력
>> 출력한 결과를 각 도메인별로 저장하는 것 까지 자동화
>>> 저장할 때, html 과 csv로 각각 저장해서 가시성 및 목록화할 수 있도록?

===
