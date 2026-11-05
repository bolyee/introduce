# 이현중 포트폴리오

빌드된 정적 사이트는 `site/`에 있습니다. 외부 라이브러리, 웹폰트, 서버 또는 설치가 필요하지 않습니다. 방문자 페이지에는 내부 편집 메모와 원본 CV가 포함되지 않습니다.

## 바로 미리보기

`site/index.html`을 브라우저에서 열면 상세 설명까지 사용할 수 있습니다.

로컬 HTTP 미리보기가 필요하면 작업 공간 루트(`CV/`)에서:

```sh
python3 -m http.server 8765 --bind 127.0.0.1 --directory Website/site
```

브라우저에서 `http://127.0.0.1:8765`를 엽니다. 종료는 Ctrl+C입니다. Codex 실행 환경에서는 로컬 포트 열기가 차단될 수 있지만 파일로 직접 여는 미리보기를 사용할 수 있습니다.

## 수정

현재 웹페이지 내용은 `../01_CV_Music/cv.tex`를 기준으로 갱신했습니다. AutoMix 프로젝트에 사용자 제공 YouTube 시연 영상 링크를 표시하며, 프로젝트 링크는 상세 설명을 펼치지 않아도 볼 수 있습니다. CV 변경은 자동 동기화되지 않습니다.

- 소개, 관심 주제, 프로젝트, 음악, 경력, 학력: `content.json`
- 사진 경로와 소개문: `content.json`의 `portrait`, `about`
- 증명사진: `site/assets/profile.jpeg` (제공한 원본을 그대로 사용)
- 페이지 구조: `build.py`
- 디자인·모바일 레이아웃: `site/style.css`
- 별도 편집 메모: `private/EDITOR_NOTES.md`

수정 후 `python3 Website/build.py`를 실행하면 HTML이 갱신됩니다. Python은 편집 시에만 필요하며 배포에는 필요하지 않습니다. 빌드는 기존 CSS와 PDF를 보존합니다.

프로젝트의 `links`에는 실제 공개 URL만 추가합니다:

```json
{"label": "프로젝트 코드", "url": "실제 https URL"}
```

음원·공연 자료는 `musicWorks`, 자동 믹싱 비교는 첫 프로젝트의 `demo`에 추가합니다. 공개 허가된 파일만 `site/assets/`에 복사하고 아래 형식을 사용합니다. 예시는 자료 구조이며 실제 파일/URL로 채워야 합니다.

```json
{
  "title": "실제 곡명 또는 입력 / 레퍼런스 / 처리 결과",
  "approved": true,
  "cover": "assets/실제-커버.webp",
  "audio": "assets/실제-음원.mp3",
  "links": [{"label": "발매 페이지 또는 공연 영상", "url": "실제 https URL"}]
}
```

`cover`, `audio`, `links`는 필요한 필드만 남깁니다. `approved`가 true가 아니면 표시하지 않습니다. 미디어가 없으면 빈 플레이어나 가짜 버튼을 생성하지 않습니다. 오디오는 브라우저 기본 컨트롤을 사용하고 자동 재생하지 않습니다. 자동 믹싱 비교는 입력·레퍼런스·결과 순서로 세 항목을 추가하세요.

## CV

CV는 이메일에 별도 첨부하므로 웹사이트의 보기·다운로드 링크와 배포용 PDF를 제거했습니다. 원본 CV와 `private/`의 공개용 사본은 보존되어 있습니다.

## GitHub Pages 배포

**`site/` 안의 파일만** 배포용 저장소 루트에 복사합니다. 원본 CV, `private/`, 작업 폴더 전체는 업로드하지 않습니다.

1. 배포용 GitHub 저장소를 만들고 `index.html`, `style.css`, `.nojekyll`, `assets/`를 루트에 업로드합니다.
2. 저장소 Settings → Pages에서 해당 브랜치의 루트 디렉터리를 배포 대상으로 선택합니다.
3. GitHub가 표시하는 배포 URL에서 프로젝트 펼침과 모바일 화면을 최종 확인합니다.

상대 경로를 사용하므로 `bolyee.github.io/저장소명/` 형태에서도 동작합니다. 기존 `site/.git`에는 원격 저장소 `https://github.com/bolyee/curriculum_vitae.git`와 `main` 브랜치 설정이 있습니다. 폴더 정리 시 이를 그대로 보존했습니다. 실제 원격 Pages 설정 및 공개 상태는 이번 로컬 정리에서 확인하거나 변경하지 않았습니다.

## 검증

`python3 Website/scripts/check-static.py`는 정적 링크, 파일 경로, 문서 구조, 가짜 링크, 자동재생 금지, 색상 대비를 확인합니다. 브라우저 검사 스크립트 `scripts/check-browser.cjs`는 현재 컴퓨터의 Chrome과 설치된 Puppeteer 경로를 사용합니다. 다른 환경에서는 해당 경로를 조정해야 합니다.

2026-11-05 검증 결과: 정적 검사 및 Chrome 브라우저 검사를 통과했습니다. 1440·768·390·320px 화면에서 가로 넘침, 상세 설명의 키보드 조작, 본문 바로가기, 빈 오디오 플레이어와 JavaScript 오류 여부를 확인했습니다.

이전 환경의 확인 기록: 정적 구조·내부 링크·파일 연결 및 주요 글자색의 WCAG AA 대비(최저 6.29:1)를 확인했습니다. 현재 실행 환경에서 로컬 포트 바인딩과 Chrome 실행이 차단되어 실제 브라우저의 키보드 동작과 모바일 시각 검증은 미완료입니다. 기본 HTML `details/summary`, 포커스 표시, 본문 바로가기, 320px까지의 반응형 CSS를 구현했으며 발송 전에 브라우저에서 직접 확인해야 합니다.

## 폴더 분리 후 관리 기준

기존 `curriculum_vitae_2/portfolio/` 전체를 이 폴더로 이동했습니다. 위 빌드·검증·HTTP 미리보기 명령은 작업 공간 루트(`CV/`)에서 실행합니다. 이 폴더 안에서는 각각 `python3 build.py`, `python3 scripts/check-static.py`를 실행할 수 있습니다.

- `content.json`은 웹페이지의 독립적인 콘텐츠 원본이며 두 CV를 자동으로 읽거나 동기화하지 않습니다.
- `build.py`는 자신의 위치를 기준으로 JSON을 읽고 `site/index.html`을 생성합니다. HTML을 직접 편집하면 다음 빌드에서 덮어써지므로 구조 변경은 `build.py`에서 합니다.
- `site/style.css`, `site/assets/` 및 `.nojekyll`은 기존 디자인·리소스·배포 파일입니다. CSS는 빌드가 생성하지 않는 직접 편집 대상입니다.
- `private/cv-public.tex`와 PDF는 기존 2번 CV에서 파생한 별도 공개용 사본입니다. 현재 사이트에는 CV 다운로드 링크가 없고 두 지원용 CV와 자동 연동하지 않습니다.
- 폴더 루트의 증명사진 원본과 `portfolio-site.zip`은 보관 자료입니다. ZIP은 현재 사이트와 동일하다고 가정하지 않으며 빌드 시 자동 갱신되지 않습니다.
- 배포 저장소 루트는 이제 `Website/site/`입니다. `.git`과 기존 변경 상태를 그대로 이동했으며 커밋·푸시·외부 배포는 실행하지 않았습니다. 저장소 루트 기준 파일 구조는 동일합니다.
