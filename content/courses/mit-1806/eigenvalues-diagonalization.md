---
title: 고윳값·고유벡터와 대각화
aliases: [eigenvalue, eigenvector, diagonalization]
tags: [선형대수, 18.06]
date: 2026-10-20
description: 선형변환이 방향은 보존하고 크기만 바꾸는 축을 찾고 반복 변환을 단순화한다.
---

> [!abstract] 한눈에
> $Av=\lambda v$를 만족하는 고유벡터 $v$는 변환 뒤에도 방향이 바뀌지 않는다. 독립인 고유벡터가 충분하면 $A=S\Lambda S^{-1}$로 대각화되어 반복 변환과 동역학을 각 축의 스케일링으로 나눠 볼 수 있다.

## 고유방향을 찾는 식

$$
Av=\lambda v,\qquad v\ne0
$$

를 옮기면 $(A-\lambda I)v=0$이다. 0이 아닌 해가 있으려면 $A-\lambda I$가 가역이 아니어야 하므로

$$
\det(A-\lambda I)=0
$$

을 푼다. 나온 $\lambda$마다 $A-\lambda I$의 영공간을 구하면 고유벡터가 된다.

고윳값은 변환 전체의 크기 하나가 아니라 각 고유방향에서 늘어나는 비율이다. 음수면 방향이 뒤집히고, 복소수면 회전과 스케일링이 함께 나타날 수 있다.

## 대각화가 주는 계산 이득

고유벡터를 열로 모은 $S=[v_1\ \cdots\ v_n]$, 고윳값을 대각에 놓은 $\Lambda$를 만들면

$$
AS=S\Lambda,\qquad A=S\Lambda S^{-1}
$$

이다. 따라서

$$
A^k=S\Lambda^kS^{-1}
$$

가 된다. 대각행렬의 거듭제곱은 각 대각원소를 $k$제곱해 얻는다. 이산 동역학 $x_{k+1}=Ax_k$의 장기 거동도 $|\lambda|$가 가장 큰 모드가 지배한다.

## 대각화 조건

$n\times n$ 행렬에 선형독립인 고유벡터가 $n$개 있어야 한다. 고윳값이 중복되었다고 항상 실패하는 것은 아니다. 각 중복 고윳값의 고유공간 차원이 충분해야 한다.

실수 대칭행렬은 고윳값이 모두 실수이고 서로 직교하는 고유벡터를 택할 수 있어

$$
A=Q\Lambda Q^T
$$

로 분해된다. 역행렬 대신 전치행렬을 쓰므로 수치적으로도 해석하기 쉽다. [[covariance-matrix|공분산 행렬]]과 [[quadratic-forms-positive-definite|이차형식]]에서 이 구조가 반복된다.

## SVD와의 차이

고유분해는 정방행렬 $A$ 자체의 방향을 찾는다. [[svd|SVD]]는 직사각행렬에도 존재하며 $A^TA$와 $AA^T$의 고유구조를 이용해 입력 공간과 출력 공간의 직교축을 따로 찾는다. 대각화가 불가능한 정방행렬도 SVD는 가능하다.

## Markov 행렬의 계산

확률벡터를 열로 쓰면 $p_{k+1}=Pp_k$이고 각 열의 합이 1인 비음수 P를 사용한다. 행벡터 규약의 행합 조건과 섞지 않는다. 새 예

$$
P=\begin{bmatrix}0.8&0.3\\0.2&0.7\end{bmatrix}
$$

의 고윳값은 1과 0.5다. 정상분포는 $P\pi=\pi$, $\pi_1+\pi_2=1$에서 π=(0.6,0.4)ᵀ다. p₀=(1,0)ᵀ이면 $p_k=\pi+0.4(0.5)^k(1,-1)^T$다. p₁=(0.8,0.2)로 직접 곱과 맞는다. 비정상 모드가 감쇠한다는 것을 계산으로 볼 수 있다.

확률행렬이 존재한다고 모든 초기값이 하나의 정상분포로 수렴하는 것은 아니다. 닫힌 클래스가 여러 개면 정상분포가 여러 개일 수 있고 주기적이면 진동할 수 있다. 유한 irreducible·aperiodic 체인 등의 수렴 조건을 확인한다.

## 연속시간 동역학

$\dot x=Ax$는 $x(t)=e^{At}x(0)$이고 대각화되면 $e^{At}=S\operatorname{diag}(e^{\lambda_it})S^{-1}$다. 이산 반복은 |λ|<1, 연속계 감쇠는 Re λ<0을 기준으로 삼는다. 위 P를 그대로 미분방정식의 A로 쓰면 λ=1 모드가 $e^t$로 커져 확률의 합을 보존하지 않는다. 연속시간 Markov 생성자는 열벡터 규약에서 열합이 0이어야 한다.

## 유의점

- 고유벡터는 0벡터가 아니며 상수배의 선택이 가능하다.
- 대각화의 S는 일반적으로 직교행렬이 아니다.
- 중근이 있어도 고유공간 차원이 충분하면 대각화가 가능하다.

## 관련 개념

- [[elimination-lu-qr|기저 변환과 닮음]]
- [[second-order-systems-numerics|연립 미분방정식]]

## 참고 자료

- 개인 학습 기록, Notion `Studies / LAIDD / Linear Algebra`, Eigenvalues and Eigenvectors, Diagonalization
- MIT OpenCourseWare, [18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
