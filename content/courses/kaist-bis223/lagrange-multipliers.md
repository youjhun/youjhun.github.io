---
title: 라그랑주 승수법
aliases: [constrained optimization]
tags: [BiS223, 최적화]
date: 2026-10-20
description: 등식 제약이 있는 최적화에서 목적함수와 제약식의 기울기를 맞추는 이유.
---

> [!abstract] 한눈에
> $g(x)=c$ 위에서 $f(x)$를 최적화할 때, 움직일 수 있는 모든 접선 방향으로 $f$가 더 이상 변하지 않는 점에서는 $\nabla f$가 $\nabla g$와 평행하다. 따라서 $\nabla f=\lambda\nabla g$를 푼다.

## 기하학적 이유

제약곡면 $g(x)=c$의 법선벡터는 $\nabla g$다. 제약을 지키며 움직일 수 있는 방향은 이 벡터에 수직인 접선 방향들이다. 최적점에서는 그 접선 방향으로 목적함수 $f$의 변화율이 모두 0이어야 한다. 따라서 $\nabla f$도 같은 법선 방향에 놓인다.

$$
\nabla f(x^*)=\lambda\nabla g(x^*),\qquad g(x^*)=c
$$

라그랑지안을

$$
\mathcal L(x,\lambda)=f(x)-\lambda(g(x)-c)
$$

로 두면 $\nabla_x\mathcal L=0$과 $\partial\mathcal L/\partial\lambda=0$을 함께 푸는 것과 같다.

## 예: 정해진 합에서 곱 최대화

$x+y=s$, $x,y>0$일 때 $xy$를 최대화하자.

$$
f(x,y)=xy,\qquad g(x,y)=x+y=s
$$

$\nabla f=(y,x)$, $\nabla g=(1,1)$이므로 $y=\lambda$, $x=\lambda$다. 따라서 $x=y=s/2$에서 곱이 최대다. 제약을 먼저 $y=s-x$로 대입해 풀 수도 있지만, 변수와 제약이 많아지면 승수법이 구조를 더 잘 보존한다.

## 승수의 의미

$\lambda$는 제약값 $c$를 조금 바꿀 때 최적 목적값이 얼마나 변하는지를 나타내는 민감도로 해석할 수 있다. 물리학에서는 보존 제약 아래 에너지 최소화, 통계역학에서는 정규화나 평균 에너지 제약 아래 엔트로피 최대화에 나타난다.

후보점을 찾았다고 최대·최소가 정해지지는 않는다. 후보점은 최대도 최소도 아닐 수 있다. 경계, 특이점, 여러 후보와 2차 조건을 따로 확인해야 한다.

## 출처

- 개인 학습 기록, Notion `Studies / 2024 Spring / BiS223 / Lagrange multipliers`
