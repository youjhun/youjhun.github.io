---
title: 단순 선형 회귀
aliases: [least squares regression]
tags: [통계, 회귀, 최소제곱]
date: 2026-10-20
description: 직선을 맞추는 계산과 확률모형을 구분하고, 기울기·잔차·R²를 해석한다.
---

> [!abstract] 한눈에
> 선형 회귀는 $x$로부터 $y$의 평균을 직선으로 설명한다. 최소제곱은 직선을 고르는 계산 규칙이고, 통계적 추론은 그 뒤에 오차 모형을 추가했을 때 가능하다.

## 모형과 적합

단순 선형 회귀 모형은

$$
y_i=\beta_0+\beta_1x_i+\epsilon_i
$$

이다. 최소제곱 추정량은 잔차제곱합

$$
RSS=\sum_i(y_i-\hat y_i)^2
$$

을 가장 작게 만드는 $\hat\beta_0,\hat\beta_1$이다.

$$
\hat\beta_1=\frac{\sum_i(x_i-\bar x)(y_i-\bar y)}{\sum_i(x_i-\bar x)^2},\qquad
\hat\beta_0=\bar y-\hat\beta_1\bar x
$$

따라서 적합 직선은 항상 $(\bar x,\bar y)$를 지난다. 기울기는 $x$가 한 단위 커질 때 조건부 평균 $E[Y\mid X=x]$가 얼마나 변하는지를 나타낸다.

## $R^2$의 해석

$$
R^2=1-\frac{RSS}{TSS},\qquad TSS=\sum_i(y_i-\bar y)^2
$$

$R^2$는 평균만 예측하는 기준선과 비교해 선형모형이 표본의 $y$ 변동을 얼마나 설명했는지 나타낸다. 인과관계, 외삽 정확도, 모형이 옳다는 사실을 보장하지 않는다.

## 잔차 진단

잔차 $e_i=y_i-\hat y_i$에는 모형이 놓친 구조가 남는다.

- 곡선 모양이 남으면 선형성이 맞지 않는다.
- $x$가 커질수록 퍼짐이 커지면 등분산 가정이 깨진다.
- 시간 순서로 패턴이 남으면 오차가 독립이 아닐 수 있다.
- 한 점이 적합선을 크게 당기면 영향점인지 확인해야 한다.

## 계산과 추론

최소제곱 직선은 어떤 데이터에도 계산할 수 있다. 그러나 계수의 표준오차, t-검정, 예측구간을 쓰려면 오차의 평균이 0이고 관측이 독립이며 분산 구조가 적절하다는 가정이 더 필요하다.

## 유의점

- 상관이나 기울기가 커도 $x$가 $y$를 원인적으로 바꾼다고 할 수는 없다.
- 훈련 데이터의 $R^2$가 높아도 새 데이터 예측이 좋다는 보장은 없다.
- $x$의 관측 범위 밖으로 직선을 길게 연장하는 외삽은 위험하다.
- 예측 평균의 신뢰구간보다 새 관측값의 예측구간이 더 넓다. 새 관측에는 개별 오차까지 들어가기 때문이다.

## 관련 개념

- [[least-squares|최소제곱과 정사영]]: 회귀를 선형대수의 투영 문제로 본다.
- [[confidence-interval-hypothesis-test|신뢰구간과 가설검정]]: 회귀계수의 불확실성을 해석한다.

## 참고 자료

- MIT OpenCourseWare, [18.05 Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/)
