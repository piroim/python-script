┌─────────────────────────────────────────────────────────────┐
│                        Scanner Core                         │
│                   (오케스트레이션&결과 집계)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      HTML Parser                            │
│                  (DOM 파싱 & 모듈 분배)                       │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  Tag Modules  │    │ Script Module │    │ Inline Module │
│  (플러그인)    │    │   (JS 분석)   │    │ (인라인 JS)   │
└───────────────┘    └───────────────┘    └───────────────┘
        │
        ├── FormExtractor
        ├── AnchorExtractor
        ├── InputExtractor
        └── ... (확장 가능)
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Result Aggregator                         │
│              (중복 제거, 정규화, 출력 포맷팅)                  │
└─────────────────────────────────────────────────────────────┘

====
# 전체 구조

scanners/
├── core/
│   ├── scanner.py          # 메인 오케스트레이터
│   ├── parser.py           # HTML 파싱 담당
│   └── result.py           # 결과 데이터 클래스
│
├── extractors/             # 태그별 추출 모듈
│   ├── base.py             # 추상 베이스 클래스
│   ├── form_extractor.py   # <form> 처리
│   ├── anchor_extractor.py # <a href> 처리
│   ├── input_extractor.py  # <input> 독립 처리
│   └── meta_extractor.py   # <meta> 태그 등
│
<!-- ├── analyzers/              # JS 분석 모듈
│   ├── base.py
│   ├── ajax_analyzer.py    # $.ajax, fetch 등
│   ├── axios_analyzer.py   # axios 호출
│   └── inline_analyzer.py  # 인라인 스크립트 -->
│
├── utils/
│   ├── url_normalizer.py   # URL 정규화
│   └── pattern_matcher.py  # 정규표현식 패턴
│
├── output/
│   ├── json_formatter.py
│   └── csv_formatter.py
│
├── save/ #추출한 데이터들을 저장하는 곳 최종 URL+Param 구조로?
│
└── main.py #메인에서 URL 입력하면 실행하는 구조
    