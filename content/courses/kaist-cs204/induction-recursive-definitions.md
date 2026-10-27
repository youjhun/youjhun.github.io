---
title: 귀납법과 재귀적 정의
aliases: [Mathematical Induction, Structural Induction, Recursive Definition]
tags: [CS204, 이산수학, 귀납법]
date: 2026-10-21
description: 자연수 명제와 재귀적으로 만들어진 구조를 base·inductive step으로 증명하는 법.
---

## 수학적 귀납법

명제 $P(n)$을 모든 $n\ge n_0$에 대해 보이려면 base case $P(n_0)$를 확인하고, $P(k)$가 참이라고 가정한 뒤 $P(k+1)$을 증명한다. inductive hypothesis는 아직 증명되지 않은 것을 멋대로 가정하는 것이 아니라, 임의 한 단계에서 다음 단계로 넘어가는 함의를 보이기 위한 조건이다.

강한 귀납법은 $P(n_0),\dots,P(k)$ 전체를 가정해 $P(k+1)$을 보인다. 소인수분해처럼 다음 대상을 하나의 바로 전 사례가 아니라 더 작은 여러 사례로 줄일 때 자연스럽다.

## 재귀적 정의

집합이나 함수도 base object와 constructor로 정의할 수 있다. 문자열, 트리, 논리식과 자연수는 재귀적으로 만들어진다. 정의가 유효하려면 base가 있고, 각 생성 규칙이 이미 만들어진 대상으로부터 새 대상을 만들며, 불필요한 대상을 포함하지 않아야 한다.

## 구조적 귀납법

재귀적으로 정의된 모든 구조에 대한 성질은 구조적 귀납법으로 증명한다. base object에서 성질을 확인하고, 각 constructor의 자식 구조가 성질을 가진다고 가정해 새 구조도 가짐을 보인다. 트리 알고리즘의 정확성 증명과 syntax tree 해석에 직접 쓰인다.

## 흔한 빈틈

base case 누락, induction step에서 $P(k+1)$을 암묵적으로 사용하는 순환, $n_0$보다 작은 경계, 구조를 만드는 constructor 중 하나를 빠뜨리는 오류가 대표적이다.

## 근거

Google Drive `CS204 / Lecture Note`의 Proof by Induction, Recursive Definitions, Structural Induction 범위를 재구성했다.
