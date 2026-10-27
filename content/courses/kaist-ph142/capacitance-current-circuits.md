---
title: 축전기·전류·직류회로
aliases: [Capacitance, Electric Current, DC Circuit]
tags: [PH142, 회로]
date: 2026-10-21
description: 전기장 에너지의 저장, 전류와 저항, Kirchhoff 법칙과 RC 시간응답을 연결한다.
---

## 축전기

capacitance는 기하와 유전체가 정하는 $C=Q/V$다. 평행판 축전기에서 $C=\epsilon A/d$이고 저장 에너지는

$$U=\frac12CV^2=\frac{Q^2}{2C}$$

다. dielectric은 polarization으로 같은 전하에서 장과 전압을 낮춰 capacitance를 늘린다.

## 전류와 저항

$I=dQ/dt$, microscopic Ohm law는 $\mathbf J=\sigma\mathbf E$다. 저항성 소자에서 $V=IR$, 전력은 $P=IV=I^2R=V^2/R$이다. Ohm 법칙은 모든 소자의 보편 법칙이 아니라 특정 범위에서 선형인 재료·소자의 모델이다.

## Kirchhoff 법칙

KCL은 node에서 전하 보존, KVL은 lumped circuit에서 loop의 전위 변화 합이 0이라는 진술이다. 여러 loop에서는 기준 방향을 일관되게 두고 부호를 식에서 판단한다.

## RC 응답

충전에서

$$V_C(t)=V_s(1-e^{-t/RC})$$

이고 방전은 $V_C(t)=V_0e^{-t/RC}$다. capacitor 전압은 순간적으로 뛰지 않는다. $\tau=RC$는 최종값의 $1-e^{-1}$까지 가는 시간척도다.

## 근거

Google Drive `일반물리학II`의 Ch.23–25와 Notion PH142 기록 범위를 공개 설명으로 재구성했다.
