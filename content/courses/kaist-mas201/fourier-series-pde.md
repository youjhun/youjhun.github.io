---
title: 푸리에 급수와 편미분방정식
aliases: [반범위 전개, half-range expansion, 변수분리법, separation of variables, 열 방정식, heat equation, 파동 방정식, wave equation, 라플라스 방정식, Laplace equation, Sturm-Liouville 문제, d'Alembert 해, 고유함수 전개, 열 핵, heat kernel]
date: 2026-10-26
tags: [MAS201, 공학수학, 공식집]
description: 주기 2L 함수의 푸리에 급수 공식과 반범위 전개, 수렴 조건, 그리고 1차원 열 방정식·파동 방정식과 직사각형 영역의 라플라스 방정식을 변수분리로 푸는 공식과 경계조건별 고유함수, 비동차 방정식의 고유함수 전개, 푸리에 변환과 무한 구간 열 방정식을 한곳에 모은 공식집.
---

> [!abstract] 한눈에
> 구간 $(-L, L)$의 함수는 사인과 코사인의 무한합으로 전개되고, 계수는 직교성을 이용한 적분으로 구한다. 열·파동·라플라스 방정식을 변수분리하면 공간 부분이 경계조건을 가진 고윳값 문제가 되어, 해가 그 고유함수의 급수로 나온다. 초기조건이나 경계값은 푸리에 계수로 들어간다.

## 푸리에 급수

주기 $2L$인 $f$의 푸리에 급수는

$$
f(x) \sim \frac{a_0}{2} + \sum_{n=1}^{\infty}\left(a_n\cos\frac{n\pi x}{L} + b_n\sin\frac{n\pi x}{L}\right)
$$

$$
a_n = \frac1L\int_{-L}^{L}f(x)\cos\frac{n\pi x}{L}\,dx, \qquad b_n = \frac1L\int_{-L}^{L}f(x)\sin\frac{n\pi x}{L}\,dx
$$

이다. $a_0$도 같은 식에 $n = 0$을 넣어 구한다. $f$와 $f'$이 조각마다 연속이면 급수는 연속점에서 $f(x)$로, 불연속점에서 좌우 극한의 평균으로 수렴한다.

- 짝함수이면 $b_n = 0$이고 $a_n = \frac2L\int_0^L f\cos\frac{n\pi x}{L}\,dx$다.
- 홀함수이면 $a_n = 0$이고 $b_n = \frac2L\int_0^L f\sin\frac{n\pi x}{L}\,dx$다.
- Parseval 등식: $\frac1L\int_{-L}^{L}f^2\,dx = \frac{a_0^2}{2} + \sum(a_n^2 + b_n^2)$.

## 반범위 전개

$(0, L)$에서만 정의된 함수는 짝 확장하면 코사인 급수로, 홀 확장하면 사인 급수로 쓸 수 있다. 경계에서 값이 0이어야 하는 문제는 사인 급수를, 기울기가 0이어야 하는 문제는 코사인 급수를 쓴다.

자주 쓰는 전개는 다음과 같다($L = \pi$, 직접 계산한 값).

| $f(x)$ | 급수 |
| --- | --- |
| $(0, \pi)$에서 1, $(-\pi, 0)$에서 $-1$ (사각파) | $\dfrac4\pi\sum_{n\text{ 홀수}}\dfrac{\sin nx}{n}$ |
| $x$, $-\pi < x < \pi$ | $2\sum_{n\ge1}\dfrac{(-1)^{n+1}}{n}\sin nx$ |
| $\lvert x\rvert$, $-\pi < x < \pi$ | $\dfrac\pi2 - \dfrac4\pi\sum_{n\text{ 홀수}}\dfrac{\cos nx}{n^2}$ |

주기 확장한 함수에 불연속이 있으면 계수는 $1/n$로, 연속이지만 꺾여 있으면 $1/n^2$로 줄어든다. 표의 $x$는 구간 안에서 연속이지만 주기 확장하면 $\pm\pi$에서 끊겨 $1/n$로 줄어든다.

## 변수분리

$u(x, t) = X(x)T(t)$로 두고 방정식에 넣어 양변을 $X$와 $T$의 식으로 나누면, 두 쪽이 같은 상수 $-\lambda$여야 한다. 공간 부분 $X'' + \lambda X = 0$은 경계조건이 붙은 고윳값 문제다.

| 경계조건 ($0 < x < L$) | 고윳값 $\lambda_n$ | 고유함수 $X_n$ |
| --- | --- | --- |
| $X(0) = X(L) = 0$ | $(n\pi/L)^2$, $n = 1, 2, \dots$ | $\sin(n\pi x/L)$ |
| $X'(0) = X'(L) = 0$ | $(n\pi/L)^2$, $n = 0, 1, \dots$ | $\cos(n\pi x/L)$ |
| $X(0) = 0$, $X'(L) = 0$ | $\big((2n-1)\pi/(2L)\big)^2$ | $\sin\big((2n-1)\pi x/(2L)\big)$ |

이 고윳값 문제는 Sturm-Liouville 문제 $\big(r(x)y'\big)' + \big(q(x) + \lambda p(x)\big)y = 0$의 가장 단순한 예($r = p = 1$, $q = 0$)다. 일반적으로 서로 다른 고윳값의 고유함수는 가중치 $p(x)$를 붙인 적분에서 직교하고, 그래서 푸리에 계수처럼 적분으로 계수를 구할 수 있다.

## 열 방정식

양 끝 온도가 0인 막대: $u_t = ku_{xx}$, $u(0, t) = u(L, t) = 0$, $u(x, 0) = f(x)$.

$$
u(x, t) = \sum_{n=1}^{\infty}b_ne^{-k(n\pi/L)^2t}\sin\frac{n\pi x}{L}, \qquad b_n = \frac2L\int_0^Lf(x)\sin\frac{n\pi x}{L}\,dx
$$

높은 모드일수록 $n^2$에 비례해 빨리 감쇠하므로, 시간이 조금 지나면 첫 항이 해를 거의 결정한다. 처음 온도가 100으로 균일하면 $b_n = 400/(n\pi)$($n$ 홀수), 0($n$ 짝수)이다(직접 계산한 예).

양 끝이 단열($u_x = 0$)이면 코사인 급수가 되고, 상수항 $a_0/2$가 남아 최종 온도는 처음 온도의 평균이다. 양 끝 온도가 0이 아닌 상수이면 정상상태 직선 해를 먼저 빼고 나머지를 위 식으로 푼다.

## 파동 방정식

양 끝이 고정된 줄: $u_{tt} = c^2u_{xx}$, $u(0, t) = u(L, t) = 0$, $u(x, 0) = f(x)$, $u_t(x, 0) = g(x)$.

$$
u(x, t) = \sum_{n=1}^{\infty}\left(A_n\cos\frac{n\pi ct}{L} + B_n\sin\frac{n\pi ct}{L}\right)\sin\frac{n\pi x}{L}
$$

$A_n$은 $f$의 사인 계수, $B_n$은 $g$의 사인 계수에 $L/(n\pi c)$를 곱한 값이다. 무한히 긴 줄에서는 d'Alembert 해

$$
u(x, t) = \frac{f(x - ct) + f(x + ct)}{2} + \frac{1}{2c}\int_{x-ct}^{x+ct}g(s)\,ds
$$

를 쓴다. 처음 속도가 0($g = 0$)이면 처음 모양이 반으로 나뉘어 양쪽으로 속도 $c$로 퍼져 나간다.

## 라플라스 방정식

직사각형 $0 < x < a$, $0 < y < b$에서 $u_{xx} + u_{yy} = 0$이고, 위쪽 변만 $u(x, b) = f(x)$, 나머지 세 변이 0이면

$$
u(x, y) = \sum_{n=1}^{\infty}A_n\sinh\frac{n\pi y}{a}\sin\frac{n\pi x}{a}, \qquad A_n = \frac{2}{a\sinh(n\pi b/a)}\int_0^af(x)\sin\frac{n\pi x}{a}\,dx
$$

다. 네 변 모두에 값이 주어지면 한 변씩 값이 있는 문제 넷으로 나누어 풀고 더한다. 원판이나 원통 영역에서 변수분리하면 반지름 부분이 Bessel 방정식이 되고, 구에서는 각도 부분이 Legendre 방정식이 된다.

반지름 $b$인 원형 막의 축대칭 진동 $u_{tt} = c^2(u_{rr} + u_r/r)$, $u(b, t) = 0$의 해는

$$
u(r, t) = \sum_{n=1}^{\infty}\big(A_n\cos c\alpha_nt + B_n\sin c\alpha_nt\big)J_0(\alpha_nr)
$$

이고, $\alpha_nb$는 $J_0$의 $n$번째 영점이다. 계수는 [[series-solutions-special-functions|Fourier-Bessel 전개]]로 구한다. $J_0$의 영점 비(약 1 : 2.30 : 3.60)가 정수가 아니어서, 고유진동수가 줄처럼 기본 진동수의 정수배로 늘어서지 않는다(직접 계산한 값).

## 비동차 방정식

열원이 있는 막대 $u_t = ku_{xx} + F(x, t)$, $u(0, t) = u(L, t) = 0$은 해를 경계조건에 맞는 고유함수로 전개해 푼다. $u = \sum T_n(t)\sin(n\pi x/L)$로 두고 $F$도 같은 사인 급수로 전개하면, 계수마다 1계 선형식

$$
T_n' + k\lambda_nT_n = F_n(t), \qquad \lambda_n = (n\pi/L)^2
$$

을 얻는다. $T_n(0)$은 초기 온도의 사인 계수이고, 해는 [[first-order-ode-methods|1계 선형식]]의 적분인자 공식으로 쓴다.

$F = Q$(상수)이고 처음 온도가 0이면, 정상상태 $u_s = Qx(L - x)/(2k)$를 먼저 구해 빼는 편이 간단하다. 남은 부분은 처음값이 $-u_s$인 동차 열 방정식이어서

$$
u(x, t) = \frac{Qx(L - x)}{2k} - \sum_{n\text{ 홀수}}\frac{4L^2Q}{\pi^3kn^3}e^{-k(n\pi/L)^2t}\sin\frac{n\pi x}{L}
$$

이다(직접 계산한 예).

## 푸리에 변환

무한한 구간에서는 급수 대신 적분을 쓴다. 공학에서 흔한 관례로

$$
F(\omega) = \int_{-\infty}^{\infty}f(t)e^{-i\omega t}\,dt, \qquad f(t) = \frac{1}{2\pi}\int_{-\infty}^{\infty}F(\omega)e^{i\omega t}\,d\omega
$$

로 정의한다. 신호처리에서는 $i$ 대신 $j$를 쓰는 경우가 많다. 교재마다 지수의 부호와 $2\pi$를 어디에 두는지가 달라, 표를 섞어 쓸 때는 관례를 먼저 맞춘다.

| $f(t)$ | $F(\omega)$ |
| --- | --- |
| $e^{-a\lvert t\rvert}$ ($a > 0$) | $2a/(a^2 + \omega^2)$ |
| $\lvert t\rvert < T/2$에서 1, 밖에서 0 | $2\sin(\omega T/2)/\omega$ |
| $e^{-t^2/(2\sigma^2)}$ | $\sigma\sqrt{2\pi}\,e^{-\sigma^2\omega^2/2}$ |
| $\delta(t)$ | $1$ |
| $f'(t)$ | $i\omega F(\omega)$ |
| $f(t - t_0)$ | $e^{-i\omega t_0}F(\omega)$ |
| $(f * g)(t)$ | $F(\omega)G(\omega)$ |

에너지는 $\int\lvert f\rvert^2\,dt = \frac{1}{2\pi}\int\lvert F\rvert^2\,d\omega$로 보존된다(Parseval). 무한한 막대의 열 방정식 $u_t = ku_{xx}$, $u(x, 0) = f(x)$를 $x$에 대해 변환하면 $\hat u_t = -k\omega^2\hat u$가 되어

$$
u(x, t) = \int_{-\infty}^{\infty}f(\xi)\frac{1}{\sqrt{4\pi kt}}e^{-(x - \xi)^2/(4kt)}\,d\xi
$$

를 얻는다. 처음 온도 분포를 표준편차가 $\sqrt{2kt}$로 커지는 가우스 함수와 합성곱한 꼴이다. 표의 쌍과 이 해는 sympy로 확인했다.

## 유의점

- 불연속점 근처에서 부분합은 점프 크기의 약 9%만큼 넘친다(Gibbs 현상). 항을 늘려도 넘치는 높이는 줄지 않는다.
- 변수분리는 방정식과 경계조건이 모두 동차일 때 쓸 수 있다. 비동차 경계조건은 정상상태 해를 빼서 동차로 만든 뒤 쓴다.
- 열 방정식의 해는 시간이 지나면 매끄러워지지만, 파동 방정식의 해는 처음 모양의 꺾임과 불연속을 그대로 실어 나른다.
- 반범위 전개에서 사인과 코사인 가운데 어느 것을 쓸지는 경계조건이 정한다.

## 관련 개념

- [[fourier-series|푸리에 급수]]: 복소 지수 형태, 스펙트럼, Gibbs 현상의 그림
- [[fourier-transform|연속시간 푸리에 변환]]: 신호처리 관점의 성질과 쌍
- [[series-solutions-special-functions|급수해와 특수함수]]
- [[diffusion-ficks-law|확산과 Fick 법칙]]: 열 방정식과 같은 꼴의 확산 방정식
- [[linear-second-order-ode|2계 선형 미분방정식 공식집]]

## 참고 자료

- Dennis G. Zill, _Advanced Engineering Mathematics_, «Orthogonal Functions and Fourier Series»와 «Boundary-Value Problems in Rectangular Coordinates» 장(판에 따라 장 번호가 다르다).
- 표의 급수와 열 방정식 예의 계수는 직접 계산했고, 해는 원식에 대입해 확인했다.
