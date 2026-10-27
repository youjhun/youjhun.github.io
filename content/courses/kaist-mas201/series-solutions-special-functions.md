---
title: 급수해와 특수함수
aliases: [급수해, power series solution, Frobenius 방법, Frobenius method, 결정방정식, indicial equation, Legendre 방정식, Legendre 다항식, Bessel 방정식, Bessel 함수, 감마 함수, gamma function, Hermite 다항식, Chebyshev 다항식, Laguerre 다항식, 직교 다항식]
date: 2026-10-26
tags: [MAS201, 공학수학, 공식집]
description: 계수가 상수가 아닌 2계 선형식을 거듭제곱급수로 푸는 방법, 정칙특이점에서의 Frobenius 방법과 세 경우, Legendre 방정식과 다항식, Bessel 방정식과 Bessel 함수, Hermite·Chebyshev·Laguerre 다항식의 공식과 성질을 한곳에 모은 공식집.
---

> [!abstract] 한눈에
> 계수가 $x$의 함수인 2계 선형식은 대개 닫힌 꼴의 해가 없어, 해를 거듭제곱급수로 두고 계수의 점화식을 구한다. 계수가 매끄러운 보통점에서는 Taylor 급수로, 정칙특이점에서는 $x^r$을 곱한 Frobenius 급수로 푼다. Bessel 함수와 Legendre 다항식은 이렇게 얻는 해로, 원통·구 좌표 문제에 되풀이해 나온다.

## 보통점과 특이점

표준형 $y'' + P(x)y' + Q(x)y = 0$에서 $P$, $Q$가 $x_0$ 근처에서 Taylor 급수로 전개되면 $x_0$는 보통점이고, 아니면 특이점이다.

| 점의 종류 | 판별 | 해의 꼴 |
| --- | --- | --- |
| 보통점 | $P$, $Q$가 $x_0$에서 해석적 | $y = \sum_{n\ge0}a_n(x - x_0)^n$ |
| 정칙특이점 | $(x - x_0)P$, $(x - x_0)^2Q$가 해석적 | $y = (x - x_0)^r\sum_{n\ge0}c_n(x - x_0)^n$ |
| 비정칙특이점 | 위 둘 다 아님 | 이 글의 방법으로는 다루지 않음 |

보통점에서 얻은 급수해의 수렴 반지름은 $x_0$에서 가장 가까운 특이점(복소평면 위의 특이점 포함)까지의 거리 이상이다.

## 거듭제곱급수

보통점에서는 $y = \sum a_nx^n$을 넣고, 같은 거듭제곱의 계수를 0으로 놓아 점화식을 얻는다. 첨자를 맞추려면 각 합의 첨자를 옮겨 모두 $x^n$으로 쓴다.

Airy 방정식 $y'' - xy = 0$은 $2a_2 = 0$과 $a_{k+3} = a_k/\big((k+3)(k+2)\big)$를 준다. $a_0$과 $a_1$이 자유 상수로 남아 두 독립해가 나온다.

$$
y_1 = 1 + \frac{x^3}{6} + \frac{x^6}{180} + \cdots, \qquad y_2 = x + \frac{x^4}{12} + \frac{x^7}{504} + \cdots
$$

두 급수는 직접 계산했고, 모든 $x$에서 수렴한다.

## Frobenius 방법

정칙특이점 $x = 0$에서는 $y = \sum c_nx^{n+r}$을 넣는다. 가장 낮은 거듭제곱의 계수에서 $r$에 대한 결정방정식을 얻고, 두 근 $r_1 \ge r_2$(실수일 때)의 차이에 따라 둘째 해의 꼴이 정해진다.

| 근의 관계 | 둘째 해 |
| --- | --- |
| $r_1 - r_2$가 정수가 아님 | $y_2 = \sum c_nx^{n+r_2}$, 두 근으로 각각 급수 |
| $r_1 = r_2$ | $y_2 = y_1\ln x + \sum_{n\ge1}b_nx^{n+r_1}$ |
| $r_1 - r_2$가 양의 정수 | $y_2 = Cy_1\ln x + \sum_{n\ge0}b_nx^{n+r_2}$, $C$는 0일 수도 있음 |

$2xy'' + y' + y = 0$은 결정방정식 $2r(r-1) + r = 0$에서 $r = 0$, $1/2$이고, 점화식은 $c_n = -c_{n-1}/\big((n + r)(2n + 2r - 1)\big)$이다. 두 급수의 합은 각각 $\cos\sqrt{2x}$와 $\sin\sqrt{2x}$다(직접 계산한 예).

## Legendre 방정식

$(1 - x^2)y'' - 2xy' + n(n+1)y = 0$은 $x = \pm1$에 정칙특이점이 있다. $n$이 0 이상의 정수이면 급수 하나가 끊겨 다항식이 된다. 이 다항식을 $P_n(1) = 1$이 되도록 정규화해 Legendre 다항식 $P_n$이라 부른다.

| $n$ | $P_n(x)$ |
| --- | --- |
| 0 | $1$ |
| 1 | $x$ |
| 2 | $\tfrac12(3x^2 - 1)$ |
| 3 | $\tfrac12(5x^3 - 3x)$ |
| 4 | $\tfrac18(35x^4 - 30x^2 + 3)$ |

- Rodrigues 공식: $P_n(x) = \dfrac{1}{2^nn!}\dfrac{d^n}{dx^n}(x^2 - 1)^n$
- 점화식: $(n+1)P_{n+1} = (2n+1)xP_n - nP_{n-1}$
- 직교성: $\int_{-1}^{1}P_mP_n\,dx = \dfrac{2}{2n+1}\delta_{mn}$
- Fourier-Legendre 전개: $f(x) = \sum c_nP_n(x)$, $c_n = \dfrac{2n+1}{2}\int_{-1}^{1}f(x)P_n(x)\,dx$

구 좌표에서 축 대칭인 라플라스 방정식을 변수분리하면 각도 부분이 $x = \cos\theta$인 Legendre 방정식이 된다.

## Bessel 방정식

$x^2y'' + xy' + (x^2 - \nu^2)y = 0$($\nu \ge 0$)은 $x = 0$이 정칙특이점이고 결정방정식의 근이 $\pm\nu$다. 제1종 Bessel 함수는

$$
J_\nu(x) = \sum_{n=0}^{\infty}\frac{(-1)^n}{n!\,\Gamma(1 + \nu + n)}\left(\frac{x}{2}\right)^{2n+\nu}
$$

이다. $\nu$가 정수가 아니면 일반해는 $c_1J_\nu + c_2J_{-\nu}$이고, 정수이면 $J_{-n} = (-1)^nJ_n$이어서 제2종 함수 $Y_\nu$를 쓴다. $Y_\nu$는 $x \to 0$에서 발산하므로, 원점을 포함하는 영역의 유한한 해에는 $J_\nu$만 남는다.

| 방정식 | 일반해 |
| --- | --- |
| $x^2y'' + xy' + (x^2 - \nu^2)y = 0$ | $c_1J_\nu(x) + c_2Y_\nu(x)$ |
| $x^2y'' + xy' + (\alpha^2x^2 - \nu^2)y = 0$ | $c_1J_\nu(\alpha x) + c_2Y_\nu(\alpha x)$ |
| $x^2y'' + xy' - (x^2 + \nu^2)y = 0$ (수정 Bessel) | $c_1I_\nu(x) + c_2K_\nu(x)$ |

자주 쓰는 성질은 다음과 같다.

- $\dfrac{d}{dx}\big[x^\nu J_\nu\big] = x^\nu J_{\nu-1}$, $\dfrac{d}{dx}\big[x^{-\nu}J_\nu\big] = -x^{-\nu}J_{\nu+1}$, 특히 $J_0' = -J_1$
- $J_{\nu-1} + J_{\nu+1} = \dfrac{2\nu}{x}J_\nu$
- $J_{1/2}(x) = \sqrt{\dfrac{2}{\pi x}}\sin x$, $J_{-1/2}(x) = \sqrt{\dfrac{2}{\pi x}}\cos x$
- $J_0$의 영점은 약 2.405, 5.520이고 $J_1$의 첫 영점은 약 3.832다.
- $J_n(\alpha_ib) = 0$인 서로 다른 $\alpha_i$, $\alpha_j$에 대해 $\int_0^b xJ_n(\alpha_ix)J_n(\alpha_jx)\,dx = 0$이다(가중치 $x$의 직교성).
- Fourier-Bessel 전개: $f(x) = \sum_i c_iJ_n(\alpha_ix)$, $c_i = \dfrac{2}{b^2J_{n+1}(\alpha_ib)^2}\int_0^b xJ_n(\alpha_ix)f(x)\,dx$

감마 함수는 $\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}\,dt$이고 $\Gamma(z+1) = z\Gamma(z)$, $\Gamma(n+1) = n!$, $\Gamma(1/2) = \sqrt\pi$다.

## 그 밖의 직교 다항식

다른 2계 방정식에서도 $n$이 정수이면 다항식 해가 나오고, 각 다항식은 정해진 구간과 가중치에서 서로 직교한다.

| 이름 | 방정식 | 구간, 가중치 | 처음 몇 개 | $\int w\,y_n^2\,dx$ |
| --- | --- | --- | --- | --- |
| Hermite $H_n$ | $y'' - 2xy' + 2ny = 0$ | $(-\infty, \infty)$, $e^{-x^2}$ | $1$, $2x$, $4x^2 - 2$, $8x^3 - 12x$ | $2^nn!\sqrt\pi$ |
| Chebyshev $T_n$ | $(1 - x^2)y'' - xy' + n^2y = 0$ | $(-1, 1)$, $1/\sqrt{1 - x^2}$ | $1$, $x$, $2x^2 - 1$, $4x^3 - 3x$ | $\pi$ ($n = 0$), $\pi/2$ ($n \ge 1$) |
| Laguerre $L_n$ | $xy'' + (1 - x)y' + ny = 0$ | $(0, \infty)$, $e^{-x}$ | $1$, $1 - x$, $\tfrac12(x^2 - 4x + 2)$ | $1$ |

Hermite 다항식은 양자 조화진동자에서, 연관 Laguerre 다항식은 수소 원자의 반지름 방향 해에서 나온다. Chebyshev 다항식은 $T_n(\cos\theta) = \cos n\theta$를 만족해 $[-1, 1]$에서 값이 $\pm1$ 사이를 고르게 오르내리고, 이 성질 때문에 함수 근사와 필터 설계에 쓰인다. 표의 다항식과 노름은 sympy로 확인했다.

## 유의점

- 급수해의 첨자를 옮길 때 처음 몇 항(위 예의 $2a_2 = 0$ 같은 식)을 빠뜨리기 쉽다.
- 정칙특이점에서 결정방정식의 두 근 차이가 정수이면 둘째 해에 로그항이 들어갈 수 있다. 둘째 근으로 만든 급수가 그대로 해가 된다고 가정하지 않는다.
- Bessel 방정식의 $\nu$가 정수이면 $J_\nu$와 $J_{-\nu}$가 독립이 아니다. 이때 일반해에는 $Y_\nu$를 쓴다.
- 수치값(Bessel 영점 등)은 표나 라이브러리에서 가져와 쓰고, 급수를 몇 항만 더해 큰 $x$에서 쓰지 않는다.

## 관련 개념

- [[linear-second-order-ode|2계 선형 미분방정식 공식집]]
- [[fourier-series-pde|푸리에 급수와 편미분방정식]]: Bessel·Legendre 함수가 나오는 변수분리
- [[second-order-systems-numerics|고계 선형식·연립계·수치해]]

## 참고 자료

- Dennis G. Zill, _Advanced Engineering Mathematics_, «Series Solutions of Linear Differential Equations» 장(판에 따라 장 번호가 다르다).
- 예와 점화식은 직접 계산했고, Legendre 다항식과 Bessel 함수의 성질은 수치로 확인했다.
