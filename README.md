# Jihun Yu's Engineering Note

공부한 과목, 직접 설계한 과목, 프로젝트, 읽은 논문을 그림과 함께 정리하는 노트입니다. 주소는 https://youjhun.github.io 입니다.

[Quartz 4](https://quartz.jzhao.xyz)로 만들고, `main`에 푸시하면 GitHub Actions가 빌드해서 GitHub Pages에 올립니다.

## 구조

```
content/
  index.md              첫 화면
  courses/<과목>/       대학 강의 (MIT OCW 등). index.md가 단원표, 나머지가 개념 글
  my-courses/<과목>/    직접 설계한 과목
  projects/             프로젝트와, 프로젝트에서 배운 개념
  papers/               논문 리뷰
  images/<글 이름>/     글에 들어가는 그림
  templates/            새 글 틀 (사이트에는 나가지 않음)
scripts/figures/        그림을 만드는 파이썬 스크립트
scripts/check_aliases.py  별칭과 파일 이름이 겹치는지 검사 (배포 전에 자동으로 돈다)
quartz/static/fonts/pretendard/  Pretendard 글꼴 (SIL OFL 1.1, LICENSE.txt 동봉)
```

## 새 글 쓰기

1. `content/templates/concept.md`를 복사해 알맞은 폴더에 `<영문-이름>.md`로 둡니다. 파일 이름이 주소가 됩니다.
2. 그림은 `content/images/<영문-이름>/`에 넣고 글의 깊이에 맞는 상대 경로로 붙입니다. `courses/<과목>/`처럼 두 단계 아래면 `../../images/…`, `papers/`처럼 한 단계면 `../images/…`입니다. 바로 아래 줄에 `*그림 1. …*`로 설명을 답니다.
3. 다른 글은 `[[파일-이름|보이는 이름]]`으로 잇습니다. 표 안에서는 `|`를 `\|`로 씁니다.
4. `aliases`에는 파일 이름과 같은 값(대소문자만 다른 것 포함)을 넣지 않습니다. 넣으면 링크가 리디렉트 페이지로 빠집니다. `python3 scripts/check_aliases.py`로 확인할 수 있습니다.

글은 같은 순서로 씁니다. 한눈에 요약, 정의, 그림과 예시, 수식, 자주 하는 오해, 관련 개념, 참고 자료 순입니다. 논문 리뷰에서는 논문이 말한 것과 읽으며 든 생각을 다른 절로 나눕니다.

**올리지 않는 것**: 이해도 기록, 학습 세션 원문, 개인 일정과 계획, 다른 사람의 개인 정보, 저작권이 있는 논문 그림. 논문 그림이 필요하면 직접 다시 그립니다.

## 그림 다시 만들기

```bash
pip install matplotlib numpy
# 글꼴: Pretendard OTF(npm 패키지 pretendard의 dist/public/static)를 시스템에 설치합니다.
# 없으면 나눔고딕(apt-get install fonts-nanum), 그다음 DejaVu Sans로 넘어갑니다.
cd scripts/figures
python3 dft_fft.py        # content/images/dft-fft/ 에 PNG를 씁니다
```

모든 그림은 `style.py`의 글꼴과 색을 같이 씁니다. 다크 모드에서도 보이도록 흰 배경으로 저장합니다.

## 로컬에서 보기

```bash
npm ci
npx quartz build --serve   # http://localhost:8080
```

## 라이선스

사이트 엔진(Quartz)은 MIT 라이선스입니다(`LICENSE.txt`). Pretendard 글꼴은 SIL Open Font License 1.1입니다. 글과 그림의 저작권은 유지훈에게 있습니다.
