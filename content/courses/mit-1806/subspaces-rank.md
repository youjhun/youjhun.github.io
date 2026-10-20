---
title: 열공간·영공간·랭크
aliases: [column space, null space, rank-nullity]
tags: [선형대수, 부분공간, 행렬]
date: 2026-10-20
description: 행렬을 입력 공간에서 출력 공간으로 가는 선형변환으로 읽고, 열공간·영공간·랭크를 연결한다.
---

> [!abstract] 한눈에
> $A\in\mathbb R^{m\times n}$은 $n$차원 입력을 $m$차원 출력으로 보낸다. 열공간은 만들 수 있는 출력의 집합이고, 영공간은 출력에서 사라지는 입력의 집합이다. 랭크는 실제로 전달되는 독립 방향의 수다.

## 행렬 모양부터 읽는다

$$
A:\mathbb R^n\rightarrow\mathbb R^m,\qquad x\mapsto Ax
$$

$A$의 열은 각각 $\mathbb R^m$의 벡터이고,

$$
Ax=x_1a_1+\cdots+x_na_n
$$

이므로 가능한 모든 출력은 열들의 선형결합이다.

## 열공간과 영공간

$$
\operatorname{Col}(A)=\{Ax:x\in\mathbb R^n\}\subseteq\mathbb R^m
$$

$$
\operatorname{Null}(A)=\{x:Ax=0\}\subseteq\mathbb R^n
$$

열공간은 출력 쪽, 영공간은 입력 쪽에 산다는 점이 중요하다. $b$가 열공간에 있을 때만 $Ax=b$의 정확한 해가 존재한다. 영공간에 0이 아닌 벡터가 있으면 서로 다른 입력이 같은 출력으로 가므로 해가 유일하지 않을 수 있다.

## 랭크-널리티

$$
\operatorname{rank}(A)+\operatorname{nullity}(A)=n
$$

입력의 $n$개 자유도는 출력에 남는 방향과 완전히 사라지는 방향으로 나뉜다. full column rank이면 영공간이 $\{0\}$이고, $Ax=b$의 해가 있다면 유일하다.

## 네 기본 부분공간

| 공간                       | 들어 있는 곳  | 의미                         |
| -------------------------- | ------------- | ---------------------------- |
| $\operatorname{Col}(A)$    | $\mathbb R^m$ | 가능한 출력                  |
| $\operatorname{Null}(A^T)$ | $\mathbb R^m$ | 열공간에 직교하는 출력 방향  |
| $\operatorname{Row}(A)$    | $\mathbb R^n$ | 출력에 영향을 주는 입력 방향 |
| $\operatorname{Null}(A)$   | $\mathbb R^n$ | 출력에서 사라지는 입력 방향  |

열공간과 $\operatorname{Null}(A^T)$, 행공간과 $\operatorname{Null}(A)$는 각각 서로 직교한다.

## 자주 하는 오해

- 열공간은 열벡터의 목록이 아니라 그 선형결합 전체다.
- 랭크는 행의 수나 열의 수가 아니라 독립한 열·행 방향의 수다.
- $Ax=0$은 출력이 0이라는 뜻이지 입력 $x$가 반드시 0이라는 뜻은 아니다.
- 행 기본변환은 영공간을 보존하지만 원래 행렬의 열공간 자체는 바꾼다.

## 관련 개념

- [[least-squares|최소제곱과 정사영]]: $b$를 열공간 위로 투영해 가장 가까운 해를 만든다.
- [[svd|특잇값 분해]]: 행공간·열공간·영공간의 직교기저를 한 번에 보여 준다.

## 참고 자료

- MIT OpenCourseWare, [18.06 Linear Algebra](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
