---
title: 페이저·임피던스·교류전력
description: 정현파 정상상태를 복소수로 계산하고 RMS와 복소전력을 구분한다.
date: 2026-10-25
tags: [EE201, 회로, 보충]
---

> [!abstract] 한눈에
> 같은 주파수의 선형 회로에서는 정현파의 미분을 $j\omega$ 곱셈으로 바꾸어 절점해석과 전압분배를 사용할 수 있다. 이 계산은 과도응답이 사라진 정상상태를 구한다. 전력 계산에서는 peak와 RMS convention을 일관되게 사용한다.

## 페이저 convention

이 글에서는 RMS 페이저 $\widetilde V=V_{rms}e^{j\phi}$와 시간신호 $v(t)=\sqrt2\operatorname{Re}[\widetilde Ve^{j\omega t}]$를 사용한다. 예를 들어 $v(t)=10\cos(\omega t+30^\circ)$ V이면 $\widetilde V=(10/\sqrt2)\angle30^\circ$ V다. Peak 페이저를 쓰는 책에서는 전력식에 $1/2$가 들어간다.

$$
Z_R=R,\qquad Z_L=j\omega L,\qquad Z_C=\frac1{j\omega C}=-\frac{j}{\omega C}.
$$

이 식은 $v=Ldi/dt$, $i=Cdv/dt$에 정상 정현파를 넣어 얻는다. 복소수 위상은 cosine 기준으로 통일한다. $\sin\theta=\cos(\theta-90^\circ)$이므로 sine 입력의 위상을 변환하지 않고 혼합하면 오류가 난다.

## 계산 규칙

직렬 임피던스는 더하고 병렬 임피던스의 역수는 더한다. 전압분배는 $\widetilde V_o=\widetilde V_sZ_2/(Z_1+Z_2)$다. 절점해석에서는 저항의 conductance $1/R$ 대신 admittance $1/Z$를 쓴다. 더할 때는 직교형 $a+jb$, 곱하고 나눌 때는 극형 $r\angle\phi$가 편리하다.

서로 다른 주파수의 입력은 각 주파수에서 별도로 푼 후 시간영역으로 돌아와 더한다. 다른 주파수의 페이저를 단순 벡터 합으로 합치지 않는다. 초기조건 응답은 라플라스 또는 시간영역의 자연응답으로 별도 계산한다.

## RL 부하 예

새 예에서 $\widetilde V_s=10\angle0^\circ$ V RMS, $R=100$ Ω, $\omega=1000$ rad/s, $L=100$ mH이면 $Z=100+j100=141.42\angle45^\circ$ Ω다.

$$
\widetilde I=\frac{10}{100+j100}=0.05-j0.05
=0.07071\angle(-45^\circ)\quad\mathrm A.
$$

따라서 $i(t)=0.1\cos(1000t-45^\circ)$ A다. 전류의 peak 0.1 A와 RMS 0.07071 A를 구분한다. 전압이 전류보다 45° 앞서는 inductive 부하다.

## 평균전력과 복소전력

수동 부호 규약에서 RMS 페이저를 사용하면

$$
\mathcal S=\widetilde V\widetilde I^*=P+jQ,
\quad P=V_{rms}I_{rms}\cos\phi,
\quad Q=V_{rms}I_{rms}\sin\phi.
$$

$P$는 평균 유효전력 W, $Q$는 무효전력 var, $|\mathcal S|=V_{rms}I_{rms}$는 피상전력 VA다. $\phi=\phi_V-\phi_I$이고 역률은 $P/|\mathcal S|$다. 위 예에서 $\mathcal S=0.5+j0.5$ VA, $P=0.5$ W, $Q=0.5$ var, 역률은 약 0.707이다. $I_{rms}^2R=0.5$ W로도 검산된다.

이상 L과 C의 한 주기 평균 소비전력은 0이지만 에너지는 저장되었다가 반환된다. 저항에는 $P=I_{rms}^2R$를 쓴다. 복소전력에서 전류의 켤레를 빼면 위상차 대신 위상합이 되어 잘못된 값이 나온다.

## 적용 순서

주파수를 정하고 모든 신호를 같은 cosine·RMS 기준으로 바꾼다. 각 소자를 임피던스로 치환해 KCL/KVL을 푼다. 진폭·위상으로 시간신호를 복원하고, 전력에서는 전류 켤레와 수동 부호 규약을 확인한다. DC 극한과 고주파 극한, 저항 손실로 결과를 검산한다.

## 유의점

- $\omega=2\pi f$이고 Hz와 rad/s는 수치가 다르다.
- 한 주파수의 정상상태 페이저는 초기조건의 정보를 담지 않는다.
- 이 글은 교류 계산을 위한 보충이다. 현재 확인한 Notion EE201 Chapter 0–8의 단원별 수강 기록으로 간주하지 않는다.

## 관련 개념

- [[thevenin-node-analysis|절점해석]]
- [[first-order-rc-rl|RC 필터]]
- [[second-order-rlc|RLC 공진]]

## 참고 자료

- [MIT 6.002, Lecture 16–17: Sinusoidal Steady State; The Impedance Model](https://ocw.mit.edu/courses/6-002-circuits-and-electronics-spring-2007/pages/lecture-notes/).
- Engineering Circuit Analysis 및 Fundamentals of Electric Circuits의 정현파 정상상태·교류전력 단원. 수치는 직접 정한 회로 예다.
