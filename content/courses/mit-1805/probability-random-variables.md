---
title: 확률공간과 확률변수
aliases: [확률변수, probability space, random variable]
tags: [확률, 통계, 18.05]
date: 2026-10-20
description: 표본공간, 사건, 확률측도와 확률변수를 구분하고 이산·연속 분포를 같은 틀로 읽는다.
---

> [!abstract] 한눈에
> 확률모형은 가능한 결과의 집합 $\Omega$, 질문할 수 있는 사건의 모음 $\mathcal F$, 사건에 수를 붙이는 확률 $P$로 이루어진다. 확률변수 $X$는 무작위인 ‘수’가 아니라 결과 $\omega$를 수 $X(\omega)$로 바꾸는 함수다.

## 확률공간의 구성

확률공간은 $(\Omega,\mathcal F,P)$로 쓴다.

- **표본공간 $\Omega$**: 가능한 결과 전체
- **사건공간 $\mathcal F$**: 확률을 물을 수 있는 결과의 집합들
- **확률측도 $P$**: 각 사건에 0과 1 사이의 값을 붙이는 규칙

주사위라면 $\Omega=\{1,2,3,4,5,6\}$이고, ‘짝수가 나온다’는 사건은 $\{2,4,6\}$이다. $P$는 결과 자체가 아니라 사건에 붙는다.

빈도주의에서는 확률을 반복 시행의 장기 비율로 읽고, 베이지안 관점에서는 정보가 불완전한 상태의 믿음 정도까지 확률로 표현한다. 계산 규칙은 공유하지만 무엇을 확률로 놓는지의 해석이 다르다. 관측 뒤 믿음을 갱신하는 방법은 [[bayes-update|베이즈 갱신]]에 이어진다.

## 확률변수와 분포

$$
X:\Omega\rightarrow\mathbb R
$$

두 개의 동전을 던진 결과가 $\Omega=\{HH,HT,TH,TT\}$일 때 $X$를 앞면의 개수로 정의하면 $X(HH)=2$, $X(HT)=1$이다. 서로 다른 결과가 같은 숫자로 모일 수 있다. 분포는 이 함수가 표본공간의 확률을 수직선으로 옮긴 결과다.

누적분포함수는 이산과 연속을 모두 다룬다.

$$
F_X(x)=P(X\le x)
$$

이산 확률변수는 점확률 $p_X(x)=P(X=x)$를 합하고, 연속 확률변수는 밀도 $f_X(x)$를 적분한다.

$$
P(a<X\le b)=F_X(b)-F_X(a)=\int_a^b f_X(x)\,dx
$$

연속형에서는 한 점의 확률이 0이어도 밀도값은 0이 아닐 수 있다. 밀도는 ‘단위 $x$당 확률’이며 확률 자체와 다르다.

## 모델링 순서

1. 실험의 가능한 결과를 정한다.
2. 관심 있는 양을 확률변수로 정의한다.
3. 분포의 모수와 가정을 적는다.
4. 관측할 통계량을 정한다.
5. 현실에서 가정이 깨지는 방식을 확인한다.

생체신호에서는 같은 사람의 연속 구간을 독립 표본으로 취급하기 쉽다. 확률변수를 정의했다고 독립성이 자동으로 생기지는 않는다. 세션, 사람, 시간 의존성을 표본공간과 생성 과정에 포함해야 한다.

## 출처

- 개인 학습 기록, Notion `Studies / LAIDD / Probability and Statistics`, Random Variables and Probability
- MIT OpenCourseWare, [18.05 Introduction to Probability and Statistics](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/)
