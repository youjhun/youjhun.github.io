---
title: 가능도·최대가능도·베이지안 추정
description: 관측을 고정한 가능도에서 MLE를 구하고 사전분포와 결합해 사후분포를 계산한다.
date: 2026-10-25
---

> [!abstract] 한눈에
> 가능도는 관측한 데이터에 대한 모수별 상대적 적합도를 나타낸다. MLE는 이를 최대화하고, 베이지안 추정은 사전분포를 곱해 모수의 사후분포를 만든다. 관측의 독립성·누락·선택 과정은 두 계산 모두의 가정이다.

## 데이터와 모수

모수 θ의 모형 $f(x\mid\theta)$에 데이터 $x_{1:n}$을 고정하면 가능도는 $L(\theta)=f(x_{1:n}\mid\theta)$다. 독립·동일분포일 때 $L(\theta)=\prod_i f(x_i\mid\theta)$다. 연속형에서는 밀도의 곱이며 그 자체가 관측값 한 점의 확률은 아니다. θ에 대해 적분해서 1이 될 필요도 없다.

곱의 underflow를 피하고 미분을 쉽게 하기 위해 로그가능도 $\ell(\theta)=\sum_i\log f(x_i\mid\theta)$를 사용한다. 로그는 단조 증가하므로 최대점이 같다. 모수에 무관한 양의 상수는 최대점에는 영향을 주지 않지만 서로 다른 데이터 생성 모형의 확률 비교에서는 정규화를 임의로 버리지 않는다.

## Bernoulli MLE

독립 Bernoulli 표본 n개에서 성공 s개이면 $L(p)=p^s(1-p)^{n-s}$이고

$$
\ell'(p)=\frac{s}{p}-\frac{n-s}{1-p}=0
\quad\Rightarrow\quad\widehat p=s/n.
$$

0<s<n일 때 $\ell''(p)=-s/p^2-(n-s)/(1-p)^2<0$여서 유일한 내부 최대다. s=0 또는 n이면 최대는 경계 0 또는 1에 있다. 도함수가 0인 해만 찾으면 이 경우를 놓친다. 20개 중 성공 14개의 새 예에서 MLE는 0.7이다.

## 정규분포의 모수

독립 $X_i\sim\mathcal N(\mu,\sigma^2)$라면

$$
\ell=-\frac n2\log(2\pi\sigma^2)
-\frac1{2\sigma^2}\sum_i(x_i-\mu)^2.
$$

μ로 미분하면 $\widehat\mu=\overline x$, 분산으로 미분하면 $\widehat{\sigma^2}_{MLE}=\sum_i(x_i-\overline x)^2/n$이다. 불편 표본분산의 n−1 분모와 MLE의 n 분모를 구별한다. 새 데이터 1,2,3은 평균 2, MLE 분산 2/3, 불편 표본분산 1이다. n>1이고 값이 모두 같지 않은 통상적인 경우의 내부 최대를 계산했다. 분산을 0에 가깝게 보낼 수 있는 퇴화 데이터는 별도 취급한다.

## Beta 사전분포와 사후분포

$p\sim\operatorname{Beta}(\alpha,\beta)$, α,β>0이면 사전밀도는 $p^{\alpha-1}(1-p)^{\beta-1}/B(\alpha,\beta)$다. Bernoulli 가능도와 곱하면

$$
p\mid x\sim\operatorname{Beta}(\alpha+s,\beta+n-s).
$$

균등 사전 Beta(1,1)과 n=20,s=14의 새 예에서 사후분포는 Beta(15,7)이다. 사후평균은 15/22≈0.6818, 두 모수가 모두 1보다 큰 경우의 MAP는 (15−1)/(15+7−2)=0.7이다. 사후평균, MAP, MLE는 정의가 다르며 이 예처럼 일부 값만 같을 수 있다.

다음 한 시행의 성공 사후예측 확률은 $\int p\,\pi(p\mid x)dp=(\alpha+s)/(\alpha+\beta+n)$다. 위 예에서는 15/22다. 이는 p를 한 점으로 고정한 plug-in 예측과 달리 사후 불확실성을 적분한 결과다. 여러 미래 시행의 총성공 횟수는 beta-binomial 예측분포를 사용한다.

## 구간과 진단

사후 credible interval은 주어진 사후분포에서 지정한 확률질량을 포함하는 구간이다. 빈도주의 신뢰구간은 반복 표집에서 구간 구성 절차의 포함률을 말한다. 한 데이터를 두 해석으로 섞어 설명하지 않는다.

모형을 적합한 뒤에는 데이터와 모형의 예측 분포를 비교하고, 사전분포를 바꿨을 때 추정이 얼마나 달라지는지 확인한다. 독립 가정을 어긴 반복 측정을 더 큰 n으로 세면 구간이 과도하게 좁아질 수 있다.

## 유의점

- 최대점의 내부 미분 조건, 경계, 허용 모수 범위를 함께 확인한다.
- 확률 $P(x\mid\theta)$와 사후 $P(\theta\mid x)$의 조건 방향을 구분한다.
- 작은 표본에서 사전분포의 영향은 정규화 상수만의 문제가 아니다.

## 관련 개념

- [[bayes-update|베이즈 갱신]]
- [[confidence-interval-hypothesis-test|신뢰구간]]
- [[probability-random-variables|Bernoulli·이항분포]]

## 참고 자료

- [MIT 18.05, Classes and Readings](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/pages/classes-reading-and-in-class-materials/), Maximum Likelihood, Bayesian Updating와 Beta Distributions. 본문의 수치는 별도로 정한 데이터다.
