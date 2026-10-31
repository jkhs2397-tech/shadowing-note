# 쉐도잉 노트

미드 쉐도잉 문장을 구조, 뉘앙스, 발음으로 복습하는 개인용 웹앱(PWA)입니다.
문장 데이터는 `sentences.json` 한 파일이고, 이 파일만 고치면 앱 내용이 바뀝니다.

- 문장 카드: 끊어 읽기, 해석, 구조, 뉘앙스, 발음(빠른 속도), 쉐도잉 팁, 응용 예문
- 퀴즈: 빈칸 채우기, 한국어 → 영어, 뜻 맞히기, 연음. 복습 간격(1, 3, 7, 14, 30일)을 자동 관리
- 30분마다 퀴즈 알림 (GitHub Actions + ntfy)
- 아이폰 홈 화면에 추가해서 앱처럼 사용

## 폴더 구성

```
index.html              앱 화면 전체
sentences.json          문장과 퀴즈 데이터 (여기만 수정)
manifest.webmanifest    홈 화면 설치 정보
sw.js                   오프라인 캐시
icons/                  앱 아이콘
scripts/quiz_push.py    퀴즈 알림 보내기
scripts/validate.py     sentences.json 검사
.github/workflows/quiz.yml   30분 스케줄
```

## 1. 앱 주소 열기

1. 저장소 **Settings → Pages → Build and deployment**에서 Source를 `Deploy from a branch`, Branch를 `main` / `/ (root)`로 저장합니다.
2. 1~2분 뒤 `https://jkhs2397-tech.github.io/shadowing-note/` 주소가 열립니다.
3. 아이폰 **사파리**로 그 주소를 열고 **공유 → 홈 화면에 추가**를 누릅니다.

## 2. 30분 퀴즈 알림 켜기

1. 아이폰 App Store에서 **ntfy** 앱을 설치합니다.
2. 추측하기 어려운 알림 주소 이름을 정합니다. 예: `shadow-` 뒤에 무작위 글자 12자 이상. 이름을 아는 사람은 누구나 같은 주소로 알림을 받거나 보낼 수 있으므로 공개하지 마세요.
3. ntfy 앱에서 **구독 추가**를 누르고 그 이름을 입력합니다.
4. 저장소 **Settings → Secrets and variables → Actions → New repository secret**에서 이름 `NTFY_TOPIC`, 값에 위 알림 주소 이름을 넣습니다.
5. 저장소 **Actions** 탭에서 `30분 퀴즈 알림`을 열고 **Run workflow**를 눌러 한 번 시험합니다. 아이폰에 알림이 오면 성공입니다.
6. 알림을 누르면 앱이 열리면서 해당 문제가 바로 나옵니다.

시간대 변경: `.github/workflows/quiz.yml`의 `cron`은 UTC 기준입니다. 기본값 `*/30 0-14 * * *`은 한국시간 09:00~23:30입니다. 한국시간에서 9시간을 빼서 계산하세요.

알아 둘 점
- GitHub 스케줄은 몇 분 늦거나 드물게 건너뛸 수 있습니다.
- 공개 저장소는 60일간 저장소 활동이 없으면 스케줄이 자동으로 꺼집니다. 문장을 추가하는 커밋이 이를 막아 줍니다. 꺼졌다면 Actions 탭에서 다시 켜세요.
- iOS에서 ntfy 알림이 도착하는 안정성은 iOS 버전과 설정에 따라 다를 수 있으니, 처음 하루는 시험 삼아 확인해 보세요.

## 3. 문장 추가하기

`sentences.json`의 `sentences` 배열 끝에 항목을 추가합니다. 필수는 `id`, `text`, `translation`, `summary`이고, 나머지는 있으면 화면에 나옵니다. 형식은 이미 들어 있는 문장을 참고하세요.

- 퀴즈 `type`: `cloze`(빈칸), `ko2en`(한→영), `meaning`(뜻 맞히기, `choices` 필요), `linking`(연음)
- `quiz`를 비워 두면 알림 스크립트가 원문에서 빈칸 문제를 자동으로 만듭니다.
- 올리면 Actions가 알림 전에 `scripts/validate.py`로 자동 검사합니다.
- 반영까지는 GitHub Pages 배포에 1~2분이 걸립니다. 앱을 새로 열면 최신 내용을 불러옵니다.

## 참고

- 복습 기록(알았어요/헷갈려요)은 각 기기의 브라우저에 저장됩니다. 기기를 바꾸거나 사파리 데이터를 지우면 초기화됩니다.
- 한글 발음 표기는 소리의 윤곽을 잡는 용도이며 실제 음원과 다를 수 있습니다. 직접 들은 음원을 우선하세요.
- 듣기 버튼은 기기의 기본 음성 합성이라 배우의 실제 발화와 다릅니다.
