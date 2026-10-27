---
title: 재귀 알고리즘과 점화식
aliases: [Recurrence Relation, Recursive Algorithm, Master Theorem]
tags: [CS204, 이산수학, 알고리즘]
date: 2026-10-21
description: 재귀 호출의 비용을 점화식으로 세우고 전개·특성방정식·분할정복 형태로 푸는 법.
---

## 코드에서 점화식으로

입력 크기 $n$을 더 작은 문제로 나누는 재귀 알고리즘은 실행시간도 재귀식으로 쓸 수 있다. binary search는

$$T(n)=T(n/2)+\Theta(1)=\Theta(\log n)$$

이고 merge sort는

$$T(n)=2T(n/2)+\Theta(n)=\Theta(n\log n)$$

이다. base case 비용과 floor/ceiling은 정확한 식에 필요하지만 점근 차수에는 영향을 주지 않는 경우가 많다.

## 푸는 세 가지 방법

- 반복 전개: 재귀식을 여러 번 대입해 패턴과 종료 깊이를 찾는다.
- recursion tree: 각 레벨 비용과 레벨 수를 합한다.
- 특성방정식: 선형 동차 점화식에 $a_n=r^n$을 대입한다.

Master theorem은 $T(n)=aT(n/b)+f(n)$에서 재귀 하위문제 총량 $n^{\log_ba}$와 결합비용 $f(n)$의 성장률을 비교한다. 조건에 맞지 않는 점화식에 기계적으로 적용하면 안 된다.

## 종료와 정확성

재귀 알고리즘은 매 호출에서 well-founded measure가 감소하고 base case에 도달해야 한다. 실행시간을 구하기 전에 종료성을 확인한다. 정확성은 base case와 recursive call의 정확성을 가정하는 구조적 귀납으로 증명할 수 있다.

## 근거

Google Drive `CS204 / Lecture Note / Recursive Algorithms and Recurrence Relations` 범위를 공개 개념으로 재구성했다.
