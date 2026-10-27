---
title: 재귀·iterator·객체 설계를 연결하기
aliases: [Recursion, Iterator, OOP]
tags: [CS206, 자료구조, Java]
date: 2026-10-21
description: 자료구조의 표현을 감추면서 순회와 재귀 알고리즘을 안전하게 만드는 설계 원칙.
---

## ADT는 구현보다 계약이 먼저다

stack은 push/pop, queue는 enqueue/dequeue라는 동작 계약으로 정의된다. 배열이나 연결 리스트는 구현 선택이다. Java의 class와 interface는 사용자가 알아야 할 동작과 내부 표현을 분리하고, representation invariant는 객체가 항상 만족해야 하는 조건을 적는다.

## 재귀는 문제 크기를 줄이는 증명이다

재귀 함수에는 base case와 더 작은 입력으로 가는 recursive case가 필요하다. 트리 순회처럼 자료구조 자체가 재귀적일 때 자연스럽다. 호출마다 stack frame이 생기므로 깊이가 큰 연결 리스트나 편향 트리에서는 stack overflow가 날 수 있고 반복문으로 바꾸는 편이 안전할 수 있다.

재귀의 시간복잡도는 호출 수와 호출당 작업으로 구한다. 같은 부분문제를 반복하면 memoization이나 bottom-up 동적계획법을 고려한다.

## iterator는 순회 상태를 객체로 만든다

iterator는 자료구조 내부를 노출하지 않고 `hasNext`와 `next`로 원소를 한 번에 하나씩 제공한다. 배열은 index, 연결 리스트는 현재 node, 트리는 명시적 stack으로 순회 상태를 보관할 수 있다. collection과 iterator의 책임을 분리하면 여러 독립 순회를 동시에 만들 수 있다.

구조를 순회 중 수정할 때의 규칙도 계약에 포함되어야 한다. Java collection의 fail-fast 동작은 동시 수정의 모든 위험을 보증하는 동기화 기법이 아니라, 잘못된 사용을 빨리 발견하는 장치다.

## 연결

- [[data-structure-tradeoffs|자료구조를 고르는 기준]]
- [[stacks-queues-trees-heaps|스택·큐·트리·힙]]
