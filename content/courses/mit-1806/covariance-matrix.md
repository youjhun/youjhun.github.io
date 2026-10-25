---
title: 공분산 행렬
aliases: [공분산 행렬, 공분산, 상관 행렬, 공간 공분산]
tags: [선형대수, 통계, 18.06, EEG]
date: 2026-10-19
description: 여러 변수가 함께 흔들리는 방식을 한 행렬에 담은 것. 대각선은 분산, 나머지는 공분산이고, 고유벡터는 자료가 퍼진 방향이다.
---

> [!abstract] 한눈에
> 변수가 $d$개인 자료의 공분산 행렬 $\Sigma$는 $d \times d$ 행렬이다. 대각선에는 각 변수의 분산이, 대각선 밖 $(i, j)$ 칸에는 변수 $i$와 $j$가 함께 움직이는 정도(공분산)가 들어간다. 항상 대칭이고 양의 준정부호여서 고유벡터끼리 직교하고 고유값은 0 이상이다. 고유벡터는 자료가 퍼진 방향이고 고유값은 그 방향의 분산이다.

## 정의

평균이 $\boldsymbol\mu$인 확률벡터 $\mathbf{x}$의 공분산 행렬은 아래 식으로 정의한다.

$$
\Sigma = E\!\left[(\mathbf{x} - \boldsymbol\mu)(\mathbf{x} - \boldsymbol\mu)^\top\right],
\qquad \Sigma_{ij} = \operatorname{Cov}(x_i, x_j)
$$

자료에서 추정할 때는 관측값 $n$개를 행으로 쌓아 행렬 $X$($n \times d$)를 만들고 각 열의 평균을 뺀 $X_c$로 계산한다.

$$
S = \frac{1}{n-1} X_c^\top X_c
$$

평균도 자료에서 추정하느라 자유도를 하나 썼으므로 $n$ 대신 $n-1$로 나눈다.

![공분산 행렬과 자료 모양](../../images/covariance-matrix/shapes.png)
_그림 1. 점 개수는 같고 공분산 행렬만 다르다. 빨간 타원은 2σ 등고선이다. 대각선 밖 값의 부호에 따라 타원이 기우는 방향이 달라진다._

## 성질

- 대칭이다. $\operatorname{Cov}(x_i, x_j) = \operatorname{Cov}(x_j, x_i)$이므로 $\Sigma^\top = \Sigma$.
- 양의 준정부호다. 자료를 어느 방향 $\mathbf{w}$로 투영하든 분산은 음수가 될 수 없다.

$$
\operatorname{Var}(\mathbf{w}^\top \mathbf{x}) = \mathbf{w}^\top \Sigma\, \mathbf{w} \ge 0
$$

- 두 성질에서 고유분해의 모양이 정해진다. 대칭 행렬이므로 서로 직교하는 고유벡터들로 $\Sigma = Q \Lambda Q^\top$로 분해되며 양의 준정부호라서 고유값이 모두 0 이상이다.

고유벡터 $\mathbf{q}_i$ 방향으로 투영한 분산은 $\mathbf{q}_i^\top \Sigma\, \mathbf{q}_i = \lambda_i$다. 따라서 고유벡터는 자료 타원의 축 방향, 고유값은 그 축 방향의 분산이다(그림 2). 고유값이 가장 큰 고유벡터가 분산이 가장 큰 방향이고 이 방향이 [[pca-svd|PCA]]의 첫 주성분이다.

![공분산 행렬의 고유벡터와 고유값](../../images/covariance-matrix/eigen.png)
_그림 2. 각 화살표는 고유벡터에 표준편차($\sqrt{\lambda}$)를 곱한 벡터다. 자료가 가장 넓게 퍼진 쪽이 긴 화살표 방향이다._

## 상관 행렬

공분산 값은 변수의 단위에 따라 달라지기 때문에 밀리볼트로 잰 채널과 마이크로볼트로 잰 채널을 그대로 비교할 수 없다. 각 공분산을 두 변수의 표준편차로 나누면 단위가 없는 **상관 행렬**을 얻는다. 대각선 값은 모두 1, 나머지 칸은 [[pearson-spearman|피어슨 상관계수]]다.

$$
R_{ij} = \frac{\Sigma_{ij}}{\sqrt{\Sigma_{ii}\,\Sigma_{jj}}}
$$

## 여러 채널 신호의 공간 공분산

뇌파처럼 채널 $C$개에서 $T$표본씩 잰 신호는 $C \times T$ 행렬 $X$로 나타낸다. 채널마다 평균을 빼고 $XX^\top/(T-1)$을 구하면 $C \times C$ **공간 공분산 행렬**이 된다. 어느 채널끼리 함께 흔들리는지가 이 행렬에 들어 있어서 [[csp|CSP]] 같은 공간 필터와 리만 기하 기반 분류기 모두 이 행렬에서 출발한다.

![여러 채널 신호의 상관 행렬](../../images/covariance-matrix/channels.png)
_그림 3. 합성한 4채널 신호다. 1·2번 채널은 주로 10 Hz 성분을, 3·4번 채널은 주로 느린 변동을 공유하게 섞었고 상관 행렬에서도 두 묶음이 보인다._

## 유의점

- 공분산 크기는 단위와 분산에 좌우되므로 공분산이 크다고 관계가 강하다고 볼 수 없다. 관계의 강도는 상관으로 비교해야 한다.
- 공분산이 0이어도 두 변수가 독립이라고 할 수 없다. 공분산은 두 변수가 선형으로 함께 움직이는 정도만 잰다. U자 같은 비선형 관계에서는 두 변수가 강하게 얽혀 있어도 공분산이 0으로 나올 수 있다.
- 표본 공분산 행렬은 역행렬이 없을 수 있다. 표본 수가 변수 수보다 적으면($n \le d$) 계수(rank)가 부족해 역행렬이 없다. 채널은 많고 시행은 적은 뇌파 자료에서 자주 겪는 일이다. 이럴 때는 대각선에 작은 값을 더하는 축소(shrinkage) 추정으로 보완한다.
- $n$으로 나눈 값과 $n-1$로 나눈 값은 표본이 작을 때 차이가 드러난다. 분산 추정이 평균적으로 치우치지 않으려면 $n-1$로 나눠야 한다.

## 관련 개념

- [[pca-svd|PCA와 SVD]]: 공분산 행렬의 고유분해로 차원을 줄이는 방법
- [[pearson-spearman|피어슨과 스피어먼 상관]]: 상관 행렬 각 칸의 값
- [[csp|CSP (공통 공간 패턴)]]: 두 조건의 공분산 행렬을 동시에 대각화하는 공간 필터

## 참고 자료

- 강완모, 「데이터과학을 위한 선형대수학」(Linear Algebra for Data Science), KAIST, Version 1.2 (2023), _Covariance Matrices_ 절(161쪽~)
- MIT OCW, [18.06 Linear Algebra (Spring 2010)](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/), Lecture 25 _Symmetric matrices and positive definiteness_
- MIT OCW, [18.05 Introduction to Probability and Statistics (Spring 2022)](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/), 공분산과 상관 단원
