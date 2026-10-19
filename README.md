# 유지훈의 공부 위키

읽은 논문과 공부한 개념을 그림과 함께 정리하는 위키입니다. 주소는 https://youjhun.github.io 입니다.

[Quartz 4](https://quartz.jzhao.xyz)로 만들고, `main`에 푸시하면 GitHub Actions가 빌드해서 GitHub Pages에 올립니다.

## 구조

```
content/
  index.md            첫 화면
  concepts/           개념 글 (한 편에 개념 하나)
  papers/             논문 리뷰
  images/<글 이름>/   글에 들어가는 그림
  templates/          새 글 틀 (사이트에는 나가지 않음)
scripts/figures/      그림을 만드는 파이썬 스크립트 (글 하나에 파일 하나)
```

## 새 글 쓰기

1. `content/templates/concept.md`를 복사해 `content/concepts/<영문-이름>.md`로 둡니다. 파일 이름이 주소가 됩니다.
2. 그림은 `content/images/<영문-이름>/`에 넣고 `![설명](../images/<영문-이름>/그림.png)`로 붙입니다. 바로 아래 줄에 `*그림 1. …*`로 설명을 답니다.
3. 다른 글은 `[[파일-이름|보이는 이름]]`으로 잇습니다.

글은 같은 순서로 씁니다. 한눈에 요약, 정의, 그림과 예시, 수식, 자주 하는 오해, 관련 개념, 참고 자료 순입니다. 논문 리뷰에서는 논문이 말한 것과 읽으며 든 생각을 다른 절로 나눕니다.

**올리지 않는 것**: 이해도 기록, 학습 세션 원문, 다른 사람의 개인 정보, 저작권이 있는 논문 그림. 논문 그림이 필요하면 직접 다시 그립니다.

## 그림 다시 만들기

```bash
sudo apt-get install fonts-nanum   # 한글 라벨용 글꼴
pip install matplotlib numpy
cd scripts/figures
python3 sampling_aliasing.py       # content/images/sampling-aliasing/ 에 PNG를 씁니다
```

모든 그림은 `style.py`의 글꼴과 색을 같이 씁니다. 다크 모드에서도 보이도록 흰 배경으로 저장합니다.

## 로컬에서 보기

```bash
npm ci
npx quartz build --serve   # http://localhost:8080
```

## 처음 한 번만: GitHub Pages 켜기

저장소 **Settings → Pages → Build and deployment → Source**를 **GitHub Actions**로 바꿉니다.

## 라이선스

사이트 엔진(Quartz)은 MIT 라이선스입니다(`LICENSE.txt`). 글과 그림의 저작권은 유지훈에게 있습니다.
