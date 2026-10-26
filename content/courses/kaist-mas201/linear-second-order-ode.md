---
title: 2계 선형 미분방정식 공식집
aliases: [2계 선형 ODE, 특성방정식, characteristic equation, 미정계수법, method of undetermined coefficients, 매개변수 변환법, variation of parameters, 론스키안, Wronskian, 계수 내림, reduction of order, Cauchy-Euler 방정식, Cauchy-Euler equation, 감쇠비, damping ratio, 강제 진동]
date: 2026-10-26
tags: [MAS201, 공학수학, 공식집]
description: 2계 선형 상미분방정식의 해 구조, 상수계수 특성방정식, 계수 내림, Wronskian과 Abel 공식, 미정계수법 표, 매개변수 변환법, Cauchy-Euler 방정식, 질량-용수철·RLC 진동과 공진을 한곳에 모은 공식집.
---

> [!abstract] 한눈에
> 2계 선형식의 일반해는 동차식의 독립인 두 해의 선형결합에 특수해 하나를 더한 것이다. 상수계수 동차식은 특성방정식의 근으로 풀리고, 특수해는 강제항의 꼴에 따라 미정계수법이나 매개변수 변환법으로 구한다. 질량-용수철과 RLC 회로는 같은 방정식이어서 감쇠비 하나로 응답의 모양이 정해진다.

## 해의 구조

표준형 $y'' + P(x)y' + Q(x)y = g(x)$에서 $P$, $Q$, $g$가 구간 $I$에서 연속이면, $I$ 안의 한 점에서 $y$와 $y'$를 정한 초기값 문제의 해는 하나뿐이다.

- 동차식($g = 0$)의 해는 더하고 상수배해도 해다.
- 동차식의 독립인 해 $y_1$, $y_2$가 있으면 동차식의 모든 해는 $y_c = c_1y_1 + c_2y_2$다.
- 비동차식의 일반해는 $y = y_c + y_p$다. $y_p$는 비동차식을 만족하는 아무 해나 하나 고르면 된다.
- 강제항이 $g_1 + g_2$이면 각각의 특수해를 더한다.

## Wronskian과 계수 내림

두 해의 독립성은 Wronskian으로 판정한다.

$$
W(y_1, y_2) = y_1y_2' - y_1'y_2, \qquad W(x) = Ce^{-\int P(x)\,dx}
$$

둘째 식은 Abel 공식이다. 동차식의 두 해의 $W$는 구간 전체에서 0이거나 어디서도 0이 아니어서, 한 점에서만 확인하면 된다.

해 하나 $y_1$을 알면 둘째 해를 계수 내림으로 구한다.

$$
y_2 = y_1\int\frac{e^{-\int P\,dx}}{y_1^2}\,dx
$$

예를 들어 $x^2y'' - 3xy' + 4y = 0$($x > 0$)은 $y_1 = x^2$을 가진다. 표준형의 $P = -3/x$이므로 $e^{-\int P} = x^3$이고, $y_2 = x^2\int x^3/x^4\,dx = x^2\ln x$다(교재에 흔한 예이고, 직접 다시 계산했다).

## 상수계수 동차식

$ay'' + by' + cy = 0$에 $y = e^{rx}$를 넣으면 특성방정식 $ar^2 + br + c = 0$을 얻는다.

| 근 | 동차해 |
| --- | --- |
| 서로 다른 실근 $r_1$, $r_2$ | $c_1e^{r_1x} + c_2e^{r_2x}$ |
| 중근 $r$ | $(c_1 + c_2x)e^{rx}$ |
| 복소근 $\alpha \pm i\beta$ | $e^{\alpha x}(c_1\cos\beta x + c_2\sin\beta x)$ |

고계 식도 같다. $m$중근 $r$은 $e^{rx}, xe^{rx}, \dots, x^{m-1}e^{rx}$를, $m$중 복소근은 여기에 $\cos$, $\sin$을 곱한 $2m$개의 해를 준다.

## 미정계수법

계수가 상수이고 강제항이 다항식, 지수, 사인·코사인과 그 곱일 때 쓴다. 강제항의 꼴과 같은 꼴의 후보를 넣어 계수를 맞춘다.

| 강제항 $g(x)$ | 후보 $y_p$ |
| --- | --- |
| $k$ (상수) | $A$ |
| $n$차 다항식 | $A_nx^n + \cdots + A_1x + A_0$ |
| $e^{ax}$ | $Ae^{ax}$ |
| $\cos\beta x$ 또는 $\sin\beta x$ | $A\cos\beta x + B\sin\beta x$ |
| $n$차 다항식 $\times\, e^{ax}$ | $(A_nx^n + \cdots + A_0)e^{ax}$ |
| $e^{ax}\cos\beta x$ 또는 $e^{ax}\sin\beta x$ | $e^{ax}(A\cos\beta x + B\sin\beta x)$ |
| $n$차 다항식 $\times\, e^{ax}\cos\beta x$ | $e^{ax}(p_n(x)\cos\beta x + q_n(x)\sin\beta x)$ |

후보의 어느 항이 동차해와 겹치면 후보 전체에 $x^s$를 곱한다. $s$는 겹치는 항이 없어지는 가장 작은 자연수이고, 2계 식에서는 1이나 2다.

- $y'' - y' - 2y = 4x^2$: 후보 $Ax^2 + Bx + C$에서 $y_p = -2x^2 + 2x - 3$이다.
- $y'' - 2y' + y = e^x$: 특성근 1이 중근이어서 $e^x$와 $xe^x$가 모두 동차해다. 후보를 $Ax^2e^x$로 올려 $y_p = \tfrac12x^2e^x$를 얻는다.

두 예는 직접 계산했다. 강제항이 $\tan x$, $\sec x$, $\ln x$, $1/x$처럼 표에 없는 꼴이거나 계수가 상수가 아니면 매개변수 변환법을 쓴다.

## 매개변수 변환법

동차해 $y_1$, $y_2$를 알면 표준형 $y'' + Py' + Qy = g$의 특수해는

$$
y_p = -y_1\int\frac{y_2\,g}{W}\,dx + y_2\int\frac{y_1\,g}{W}\,dx
$$

다. $g$는 표준형(최고차 계수 1)의 우변이어야 한다. $ay''$ 꼴이면 먼저 $a$로 나눈다.

예를 들어 $y'' + y = \sec x$는 $y_1 = \cos x$, $y_2 = \sin x$, $W = 1$이다. 두 적분은 $-\int\sin x\sec x\,dx = \ln\lvert\cos x\rvert$와 $\int\cos x\sec x\,dx = x$이므로 $y_p = \cos x\ln\lvert\cos x\rvert + x\sin x$다(직접 계산한 예).

## Cauchy-Euler 방정식

$x^2y'' + axy' + by = 0$($x > 0$)에 $y = x^r$을 넣으면 보조방정식 $r(r-1) + ar + b = 0$을 얻는다. $x = e^t$로 바꾸면 상수계수 식이 되므로 해의 꼴이 상수계수 표와 대응한다.

| 보조방정식의 근 | 해 |
| --- | --- |
| 서로 다른 실근 $r_1$, $r_2$ | $c_1x^{r_1} + c_2x^{r_2}$ |
| 중근 $r$ | $(c_1 + c_2\ln x)x^r$ |
| 복소근 $\alpha \pm i\beta$ | $x^\alpha\big(c_1\cos(\beta\ln x) + c_2\sin(\beta\ln x)\big)$ |

$x^2y'' - xy' + y = 0$은 $r^2 - 2r + 1 = 0$의 중근 1에서 $(c_1 + c_2\ln x)x$이고, $x^2y'' + xy' + 4y = 0$은 $r = \pm 2i$에서 $c_1\cos(2\ln x) + c_2\sin(2\ln x)$다(직접 계산한 예). $x < 0$에서는 $\ln x$ 자리에 $\ln\lvert x\rvert$를 쓴다.

## 진동

질량-용수철과 직렬 RLC 회로는 같은 꼴이다.

| 계 | 방정식 | 고유진동수 $\omega_n$ | 감쇠비 $\zeta$ |
| --- | --- | --- | --- |
| 질량-용수철 | $mx'' + cx' + kx = F(t)$ | $\sqrt{k/m}$ | $c/(2\sqrt{mk})$ |
| 직렬 RLC | $Lq'' + Rq' + q/C = E(t)$ | $1/\sqrt{LC}$ | $(R/2)\sqrt{C/L}$ |

질량-용수철은 $x'' + 2\zeta\omega_nx' + \omega_n^2x = F(t)/m$으로, RLC는 같은 꼴에 $x$ 대신 $q$, 우변 $E(t)/L$을 넣어 쓸 수 있다. 특성근은 $-\zeta\omega_n \pm \omega_n\sqrt{\zeta^2 - 1}$이다.

| 감쇠 | 조건 | 자유 응답 |
| --- | --- | --- |
| 과감쇠 | $\zeta > 1$ | 두 지수의 합, 진동 없음 |
| 임계감쇠 | $\zeta = 1$ | $(c_1 + c_2t)e^{-\omega_nt}$, 진동이 없고, 진동하지 않는 경우 가운데 감쇠율이 가장 큼 |
| 부족감쇠 | $0 < \zeta < 1$ | $e^{-\zeta\omega_nt}(c_1\cos\omega_dt + c_2\sin\omega_dt)$, $\omega_d = \omega_n\sqrt{1 - \zeta^2}$ |
| 무감쇠 | $\zeta = 0$ | $c_1\cos\omega_nt + c_2\sin\omega_nt$ |

$F(t) = F_0\cos\omega t$로 강제하면 정상상태 응답은 같은 진동수의 코사인이고, 진폭은

$$
A = \frac{F_0/m}{\sqrt{(\omega_n^2 - \omega^2)^2 + (2\zeta\omega_n\omega)^2}}
$$

다. $\zeta < 1/\sqrt2$이면 진폭이 $\omega = \omega_n\sqrt{1 - 2\zeta^2}$에서 가장 크고, 그 값은 정적 변위 $F_0/k$의 $1/(2\zeta\sqrt{1-\zeta^2})$배다. 감쇠가 없으면($\zeta = 0$, $\omega = \omega_n$) 특수해가 $\frac{F_0}{2m\omega_n}t\sin\omega_nt$로 시간에 비례해 커진다.

![[../../images/linear-second-order-ode/damping.png]]
*그림 1. 왼쪽은 $x(0) = 1$, $x'(0) = 0$에서 출발한 자유 응답을 감쇠비별로 수치 적분한 것이고, 오른쪽은 위 진폭 식을 정적 변위로 나눈 진폭비다. 직접 계산했다.*

그림 1의 오른쪽에서 $\zeta = 0.1$의 최대 진폭비는 약 5.0, $\zeta = 0.2$는 약 2.55이고, $\zeta = 0.5$에서는 $0.707\omega_n$에서 약 1.15로 낮아진다. $\zeta \ge 1/\sqrt2$이면 봉우리가 없다(직접 계산한 값).

## 유의점

- 초기조건은 일반해 $y_c + y_p$에 적용한다. $y_c$에만 적용하면 상수가 틀린다.
- 미정계수법의 후보가 동차해와 겹치면 후보 전체에 $x^s$를 곱한다. 겹치는 항에만 곱하면 계수가 맞지 않는다.
- 매개변수 변환법의 $g$는 최고차 계수를 1로 만든 표준형의 우변이다.
- 공진 봉우리의 위치 $\omega_n\sqrt{1-2\zeta^2}$, 감쇠 진동수 $\omega_d = \omega_n\sqrt{1-\zeta^2}$, 고유진동수 $\omega_n$은 서로 다른 값이다.
- Cauchy-Euler 방정식은 $x = 0$에서 표준형 계수가 정의되지 않으므로 $x > 0$과 $x < 0$을 따로 푼다.

## 관련 개념

- [[first-order-ode-methods|1계 미분방정식 풀이법 모음]]
- [[laplace-transform-table|라플라스 변환 공식표]]: 초기조건과 불연속 강제항을 함께 다루는 방법
- [[linear-systems-ode|연립 선형 미분방정식]]: 2계 식을 1계 연립식으로 바꾸어 푸는 방법
- [[second-order-systems-numerics|고계 선형식·연립계·수치해]]: 상수계수 식, 상태공간, Euler 안정성을 짧게 묶은 개관
- [[second-order-rlc|RLC 2차 회로]]

## 참고 자료

- Dennis G. Zill, _Advanced Engineering Mathematics_, «Higher-Order Differential Equations» 장(판에 따라 장 번호가 다르다).
- 예의 해는 모두 직접 계산했고, 원식에 대입해 확인했다.
