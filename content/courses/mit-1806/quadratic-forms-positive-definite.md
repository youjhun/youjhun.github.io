---
title: 이차형식과 양의 정부호
aliases: [quadratic form, positive definite, 양의 정부호]
tags: [선형대수, 18.06]
date: 2026-10-20
description: xᵀAx가 만드는 곡면을 고윳값, 최적화, 공분산과 연결한다.
---

> [!abstract] 한눈에
> 이차형식 $x^TAx$는 방향에 따라 달라지는 곡률과 에너지를 표현한다. 모든 $x\ne0$에서 양수이면 $A$는 양의 정부호이며, 대칭행렬에서는 모든 고윳값이 양수라는 조건과 같다.

## 행렬이 만드는 이차식

대칭행렬

$$
A=\begin{bmatrix}a&b\\b&c\end{bmatrix}
$$

에 대해

$$
x^TAx=ax_1^2+2bx_1x_2+cx_2^2
$$

이다. 비대칭행렬도 $x^TAx$에서는 대칭 부분 $(A+A^T)/2$만 남으므로 이차형식은 대칭행렬로 다뤄도 된다.

## 고유좌표계에서 교차항 지우기

$A=Q\Lambda Q^T$이고 $z=Q^Tx$라면

$$
x^TAx=z^T\Lambda z=\sum_i \lambda_i z_i^2
$$

가 된다. 원래 좌표의 교차항은 고유벡터 방향으로 회전하면 사라진다. 각 고윳값이 그 방향의 곡률을 정한다.

- 모든 $\lambda_i>0$: 양의 정부호, 그릇 모양
- 모든 $\lambda_i\ge0$: 양의 준정부호, 평평한 방향이 있을 수 있음
- 양수와 음수가 섞임: 부정부호, 안장 모양

## 최적화와 최소제곱

$$
f(x)=\frac12x^TAx-b^Tx
$$

의 그래디언트는 대칭 $A$에 대해 $\nabla f=Ax-b$다. $A$가 양의 정부호이면 해 $x=A^{-1}b$는 유일한 전역 최소점이다. 가장 작은 고윳값과 가장 큰 고윳값의 비는 경사하강법이 어느 방향에서 느리게 움직이는지와 연결된다.

[[least-squares|최소제곱]]의 목적함수 $\|Ax-b\|^2$의 헤시안은 $2A^TA$다. $A$의 열이 독립이면 $A^TA$가 양의 정부호가 되어 해가 유일하다.

## 공분산과 거리

공분산 행렬 $\Sigma$는 양의 준정부호다. 임의의 $x$에 대해

$$
x^T\Sigma x=\operatorname{Var}(x^TX)\ge0
$$

이기 때문이다. $\Sigma^{-1}$가 존재하면 $(x-\mu)^T\Sigma^{-1}(x-\mu)$는 분산이 큰 방향의 차이는 작게, 분산이 작은 방향의 차이는 크게 보는 마할라노비스 거리의 제곱이 된다.

## 출처

- 개인 학습 기록, Notion `Studies / LAIDD / Linear Algebra`, Symmetric Matrices, Quadratic Forms, Positive Definiteness
- MIT OpenCourseWare, [18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
