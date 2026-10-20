---
title: 절점해석과 Thevenin 등가
aliases: [node voltage, Thevenin equivalent, superposition]
tags: [BiS252, 회로]
date: 2026-10-20
description: KCL로 회로의 절점 전압을 구하고 복잡한 선형 네트워크를 하나의 전압원과 저항으로 줄인다.
---

## 절점 전압법

기준 절점을 하나 정하고 나머지 절점 전압을 미지수로 둔다. 각 절점에서 Kirchhoff 전류법칙을 적용한다.

$$
\sum_k \frac{V_i-V_k}{R_{ik}}=I_i
$$

전류 방향을 일관되게 정하면 회로가 커져도 선형 연립방정식으로 정리된다. 전압원이 두 비기준 절점 사이에 있으면 두 절점을 supernode로 묶고 전압 제약식을 추가한다.

## 중첩 원리

선형 회로에서는 독립 전원을 하나씩 켠 응답을 더할 수 있다. 이상 전압원을 끌 때는 단락, 이상 전류원을 끌 때는 개방으로 바꾼다. 종속 전원은 회로의 선형 관계를 구성하므로 끄지 않는다.

전압과 전류는 중첩되지만 전력은 제곱에 비례하므로 각 전원의 전력을 따로 계산해 더할 수 없다.

## Thevenin 등가

두 단자에서 본 선형 회로는 이상 전압원 $V_{th}$와 직렬 저항 $R_{th}$로 바꿀 수 있다.

- $V_{th}$: 단자를 열어 둔 개방회로 전압
- $R_{th}$: 독립 전원을 끈 뒤 단자에서 본 등가저항, 또는 $V_{oc}/I_{sc}$

센서를 Thevenin 등가로 보면 측정기 입력저항이 센서 신호를 얼마나 로딩하는지 계산할 수 있다. 입력저항이 충분히 크지 않으면 측정 자체가 원래 전압을 바꾼다.

## 출처

- 개인 학습 기록, Notion `Studies / 2024 Fall / BiS252`, Resistive Circuits, Node Voltage, Thevenin, Superposition
