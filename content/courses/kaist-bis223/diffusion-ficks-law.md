---
title: 확산과 Fick 법칙
aliases: [Fick's law, diffusion, Einstein-Smoluchowski]
tags: [BiS223, 물질전달, 확산]
date: 2026-10-20
description: 농도 기울기에서 flux를 만들고 확산 시간척도와 마찰의 관계를 생명공학 문제에 적용한다.
---

> [!abstract] 한눈에
> 확산은 개별 입자의 무작위 운동이 집단 수준에서 농도 기울기를 평탄하게 만드는 과정이다. Fick 제1법칙은 flux와 농도 기울기를, 제2법칙은 농도가 시간에 따라 바뀌는 속도를 연결한다.

## Fick 제1법칙

한 방향에서 확산 flux $J$는

$$
J=-D\frac{\partial c}{\partial x}
$$

다. $c$는 농도, $D$는 확산계수다. 음수 부호는 입자가 높은 농도에서 낮은 농도로 이동한다는 뜻이다. $J$의 단위는 면적과 시간당 물질량이므로 식의 각 항 단위를 확인하면 부호와 계수를 검산하기 쉽다.

정상상태에서는 위치별 농도는 다를 수 있어도 시간에 따라 더 변하지 않는다. ‘평형’은 순 구동력이 없는 더 강한 조건이므로 정상상태와 같은 말이 아니다.

## 보존법칙과 Fick 제2법칙

들어오는 양과 나가는 양의 차이가 국소 농도를 바꾼다는 연속방정식에 제1법칙을 넣으면, 일정한 $D$에서

$$
\frac{\partial c}{\partial t}=D\frac{\partial^2c}{\partial x^2}
$$

가 된다. 확산으로 거리 $L$을 건너는 대표 시간은 대략

$$
t\sim\frac{L^2}{D}
$$

다. 거리가 두 배가 되면 시간은 약 네 배다. 작은 세포 안에서는 확산이 유용하지만 큰 조직에서 장거리 운반을 확산만으로 해결하기 어려운 이유다.

## 확산과 마찰

열적 요동이 만드는 확산과 유체가 입자 운동을 방해하는 마찰은 Einstein-Smoluchowski 관계로 연결된다.

$$
D=\frac{k_BT}{\zeta}
$$

$\zeta$는 마찰계수다. 온도가 높을수록 확산이 커지고, 입자가 크거나 점성이 커져 마찰이 증가하면 확산이 작아진다. 이는 미시적 무작위 운동과 거시적 수송계수를 잇는 예다.

## 출처

- 개인 학습 기록, Notion `Studies / 2024 Spring / BiS223 / Lecture Note / 2024 03 06 - Fick’s Law`
- K. A. Dill and S. Bromberg, _Molecular Driving Forces_, 2nd ed.
