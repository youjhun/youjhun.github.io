---
title: 라플라스 변환 공식표
aliases: [라플라스 변환 표, 단위 계단 함수, unit step function, 디랙 델타, 이동 정리, shifting theorem, 합성곱 정리, convolution theorem, 부분분수 전개]
date: 2026-10-26
tags: [MAS201, 공학수학, 공식집]
description: 초기값 문제를 풀기 위한 단방향 라플라스 변환의 변환 쌍 표, 선형성·이동·미분·적분·합성곱·주기 함수 성질, 부분분수 전개, 계단과 임펄스 강제항을 다루는 예를 한곳에 모은 공식집.
---

> [!abstract] 한눈에
> 단방향 라플라스 변환 $F(s) = \int_0^\infty f(t)e^{-st}\,dt$는 미분을 $s$ 곱과 초기값으로 바꾸어, 상수계수 선형 초기값 문제를 대수식으로 만든다. 풀이는 변환, $Y(s)$에 대해 정리, 부분분수 전개, 표를 거꾸로 읽는 역변환의 네 단계다. 계단 함수와 임펄스로 표현한 불연속 강제항도 이동 정리로 같은 방식으로 다룬다.

## 풀이 순서

1. 방정식 양변을 변환한다. $y'$, $y''$은 아래 미분 공식으로 초기값을 넣어 바꾼다.
2. $Y(s)$에 대해 정리한다. $Y(s) = (\text{강제항 몫}) + (\text{초기값 몫})$ 꼴이 된다.
3. 부분분수로 나누고 $e^{-as}$ 인수는 따로 둔다.
4. 표를 거꾸로 읽어 $y(t)$를 얻고, 원식과 초기값에 대입해 확인한다.

## 변환 쌍

$a$, $\omega$는 상수, $n$은 0 이상의 정수다. 모든 쌍은 $\operatorname{Re}s$가 충분히 클 때 성립한다.

| $f(t)$ | $F(s)$ |
| --- | --- |
| $1$ | $1/s$ |
| $t^n$ | $n!/s^{n+1}$ |
| $t^{-1/2}$, $t^{1/2}$ | $\sqrt{\pi/s}$, $\sqrt\pi/(2s^{3/2})$ |
| $e^{at}$ | $1/(s - a)$ |
| $t^ne^{at}$ | $n!/(s - a)^{n+1}$ |
| $\sin\omega t$ | $\omega/(s^2 + \omega^2)$ |
| $\cos\omega t$ | $s/(s^2 + \omega^2)$ |
| $\sinh at$ | $a/(s^2 - a^2)$ |
| $\cosh at$ | $s/(s^2 - a^2)$ |
| $e^{at}\sin\omega t$ | $\omega/\big((s - a)^2 + \omega^2\big)$ |
| $e^{at}\cos\omega t$ | $(s - a)/\big((s - a)^2 + \omega^2\big)$ |
| $t\sin\omega t$ | $2\omega s/(s^2 + \omega^2)^2$ |
| $t\cos\omega t$ | $(s^2 - \omega^2)/(s^2 + \omega^2)^2$ |
| $\sin\omega t - \omega t\cos\omega t$ | $2\omega^3/(s^2 + \omega^2)^2$ |
| $\mathcal U(t - a)$ | $e^{-as}/s$ |
| $\delta(t - a)$ | $e^{-as}$ |

$\mathcal U(t - a)$는 $t < a$에서 0, $t \ge a$에서 1인 단위 계단 함수다. $\delta(t - a)$는 넓이 1인 순간 충격이다.

## 성질

| 성질 | 시간 영역 | $s$ 영역 |
| --- | --- | --- |
| 선형성 | $\alpha f + \beta g$ | $\alpha F + \beta G$ |
| $s$축 이동 | $e^{at}f(t)$ | $F(s - a)$ |
| $t$축 이동 | $f(t - a)\,\mathcal U(t - a)$ | $e^{-as}F(s)$ |
| 계단과 곱 | $g(t)\,\mathcal U(t - a)$ | $e^{-as}\,\mathcal L\{g(t + a)\}$ |
| 1계 도함수 | $f'(t)$ | $sF(s) - f(0)$ |
| 2계 도함수 | $f''(t)$ | $s^2F(s) - sf(0) - f'(0)$ |
| $n$계 도함수 | $f^{(n)}(t)$ | $s^nF - s^{n-1}f(0) - \cdots - f^{(n-1)}(0)$ |
| 적분 | $\int_0^t f(\tau)\,d\tau$ | $F(s)/s$ |
| $t$ 곱 | $t^nf(t)$ | $(-1)^nF^{(n)}(s)$ |
| $t$로 나눔 | $f(t)/t$ | $\int_s^\infty F(u)\,du$ |
| 합성곱 | $(f * g)(t) = \int_0^t f(\tau)g(t - \tau)\,d\tau$ | $F(s)G(s)$ |
| 주기 $T$ | $f(t + T) = f(t)$ | $\dfrac{1}{1 - e^{-sT}}\int_0^T e^{-st}f(t)\,dt$ |

초기값 정리 $f(0^+) = \lim_{s\to\infty}sF(s)$와 최종값 정리 $\lim_{t\to\infty}f(t) = \lim_{s\to0}sF(s)$도 자주 쓴다. 최종값 정리는 $sF(s)$의 극점이 모두 왼쪽 반평면에 있을 때만 쓸 수 있다.

## 부분분수

$Y(s) = P(s)/Q(s)$에서 분자의 차수가 분모보다 낮으면 분모의 인수에 따라 나눈다.

| 분모의 인수 | 항 | 역변환 |
| --- | --- | --- |
| $(s - a)$ | $A/(s - a)$ | $Ae^{at}$ |
| $(s - a)^m$ | $A_1/(s-a) + \cdots + A_m/(s-a)^m$ | $\sum_k A_k\dfrac{t^{k-1}}{(k-1)!}e^{at}$ |
| $(s - \alpha)^2 + \beta^2$ | $\dfrac{B(s - \alpha) + C\beta}{(s - \alpha)^2 + \beta^2}$ | $e^{\alpha t}(B\cos\beta t + C\sin\beta t)$ |

서로 다른 1차 인수의 계수는 $A = \lim_{s\to a}(s - a)Y(s)$로 바로 구한다(Heaviside 덮개법). 복소 인수는 완전제곱으로 바꾸어 $s$축 이동 쌍에 맞춘다.

## 예

- 임펄스 강제: $y'' + 3y' + 2y = \delta(t)$, $y(0) = y'(0) = 0$이면 $Y = 1/\big((s+1)(s+2)\big) = 1/(s+1) - 1/(s+2)$이고 $y = e^{-t} - e^{-2t}$다.
- 늦게 켜지는 계단: $y' + y = \mathcal U(t - 1)$, $y(0) = 0$이면 $Y = e^{-s}/\big(s(s+1)\big)$이다. $1/\big(s(s+1)\big)$의 역변환 $1 - e^{-t}$를 1만큼 밀어 $y = \big(1 - e^{-(t-1)}\big)\mathcal U(t - 1)$을 얻는다.
- 합성곱: $1/(s^2 + 1)^2 = \mathcal L\{\sin t\}\cdot\mathcal L\{\sin t\}$이므로 역변환은 $\int_0^t\sin\tau\sin(t - \tau)\,d\tau = \tfrac12(\sin t - t\cos t)$다.
- 주기 함수: $[0, 1)$에서 1, $[1, 2)$에서 0을 되풀이하는 사각파는 $F(s) = \dfrac{1 - e^{-s}}{s(1 - e^{-2s})} = \dfrac{1}{s(1 + e^{-s})}$이다.

네 예는 모두 직접 계산했다. 첫째 예의 $y$는 이 계의 임펄스 응답이고, 임의의 입력 $g$에 대한 영상태 응답은 $y = (e^{-t} - e^{-2t}) * g$다.

## 유의점

- 단방향 변환은 $t \ge 0$만 본다. 공학에서는 $f(0)$을 $0^-$의 값으로 쓰는 관례가 많아, 임펄스가 $t = 0$에 들어오면 $0^-$와 $0^+$의 초기값이 다를 수 있다.
- $t$축 이동은 $f(t - a)\,\mathcal U(t - a)$ 꼴에만 바로 적용된다. $f(t)\,\mathcal U(t - a)$는 표의 «계단과 곱» 공식으로 바꾼다.
- 최종값 정리를 진동하거나 발산하는 해에 쓰면 틀린 값이 나온다. 극점의 위치를 먼저 확인한다.
- 신호처리에서 쓰는 양방향 변환은 수렴영역까지 적어야 역변환이 하나로 정해진다. 초기값 문제에는 단방향 변환을 쓴다.

## 관련 개념

- [[laplace-transform|라플라스 변환]]: 양방향 변환, 수렴영역, 시스템 함수
- [[linear-second-order-ode|2계 선형 미분방정식 공식집]]
- [[linear-systems-ode|연립 선형 미분방정식]]: $(sI - A)^{-1}$로 구하는 행렬 지수
- [[first-order-rc-rl|RC·RL 응답]]

## 참고 자료

- Dennis G. Zill, _Advanced Engineering Mathematics_, Ch. 4 (The Laplace Transform).
- 표의 쌍과 예는 직접 계산해 확인했다.
