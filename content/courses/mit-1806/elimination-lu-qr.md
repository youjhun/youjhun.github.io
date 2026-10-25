---
title: 소거법·LU·행렬식·QR
description: 연립방정식의 해법과 기저 변환, 직교화, 수치 오차를 계산 예로 연결한다.
date: 2026-10-25
---

> [!abstract] 한눈에
> 소거법은 연립방정식을 상삼각 형태로 바꾸고 LU는 그 연산을 저장한다. 행렬식은 가역성과 부피 배율을 나타내지만 큰 시스템을 푸는 기본 알고리즘은 아니다. QR은 직교기저를 구성해 최소제곱을 안정적으로 계산하는 데 사용한다.

## 소거와 LU 계산

새 예 $A=\begin{bmatrix}2&1\\4&5\end{bmatrix}$, $b=(5,13)^T$에서 두 번째 행에서 첫 번째 행의 2배를 빼면

$$
U=\begin{bmatrix}2&1\\0&3\end{bmatrix},\quad
L=\begin{bmatrix}1&0\\2&1\end{bmatrix},\quad A=LU.
$$

$Ly=b$를 전진대입하면 y=(5,3), $Ux=y$를 후진대입하면 x=(2,1)이다. Ax=b에 대입해 (5,13)을 복원한다. 같은 A에 여러 b가 있으면 분해를 재사용할 수 있다. 0 또는 지나치게 작은 pivot이 있으면 행교환을 포함해 PA=LU로 쓴다. P가 b에도 작용해야 하므로 $Ly=Pb$를 푼다.

직접 역행렬을 만든 뒤 곱하는 방법보다 분해와 대입을 우선한다. 작은 residual $b-A\widehat x$만으로 참해 오차가 작다고 단정하지 않는다. 조건수가 큰 A는 작은 데이터 오차를 큰 해 오차로 증폭할 수 있다.

## 가역성과 행렬식

정사각 A에서 가역, 모든 열의 독립, rank=n, Null(A)={0}, det A≠0은 동치다. 행교환은 determinant 부호를 바꾸고 한 행에 다른 행의 배수를 더하는 소거는 determinant를 보존한다. 위 A는 det=2·5−4·1=6이며 U 대각곱도 6이다.

선형변환은 부피를 |det A|배로 바꾸고 determinant 부호는 방향 반전을 구분한다. 행렬 크기가 다르면 determinant 자체를 정의하지 않는다. 절대적으로 작은 determinant를 보편적인 수치적 특이성 기준으로 쓰지 않는다. 단위나 행렬 전체 배율만 바꾸어도 determinant 크기가 크게 바뀐다. 특잇값과 조건수를 함께 본다.

## Gram–Schmidt와 QR

$a_1=(1,1,0)^T$, $a_2=(1,0,1)^T$인 새 예에서

$$
q_1=\frac{(1,1,0)^T}{\sqrt2},\quad
u_2=a_2-q_1(q_1^Ta_2)=(1/2,-1/2,1)^T,
\quad q_2=\frac{(1,-1,2)^T}{\sqrt6}.
$$

따라서 Q=[q₁ q₂]이고

$$
R=\begin{bmatrix}\sqrt2&1/\sqrt2\\0&\sqrt{3/2}\end{bmatrix},
\quad A=QR,\quad Q^TQ=I_2.
$$

기저를 만들 때 이미 만든 모든 q 방향의 투영을 빼야 한다. 잔차가 0이면 새 열은 종속이므로 정규화하지 않는다. 유한정밀도 구현에서는 고전적 Gram–Schmidt의 직교성 손실에 주의하고 수정 Gram–Schmidt, Householder 또는 SVD를 선택한다.

## QR 최소제곱

Full column rank A의 얇은 QR에서 $\|Ax-b\|^2$를 최소화하면 $Rx=Q^Tb$를 푼다. 위 A와 새 b=(1,2,3)ᵀ에서는 $Q^Tb=(3/\sqrt2,5/\sqrt6)^T$이므로 x=(2/3,5/3)ᵀ다. 예측 Ax=(7/3,2/3,5/3)ᵀ이고 residual b−Ax=(−4/3,4/3,4/3)ᵀ이다. 두 열과의 내적은 모두 0이다.

정규방정식 $A^TAx=A^Tb$도 같은 정확해를 주지만 2-norm 조건수는 $\kappa_2(A^TA)=\kappa_2(A)^2$로 커질 수 있다. 나쁜 조건에서 QR과 SVD의 수치적 이점이 생긴다. 실제 계산에서는 역행렬을 명시적으로 구성하지 않고 선형 solver를 쓴다.

## 기저 변환과 닮음

새 기저 벡터를 열로 모은 가역행렬 B에 대해 원래 좌표는 x=Bz다. 같은 선형변환 A의 새 좌표 표현은 $A_{new}=B^{-1}AB$다. 닮음은 같은 변환을 다른 기저로 적는 관계이고, 고윳값·trace·determinant를 보존한다. 직교 B에서는 $B^{-1}=B^T$여서 좌표 변환이 길이와 각도를 보존한다. 일반 가역 B에 전치만 대입하지 않는다.

## 계산 순서

크기와 rank 조건을 확인한다. 정방 정확해는 pivoting을 포함한 분해로, 과결정 최소제곱은 QR 또는 SVD로 푼다. 분해 재구성 오차, residual, 직교성, 조건수를 요구 정밀도에 맞춰 확인한다.

## 유의점

- 행 기본변환 뒤 pivot 열의 위치로 원래 A의 독립 열을 고른다.
- 유리수·상징 계산의 정확한 0과 부동소수점의 작은 값을 같은 규칙으로 판정하지 않는다.
- QR의 Q 열 개수와 전체 공간의 차원을 구분한다.

## 관련 개념

- [[subspaces-rank|네 부분공간과 rank]]
- [[least-squares|최소제곱·직교투영]]
- [[svd|SVD와 조건수]]
- [[eigenvalues-diagonalization|고윳값과 닮음]]

## 참고 자료

- [MIT 18.06, Readings](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/pages/readings/), L2–5, L17–20, L33–34.
- Gilbert Strang, Introduction to Linear Algebra, 소거·직교화·행렬식·선형변환. 숫자는 별도 구성했다.
