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

고윳값은 변환의 ‘크기’ 하나가 아니다. 각 고유방향에서 늘어나는 비율이다. 음수면 방향이 뒤집히고, 복소수면 회전과 스케일링이 함께 나타날 수 있다.

## 대각화가 주는 계산 이득

고유벡터를 열로 모은 $S=[v_1\ \cdots\ v_n]$, 고윳값을 대각에 놓은 $\Lambda$를 만들면

$$
AS=S\Lambda,\qquad A=S\Lambda S^{-1}
$$

이다. 따라서

$$
A^k=S\Lambda^kS^{-1}
$$

가 된다. 대각행렬의 거듭제곱은 각 대각원소를 $k$제곱하면 끝이다. 이산 동역학 $x_{k+1}=Ax_k$의 장기 거동도 $|\lambda|$가 가장 큰 모드가 지배한다.

## 언제 대각화되지 않는가

$n\times n$ 행렬에 선형독립인 고유벡터가 $n$개 있어야 한다. 고윳값이 중복되었다고 항상 실패하는 것은 아니다. 각 중복 고윳값의 고유공간 차원이 충분해야 한다.

실수 대칭행렬은 특별하다. 고윳값이 모두 실수이고 서로 직교하는 고유벡터를 택할 수 있어

$$
A=Q\Lambda Q^T
$$

로 분해된다. 역행렬 대신 전치행렬을 쓰므로 수치적으로도 해석하기 쉽다. [[covariance-matrix|공분산 행렬]]과 [[quadratic-forms-positive-definite|이차형식]]에서 이 구조가 반복된다.

## SVD와의 차이

고유분해는 정방행렬 $A$ 자체의 방향을 찾는다. [[svd|SVD]]는 직사각행렬에도 존재하며 $A^TA$와 $AA^T$의 고유구조를 이용해 입력 공간과 출력 공간의 직교축을 따로 찾는다. 대각화가 불가능한 정방행렬도 SVD는 가능하다.

## 출처

- 개인 학습 기록, Notion `Studies / LAIDD / Linear Algebra`, Eigenvalues and Eigenvectors, Diagonalization
- MIT OpenCourseWare, [18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
