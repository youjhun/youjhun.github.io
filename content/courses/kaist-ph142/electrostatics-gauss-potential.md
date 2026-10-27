---
title: 전기장·Gauss 법칙·전위
aliases: [Electric Field, Gauss Law, Electric Potential]
tags: [PH142, 전자기학]
date: 2026-10-21
description: Coulomb 힘을 장과 flux, scalar potential로 바꾸어 대칭적인 전하분포를 푸는 법.
---

## 힘에서 장으로

점전하 $q$가 만드는 전기장은

$$\mathbf E=\frac{1}{4\pi\epsilon_0}\frac{q}{r^2}\hat{\mathbf r}$$

이고 여러 전하의 장은 vector superposition으로 더한다. 연속 분포에서는 $dq$에 대해 적분한다. 시험전하가 없어도 공간에 정의되는 $\mathbf E$를 먼저 구하면 어떤 전하의 힘도 $\mathbf F=q\mathbf E$로 얻는다.

## Gauss 법칙

$$\oint_S\mathbf E\cdot d\mathbf A=\frac{Q_{enc}}{\epsilon_0}$$

는 닫힌 면을 통과하는 flux와 내부 총전하를 연결한다. 법칙은 항상 맞지만, $E$를 적분 밖으로 꺼낼 만큼 구면·원통·평면 대칭이 있을 때 계산 도구로 특히 강하다. Gaussian surface 밖의 전하도 국소 전기장에는 기여하지만 net flux에는 총합이 0이 된다.

## 전위

정전기장은 보존장이므로

$$V(B)-V(A)=-\int_A^B\mathbf E\cdot d\mathbf l,\qquad \mathbf E=-\nabla V$$

이다. 전위는 scalar라 여러 전하의 기여를 단순 합할 수 있다. 전기력선은 등전위면에 수직이고 conductor의 정전평형에서는 내부 $E=0$, 표면은 등전위다.

## 연결

- [[courses/kaist-bis223/electrostatics-screening|생체분자의 정전기 상호작용과 차폐]]
- [[capacitance-current-circuits|축전기·전류·직류회로]]

## 근거

Google Drive `일반물리학II`의 Ch.20–23 범위와 Notion PH142 강의 기록을 토대로 구성했다.
