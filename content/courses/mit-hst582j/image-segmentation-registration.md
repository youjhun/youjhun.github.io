---
title: 영상 분할·형태학·정합
description: 영상의 좌표·라벨·변환과 최적화 목적, Dice와 정합 오차의 차이를 설명한다.
date: 2026-10-25
---

> [!abstract] 한눈에
> 분할은 각 위치의 조직·구조 라벨을 구하고 정합은 두 영상의 대응 좌표 변환을 구한다. 픽셀 인덱스와 물리 좌표, intensity와 label을 구별해야 결과를 해석할 수 있다. 모달리티는 영상 신호가 어떤 물리량에서 나오는지를 정한다.

## 영상 좌표와 공간 필터

영상 I[i,j,k]의 voxel spacing이 (sₓ,sᵧ,s_z)이면 한 voxel 부피는 그 곱이다. 새 예 0.5×0.5×2 mm voxel 100개는 50 mm³다. 방향 행렬과 원점까지 있어야 인덱스를 환자 또는 장치의 물리 좌표로 보낼 수 있다. 배열의 축 순서만 보고 좌우를 결정하지 않는다.

2D 컨볼루션은 $J[i,j]=\sum_{u,v}h[u,v]I[i-u,j-v]$다. Gaussian 평활은 잡음을 줄이는 대신 경계를 흐리게 하고, 미분 필터는 경계뿐 아니라 고주파 잡음도 키울 수 있다. 경계 padding 규칙도 결과에 포함된다. 이방성 voxel에서 각 축에 같은 voxel 수의 커널을 쓰면 물리 길이는 서로 다르다.

## 강도 기반 분할

단일 문턱으로 $I>\tau$인 voxel을 선택하는 방법은 간단하지만 조직의 강도 중첩·부분용적·bias field에 제한된다. 확률 모형에서는 $P(c\mid I)\propto p(I\mid c)P(c)$로 클래스 c를 선택한다. Spatial prior를 넣으면 이웃 라벨과의 관계까지 반영한다. 이미지 강도를 잘 설명하는 모형이 해부학적 라벨을 정확히 복원한다고 단정하지 않는다.

## 형태학 연산

이진 집합 A와 구조요소 B에 대해 dilation은 집합을 확장하고 erosion은 구조요소가 포함되는 위치만 남긴다. Opening은 erosion 후 dilation, closing은 dilation 후 erosion이다. 같은 이름의 필터라도 구조요소 모양·크기·차원에 따라 결과가 다르다. 연결성의 4/8 또는 6/18/26 이웃 규약을 정하지 않으면 성분 개수와 구멍 판정이 달라질 수 있다.

## 분할 평가

예측 집합 A와 기준 B에 대해

$$
Dice=\frac{2|A\cap B|}{|A|+|B|},\quad
IoU=\frac{|A\cap B|}{|A\cup B|},\quad
Dice=\frac{2IoU}{1+IoU}.
$$

새 예 |A|=80, |B|=100, 교집합=60이면 Dice=120/180=2/3, IoU=60/120=0.5다. 둘 다 빈 집합일 때의 점수는 별도 규약이 필요하다. 큰 장기의 겹침 점수는 작은 경계 오차에 둔감할 수 있어 표면 거리와 구조별 성능을 함께 본다.

## 정합의 네 구성

Fixed 영상 F와 moving 영상 M을 두고 $M(T(x))$가 F(x)에 맞도록 정의하면

$$
\widehat T=\arg\min_T\sum_x d(F(x),M(T(x)))+\lambda\mathcal R(T).
$$

T가 fixed 좌표에서 moving 좌표로 가는 pull 변환임을 먼저 정했다. 반대 방향의 변환을 제공받으면 역변환이 필요하다. 정합에는 변환 모형, 유사도, 보간, 최적화와 규제가 포함된다.

Rigid는 회전·평행이동, affine은 배율·shear까지, deformable은 위치별 변형까지 허용한다. 자유도가 크면 맞출 수 있는 범위와 과적합·비물리적 변형 가능성이 함께 커진다. 같은 모달리티의 밝기 차에 SSD를 사용할 수 있지만 다른 모달리티에는 강도가 일대일로 같다는 가정이 맞지 않을 수 있다. Mutual information 같은 통계적 기준도 정합 품질을 자동 보장하지 않는다.

## 보간과 검산

연속 강도는 선형·고차 보간을, 범주 라벨은 보통 nearest-neighbor 등 라벨 규약을 보존하는 방법을 선택한다. 라벨 ID 1과 3 사이를 선형 보간한 2는 새로운 조직을 뜻하지 않는다. 재표본화는 새 격자에 값을 계산하는 것이며 획득하지 않은 세부정보를 복원하지 않는다.

새 2D 예에서 moving의 landmark (12,7)이 fixed의 (10,10)에 대응하면 위 pull 변환의 평행이동은 T(x,y)=(x+2,y−3)다. T(10,10)=(12,7)로 방향을 검산한다. 실제 품질은 최적화에 쓰지 않은 landmark의 물리 거리, overlay, 구조 보존과 Jacobian 등을 함께 확인한다.

## 모달리티와 영상 해석

X선·CT는 감쇠, 초음파는 음향 전파와 산란, MRI는 자화와 이완·시퀀스에 의존한다. 강도의 의미와 해상도·잡음 구조가 다르므로 한 영상의 threshold를 다른 모달리티에 그대로 옮기지 않는다. 물리적 형성 과정은 [[medical-imaging-physics|의료영상 물리]]에 연결한다. 후처리의 높은 점수와 원영상의 물리적 정량성은 별도로 평가한다.

## 유의점

- spacing·origin·direction과 transform 방향을 결과와 함께 보존한다.
- 훈련·튜닝·평가에 같은 환자의 인접 영상을 무심코 나누지 않는다.
- Dice와 정합 landmark 오차는 서로 다른 질문에 답한다.

## 관련 개념

- [[medical-imaging-physics|의료영상의 물리적 신호]]
- [[digital-filters-convolution|컨볼루션]]
- [[bayes-classifier-detection|확률적 분류]]

## 참고 자료

- [William Wells, HST.582J: Medical Image Segmentation](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007/resources/l15_seg/), intensity 분류·사전모형·형태학.
- [HST.582J Lecture Notes](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007/pages/lecture-notes/), Image Processing, Registration I–II, Imaging Modalities. 좌표·평가 예는 별도로 계산했다.
