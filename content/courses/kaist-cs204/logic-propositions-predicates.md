---
title: 명제논리와 술어논리
aliases: [Propositional Logic, Predicate Logic, 명제논리, 술어논리]
tags: [CS204, 이산수학, 논리]
date: 2026-10-21
description: 문장을 명제와 술어로 형식화하고 진리표·양화사·자연연역으로 추론을 검사하는 법.
---

## 명제논리

명제는 참 또는 거짓이 정해지는 문장이다. $\neg,\land,\lor,\to,\leftrightarrow$로 복합명제를 만들고 진리표로 모든 truth assignment에서 값을 확인한다. 항상 참이면 tautology, 항상 거짓이면 contradiction, 경우에 따라 달라지면 contingency다.

$p\to q$는 $\neg p\lor q$와 동치다. converse $q\to p$와는 다르고, contrapositive $\neg q\to\neg p$와는 동치다. 조건문의 방향을 바꾸는 오류는 증명과 프로그램 사양에서 자주 발생한다.

## 술어와 양화사

술어 $P(x)$는 변수 값이 정해져야 명제가 된다.

$$\forall x\,P(x),\qquad \exists x\,P(x)$$

양화사의 순서는 중요하다. $\forall x\exists y\,R(x,y)$는 각 $x$에 다른 $y$를 골라도 되지만, $\exists y\forall x\,R(x,y)$는 하나의 $y$가 모든 $x$에 통해야 한다.

부정은 양화사를 바꾼다.

$$\neg\forall xP(x)\equiv\exists x\neg P(x)$$

## 형식적 추론

modus ponens는 $p$와 $p\to q$에서 $q$를, modus tollens는 $p\to q$와 $\neg q$에서 $\neg p$를 얻는다. 자연연역에서는 각 줄의 전제와 적용한 규칙을 명시해 결론이 문장 모양이 아니라 추론 규칙으로 따라오는지 확인한다.

## 프로그램과의 연결

precondition과 postcondition, loop invariant, 데이터베이스 질의의 조건은 술어로 쓸 수 있다. 테스트 사례가 많아도 전 범위의 참을 보장하지 않지만, 형식 증명은 정의역 전체에 대한 주장을 다룬다.

## 근거

Google Drive `CS204 / Lecture Note`의 1–8강 formal system, propositional·predicate logic, truth table, natural deduction 범위를 재구성했다.
