---
title: 자기장·전자기유도·교류
aliases: [Magnetism, Faraday Law, Induction, AC]
tags: [PH142, 전자기학]
date: 2026-10-21
description: 움직이는 전하의 자기력, 전류가 만드는 장, Faraday–Lenz 법칙과 AC 회로의 위상.
---

## 자기력과 자기장

$$\mathbf F=q\mathbf v\times\mathbf B$$

이므로 자기력은 속도에 수직이고 한 입자에 일을 하지 않는다. 전류가 흐르는 도선은 $d\mathbf F=I\,d\mathbf l\times\mathbf B$를 받는다. Biot–Savart와 Ampère 법칙은 전류 분포가 만드는 $\mathbf B$를 구한다.

## Faraday–Lenz 법칙

$$\mathcal E=-\frac{d\Phi_B}{dt}$$

자속의 시간변화가 유도기전력을 만든다. 음의 부호는 유도전류가 자속 변화를 방해하는 방향이라는 Lenz 법칙이다. 에너지 보존이 방향 규칙으로 나타난 것이다. 자체유도에서 $V_L=L\,dI/dt$이며 inductor 전류는 순간적으로 뛰지 않는다.

## LC·RLC와 에너지 교환

inductor의 에너지 $U_L=LI^2/2$와 capacitor의 에너지 $U_C=CV^2/2$가 오가며 진동한다. 저항은 에너지를 열로 소모한다. 구동주파수가 고유주파수에 가까우면 resonance가 나타나며 damping이 응답 폭을 정한다.

## 교류와 phasor

sinusoidal steady state에서 $Z_R=R$, $Z_L=j\omega L$, $Z_C=1/(j\omega C)$다. phasor로 미분방정식을 복소수 대수로 바꿀 수 있다. 평균전력은 voltage와 current의 위상차에 의존한다.

## 근거

Google Drive `일반물리학II`의 Ch.26–30 범위와 Notion PH142 기록을 바탕으로 작성했다.
