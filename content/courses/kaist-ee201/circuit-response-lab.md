---
title: 회로 실습 — OP-AMP 피드백과 정전류 RC
tags: [EE201, BiS252, 회로]
date: 2026-11-26
description: 출력 교란, Bode 선도, 정전류의 분배와 초기 상승률을 그래프에서 비교한다.
---

출력에서 생긴 교란이 어떻게 줄어드는지 살펴보고, 같은 단일 극점 모델을 Bode 선도에서 확인한다. 이어서 독립 정전류원으로 병렬 RC를 충전하며 저항과 커패시터가 전류를 어떻게 나누는지 비교한다.

- [비반전 OP-AMP와 출력 교란](#feedback)
- [이득과 대역폭](#bode)
- [정전류 병렬 RC](#charging)
- [시정수와 초기 상승률](#slope)

기초 개념은 [[op-amp-biosignal-front-end|연산증폭기와 생체신호 앞단]]과 [[first-order-rc-rl|RC·RL 1차 회로]]에서 확인할 수 있다.
