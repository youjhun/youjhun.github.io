---
title: 기댓값·분산·공분산
aliases: [expectation, variance, covariance]
tags: [확률, 통계, 18.05]
date: 2026-10-20
description: 분포의 중심과 퍼짐, 두 변수의 함께 변하는 정도를 하나의 계산 흐름으로 정리한다.
---

> [!abstract] 한눈에
> 기댓값은 분포의 무게중심, 분산은 평균에서 떨어진 제곱거리의 평균, 공분산은 두 변수가 평균에서 같은 방향으로 움직이는지를 나타낸다. 모두 표본에서 계산한 값과 모집단의 양을 구분해야 한다.

## 기댓값

이산 확률변수는

$$
E[X]=\sum_x xP(X=x)
$$

이고, 연속 확률변수는

$$
E[X]=\int_{-\infty}^{\infty}x f_X(x)\,dx
$$

다. 기댓값은 한 번 관측했을 때 가장 자주 나오는 값과 같을 필요가 없다. 여러 번 반복한 평균이 가까워지는 중심이다.

기댓값은 선형이다.

$$
E[aX+bY+c]=aE[X]+bE[Y]+c
$$

여기에는 $X,Y$의 독립성이 필요하지 않다.

## 분산과 표준편차

$$
\operatorname{Var}(X)=E[(X-E[X])^2]=E[X^2]-E[X]^2
$$

분산은 원래 단위의 제곱이므로, 해석할 때는 같은 단위로 돌아오는 표준편차 $\sigma_X=\sqrt{\operatorname{Var}(X)}$가 편하다. 상수를 더해도 퍼짐은 바뀌지 않고, $a$배 하면 분산은 $a^2$배가 된다.

$$
\operatorname{Var}(aX+b)=a^2\operatorname{Var}(X)
$$

## 공분산과 상관

$$
\operatorname{Cov}(X,Y)=E[(X-E[X])(Y-E[Y])]
$$

두 변수가 평균보다 함께 크거나 함께 작으면 양수, 반대 방향으로 움직이면 음수가 되기 쉽다. 단위에 영향을 받지 않도록 정규화하면 피어슨 상관계수가 된다.

$$
\rho_{XY}=\frac{\operatorname{Cov}(X,Y)}{\sigma_X\sigma_Y}
$$

독립이면 공분산은 0이지만, 공분산이 0이라고 일반적으로 독립인 것은 아니다. 공분산 0은 선형 관계가 없다는 것에 가깝고, 비선형 의존은 남을 수 있다.

## 합의 분산

$$
\operatorname{Var}(X+Y)=\operatorname{Var}(X)+\operatorname{Var}(Y)+2\operatorname{Cov}(X,Y)
$$

독립이면 공분산 항이 0이 된다. 센서 여러 개를 평균낼 때 잡음이 서로 독립이라는 가정 아래 분산이 줄어드는 이유다. 공통 전원 잡음이나 움직임 아티팩트처럼 상관된 잡음이 있으면 기대만큼 줄지 않는다.

여러 변수를 모으면 공분산은 [[covariance-matrix|공분산 행렬]]이 되고, 그 고유방향을 찾는 과정이 [[pca-svd|PCA]]로 이어진다.

## 유의점

- 기댓값이 실제로 관측 가능한 값일 필요는 없다. 주사위 평균 3.5처럼 표본공간 밖일 수 있다.
- 표준편차와 표준오차는 구분해야 한다. 표준편차는 데이터의 퍼짐, 표준오차는 추정량의 불확실성이다.
- 상관을 인과로 읽으면 안 된다. 공통 원인, 선택 편향, 시간 추세가 상관을 만들 수 있다.

## 출처

- MIT OpenCourseWare, [18.05 Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/), Unit 2
- 개인 학습 기록, Notion `Studies / LAIDD / Probability and Statistics`
