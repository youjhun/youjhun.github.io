---
title: 연립 선형 미분방정식
aliases: [연립 선형 ODE, 1계 연립 미분방정식, 고윳값 방법, 기본 행렬, fundamental matrix, 행렬 지수, matrix exponential, 위상 초상, phase portrait, 안장점, 마디점, 나선점, 선형화, Jacobian 선형화]
date: 2026-10-26
tags: [MAS201, 공학수학, 공식집]
description: 상수계수 1계 연립 선형식 X' = AX를 고윳값으로 푸는 세 경우(서로 다른 실근, 복소근, 중근), 기본 행렬과 행렬 지수를 구하는 방법, 비동차식의 매개변수 변환, trace와 determinant로 평형점을 분류하는 표, 비선형계의 선형화를 한곳에 모은 공식집.
---

> [!abstract] 한눈에
> $X' = AX$의 해는 $A$의 고윳값과 고유벡터로 만든 $e^{\lambda t}v$ 꼴 해들의 선형결합이다. 고윳값이 복소수이면 실수부와 허수부를 떼어 실수 해 두 개를 만들고, 고유벡터가 모자라면 일반화 고유벡터로 $t$를 곱한 해를 더한다. 원점의 평형점은 $A$의 trace와 determinant만으로 안장점, 마디점, 나선점, 중심으로 나뉜다.

## 고계 식을 연립식으로

$n$계 선형식은 $x_1 = y$, $x_2 = y'$, …, $x_n = y^{(n-1)}$로 두면 1계 연립식이 된다. 예를 들어 $y'' + 3y' + 2y = g(t)$는

$$
X' = \begin{bmatrix}0 & 1\\ -2 & -3\end{bmatrix}X + \begin{bmatrix}0\\ g(t)\end{bmatrix}
$$

이다. 이 행렬의 고윳값 $-1$, $-2$는 원래 식의 특성근과 같다.

## 고윳값 방법

$X = ve^{\lambda t}$를 $X' = AX$에 넣으면 $Av = \lambda v$를 얻는다. $\det(A - \lambda I) = 0$으로 고윳값을, $(A - \lambda I)v = 0$으로 고유벡터를 구한다.

| 고윳값 | 해 |
| --- | --- |
| 서로 다른 실수 $\lambda_1$, $\lambda_2$ | $c_1v_1e^{\lambda_1t} + c_2v_2e^{\lambda_2t}$ |
| 복소수 $\alpha \pm i\beta$, $v = a + ib$ | $c_1e^{\alpha t}(a\cos\beta t - b\sin\beta t) + c_2e^{\alpha t}(b\cos\beta t + a\sin\beta t)$ |
| 중근 $\lambda$, 고유벡터 둘 | $(c_1v_1 + c_2v_2)e^{\lambda t}$ |
| 중근 $\lambda$, 고유벡터 하나 | $c_1ve^{\lambda t} + c_2(vt + p)e^{\lambda t}$, $(A - \lambda I)p = v$ |

복소수 경우는 $\lambda = \alpha + i\beta$ 쪽의 고유벡터 $v = a + ib$로 만든 복소 해 $ve^{\lambda t}$의 실수부와 허수부다.

세 예는 직접 계산했다.

- $A = \begin{bmatrix}1 & 3\\ 3 & 1\end{bmatrix}$: 고윳값 4, $-2$와 고유벡터 $(1, 1)$, $(-1, 1)$에서 $X = c_1(1,1)^Te^{4t} + c_2(-1,1)^Te^{-2t}$다.
- $A = \begin{bmatrix}-1 & 2\\ -2 & -1\end{bmatrix}$: 고윳값 $-1 \pm 2i$이고, $X = e^{-t}(\cos 2t, -\sin 2t)^T$와 $X = e^{-t}(\sin 2t, \cos 2t)^T$가 실수 해다.
- $A = \begin{bmatrix}3 & 1\\ 0 & 3\end{bmatrix}$: 중근 3에 고유벡터는 $v = (1, 0)$ 하나다. $(A - 3I)p = v$의 $p = (0, 1)$로 둘째 해 $(vt + p)e^{3t} = (t, 1)^Te^{3t}$를 만든다.

## 기본 행렬과 행렬 지수

독립인 해 $n$개를 열로 늘어놓은 행렬 $\Phi(t)$를 기본 행렬이라 하고, 일반해는 $X = \Phi(t)C$다. $\Phi(0) = I$가 되도록 고른 기본 행렬이 행렬 지수 $e^{At}$이고, 초기값 문제의 해는 $X(t) = e^{At}X(0)$이다.

$e^{At}$를 구하는 방법은 셋이다.

1. 대각화: $A = PDP^{-1}$이면 $e^{At} = Pe^{Dt}P^{-1}$, $e^{Dt}$는 대각 원소 $e^{\lambda_it}$.
2. 라플라스 변환: $e^{At} = \mathcal L^{-1}\{(sI - A)^{-1}\}$.
3. 기본 행렬: $e^{At} = \Phi(t)\Phi(0)^{-1}$.

위의 $A = \begin{bmatrix}0 & 1\\ -2 & -3\end{bmatrix}$이면 $(sI - A)^{-1} = \dfrac{1}{(s+1)(s+2)}\begin{bmatrix}s + 3 & 1\\ -2 & s\end{bmatrix}$이고, 원소마다 부분분수로 역변환하면

$$
e^{At} = \begin{bmatrix}2e^{-t} - e^{-2t} & e^{-t} - e^{-2t}\\ -2e^{-t} + 2e^{-2t} & -e^{-t} + 2e^{-2t}\end{bmatrix}
$$

다(직접 계산한 예). $t = 0$에서 단위 행렬이 되는지로 검산한다.

## 비동차식

$X' = AX + F(t)$의 해는 매개변수 변환으로

$$
X(t) = \Phi(t)C + \Phi(t)\int\Phi^{-1}(t)F(t)\,dt
$$

이고, 행렬 지수로 쓰면 $X(t) = e^{At}X(0) + \int_0^t e^{A(t-\tau)}F(\tau)\,d\tau$다. 둘째 항은 입력과 $e^{At}$의 합성곱이다. $F$가 상수나 지수 꼴이면 미정계수법처럼 같은 꼴의 상수 벡터 후보를 넣어도 된다.

## 평형점의 분류

$2\times2$ 행렬에서 $\tau = \operatorname{tr}A$, $\Delta = \det A$로 두면 고윳값은 $\lambda^2 - \tau\lambda + \Delta = 0$의 근이다. 따라서 $\tau$, $\Delta$와 판별식 $\tau^2 - 4\Delta$만으로 원점의 성격이 정해진다.

| 조건 | 고윳값 | 평형점 | 안정성 |
| --- | --- | --- | --- |
| $\Delta < 0$ | 부호가 다른 실수 | 안장점 | 불안정 |
| $\Delta > 0$, $\tau^2 - 4\Delta > 0$ | 부호가 같은 실수 | 마디점 | $\tau < 0$이면 안정, $\tau > 0$이면 불안정 |
| $\Delta > 0$, $\tau^2 - 4\Delta = 0$ | 실수 중근 | 퇴화 마디점 또는 별 모양 마디점 | $\tau$의 부호로 정함 |
| $\Delta > 0$, $\tau^2 - 4\Delta < 0$, $\tau \ne 0$ | 실수부가 0이 아닌 복소수 | 나선점 | $\tau < 0$이면 안정, $\tau > 0$이면 불안정 |
| $\Delta > 0$, $\tau = 0$ | 순허수 | 중심 | 안정이지만 점근 안정은 아님 |
| $\Delta = 0$ | 0인 고윳값 포함 | 평형점이 직선 위에 늘어섬 | 다른 고윳값으로 판정 |

![[../../images/linear-systems-ode/phase-portraits.png]]
*그림 1. 행렬 넷의 위상 초상. 왼쪽부터 $\begin{bmatrix}1&3\\3&1\end{bmatrix}$, $\begin{bmatrix}-3&1\\1&-3\end{bmatrix}$, $\begin{bmatrix}-1&2\\-2&-1\end{bmatrix}$, $\begin{bmatrix}0&2\\-2&0\end{bmatrix}$이다. 중심은 보존량 $x^2 + y^2$의 등고선과 방향 화살표로 그렸다. 직접 계산했다.*

## 비선형계의 선형화

$X' = F(X)$의 평형점 $X^*$($F(X^*) = 0$) 근처에서는 Jacobian $J = \partial F/\partial X\,\big|_{X^*}$로 $U' = JU$($U = X - X^*$)를 본다. $J$의 고윳값 실수부가 모두 0이 아니면 선형화의 분류(안장점, 마디점, 나선점)가 평형점 근처의 원래 흐름에도 그대로 맞는다.

선형화가 중심이나 0인 고윳값을 주면 원래 계는 중심일 수도, 느린 나선일 수도 있다. 이때는 보존량이나 Lyapunov 함수 같은 다른 방법으로 판정한다.

## 유의점

- 복소 고윳값에서는 켤레 쌍 가운데 하나만 써서 실수 해 두 개를 만든다. 두 켤레를 모두 쓰면 같은 해를 두 번 세게 된다.
- 고유벡터가 모자란 중근에서 $te^{\lambda t}v$만 더하면 해가 되지 않는다. $(A - \lambda I)p = v$의 $p$를 함께 더해야 한다.
- 중심은 선형계에서도 점근 안정이 아니다. 궤도는 원점으로 다가가지 않고 같은 닫힌 곡선을 돈다.
- 위상 초상은 상수계수 동차식의 평형점 근처 모양이다. 비선형계 전체의 흐름은 평형점마다 선형화해 이어 본다.

## 관련 개념

- [[linear-second-order-ode|2계 선형 미분방정식 공식집]]
- [[laplace-transform-table|라플라스 변환 공식표]]
- [[eigenvalues-diagonalization|고윳값과 대각화]]
- [[second-order-systems-numerics|고계 선형식·연립계·수치해]]

## 참고 자료

- Dennis G. Zill, _Advanced Engineering Mathematics_, Ch. 10 (Systems of Linear Differential Equations), Ch. 11 (Systems of Nonlinear Differential Equations).
- 예의 해와 행렬 지수는 직접 계산했고, 원식에 대입해 확인했다.
