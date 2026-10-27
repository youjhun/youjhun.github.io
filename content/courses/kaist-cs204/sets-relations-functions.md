---
title: 집합·관계·함수
aliases: [Sets, Relations, Functions, Equivalence Relation, Partial Order]
tags: [CS204, 이산수학]
date: 2026-10-21
description: 원소의 모음에서 동치류와 부분순서, 일대일·전사 함수로 구조를 만드는 법.
---

## 집합의 연산

합집합, 교집합, 차집합과 여집합은 논리의 OR, AND, AND NOT에 대응한다. power set $\mathcal P(A)$는 $A$의 모든 부분집합을 모으며 $|A|=n$이면 $|\mathcal P(A)|=2^n$이다. Cartesian product $A\times B$는 순서쌍을 만들고 관계와 함수의 정의역이 된다.

## 관계

$A$ 위의 이항관계는 $A\times A$의 부분집합이다. reflexive, symmetric, antisymmetric, transitive 성질의 조합이 구조를 정한다.

- equivalence relation: reflexive + symmetric + transitive. 원소를 겹치지 않는 equivalence class로 분할한다.
- partial order: reflexive + antisymmetric + transitive. 모든 쌍을 비교할 필요는 없다.
- total order: partial order에 모든 서로 다른 두 원소의 비교가능성을 더한다.

Hasse diagram은 partial order에서 자명한 reflexive edge와 transitivity로 따라오는 edge를 생략해 cover relation만 그린다.

## 함수

함수 $f:A\to B$는 각 $a\in A$에 정확히 하나의 $b\in B$를 대응시키는 관계다. injective는 서로 다른 입력이 서로 다른 출력으로, surjective는 codomain의 모든 원소가 적어도 한 번 출력으로, bijective는 둘 다 만족한다. 역함수가 존재하는 정확한 조건은 bijection이다.

함수 합성은 결합법칙을 만족하지만 일반적으로 교환법칙은 만족하지 않는다. 정의역·공역과 실제 image를 구분해야 surjectivity를 올바르게 판단할 수 있다.

## 근거

Google Drive `CS204 / Lecture Note`의 Sets, Relations, Equivalence Relations, Order Relations, Functions 범위를 재구성했다.
