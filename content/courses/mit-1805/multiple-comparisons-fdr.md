---
title: 다중비교와 FDR
aliases: [다중비교, FDR, 거짓 발견율, Benjamini-Hochberg, BH 절차, Bonferroni, Multiple comparisons]
tags: [통계, 18.05]
date: 2026-10-19
description: 검정을 여러 번 하면 우연히 걸리는 것이 반드시 생긴다. Bonferroni와 Benjamini–Hochberg가 각각 무엇을 막는지.
---

> [!abstract] 한눈에
> 효과가 없는 검정을 20번 하면, 각각 유의수준 0.05여도 한 번 이상 '유의'가 나올 확률은 64%다. 이를 막는 방법은 무엇을 통제하느냐에 따라 갈린다. **Bonferroni**는 거짓 양성이 **하나라도** 나올 확률(FWER)을 묶고, **Benjamini–Hochberg(BH)** 는 발견한 것들 가운데 거짓의 **비율의 기댓값**(FDR)을 묶는다. BH는 더 많이 발견하는 대신 그중 일부가 틀릴 수 있다는 것을 받아들인다.

## 문제: 많이 물으면 우연히 걸린다

검정 하나를 유의수준 $\alpha = 0.05$로 하면, 효과가 없을 때 '유의'로 잘못 판정할 확률은 5%다. 서로 독립인 검정을 $m$번 하면 한 번 이상 잘못 판정할 확률은

$$
1 - (1 - \alpha)^m
$$

이다. 10번이면 40%, 20번이면 64%, 50번이면 92%다(그림 1). 뇌파 채널 수십 개, 주파수 대역 여러 개, 지표 여러 개를 각각 검정하면 '유의한' 결과가 몇 개 나오는 것은 당연한 일이다.

![검정 횟수와 거짓 양성 확률](../../images/multiple-comparisons-fdr/fwer.png)
*그림 1. 모든 검정이 효과가 없을 때, 한 번 이상 거짓 양성이 나올 확률.*

## 두 가지 기준: FWER와 FDR

검정 $m$개 가운데 기각한 것(발견)을 $R$개, 그중 실제로는 효과가 없던 것(거짓 발견)을 $V$개라 하자.

- **FWER**(family-wise error rate) $= P(V \ge 1)$: 거짓 발견이 하나라도 있을 확률
- **FDR**(false discovery rate) $= E\!\left[\, V / R \,\right]$ ($R = 0$이면 $V/R$을 0으로 둔다): 발견들 가운데 거짓의 비율의 기댓값

FWER을 통제하면 "발견 목록 전체가 다 맞을" 확률을 보장한다. FDR을 통제하면 "발견 목록의 평균적인 순도"를 보장한다.

## Bonferroni: 기준을 m으로 나눈다

가장 단순한 방법이다. 각 검정을 $\alpha/m$으로 판정하면 FWER가 $\alpha$ 이하가 된다. 검정 사이의 의존 관계와 상관없이 성립한다. 대신 $m$이 커지면 기준이 아주 엄격해져서, 진짜 효과도 많이 놓친다.

## Benjamini–Hochberg 절차

1995년에 벤야미니(Benjamini)와 호흐베르크(Hochberg)가 제안했다. 목표 FDR을 $q$(예: 0.05)라 하자.

1. p-value $m$개를 작은 것부터 정렬한다: $p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}$.
2. $p_{(k)} \le \dfrac{k}{m}\, q$를 만족하는 **가장 큰** $k$를 찾는다.
3. $p_{(1)}, \dots, p_{(k)}$에 해당하는 가설을 모두 기각한다.

그림으로 보면 정렬한 p-value를 기울기 $q/m$인 직선과 비교하는 것이다(그림 2). Bonferroni는 높이가 $q/m$인 수평선 하나와 비교하는 셈이라 첫 번째 칸에서만 같고, 순위가 올라갈수록 BH의 기준이 너그러워진다.

![BH 절차](../../images/multiple-comparisons-fdr/bh-procedure.png)
*그림 2. 검정 50개 중 10개만 진짜 효과(초록)인 시뮬레이션. 파란 BH 선 아래에 있는 마지막 점까지 기각한다. 같은 자료에서 Bonferroni(주황 점선)는 더 적게 기각한다.*

2단계에서 '가장 큰 $k$'를 찾는다는 점이 중요하다. 중간에 선 위로 올라간 점이 있어도, 더 뒤에 선 아래에 있는 점이 있으면 거기까지 모두 기각한다.

검정들이 서로 독립이거나 특정한 양의 의존 관계(PRDS)에 있으면 BH는 FDR을 $q \cdot m_0/m$ 이하로 지킨다. $m_0$은 실제로 효과가 없는 검정의 수다. 의존 구조를 모를 때는 더 보수적인 Benjamini–Yekutieli 절차를 쓴다.

## 세 방법을 나란히

그림 2의 상황(검정 50개 중 진짜 효과 10개)을 1,000번 반복해 평균을 냈다.

![세 방법의 발견과 거짓 발견](../../images/multiple-comparisons-fdr/methods.png)
*그림 3. 보정하지 않으면 발견은 많지만 그중 약 17%가 거짓이다. Bonferroni는 거짓이 거의 없지만 진짜도 절반 넘게 놓친다. BH는 그 사이에서 거짓 비율을 0.05 아래로 지킨다.*

## 자주 하는 오해

- **"FDR 0.05로 통제했으니 이번 발견 중 정확히 5%가 거짓이다."** FDR은 **기댓값**이다. 한 번의 연구에서는 거짓 비율이 0일 수도, 20%일 수도 있다.
- **"FDR 0.05면 각 발견이 거짓일 확률이 5%다."** 목록 전체의 평균 순도에 대한 보장이지, 발견 하나하나의 확률이 아니다. 기준선 근처에서 겨우 통과한 발견은 더 의심스럽다.
- **"Bonferroni는 너무 보수적이니 틀린 방법이다."** 틀린 것이 아니라 다른 것을 지킨다. "하나라도 틀리면 안 되는" 상황(예: 확증 임상시험)에서는 FWER이 맞는 기준이다.
- **"부트스트랩을 1,000번 했으니 다중비교 문제가 있다."** 부트스트랩 반복은 추정값 **하나**의 불확실성을 재는 계산일 뿐, 가설을 1,000개 검정한 것이 아니다. 다중비교가 문제 되는 것은 서로 다른 질문(지표, 채널, 주파수 대역 등)을 여러 개 검정할 때다.
- **"보정은 검정 개수만 세면 된다."** 무엇을 한 묶음(family)으로 볼지는 연구 질문이 정한다. 결과를 보고 나서 묶음을 정하면 보정의 의미가 사라진다.

## 관련 개념

- [[p-value|p-value]]: 보정의 재료
- [[bootstrap|부트스트랩과 표준오차]]: 다중비교와 헷갈리기 쉬운 '반복 계산'

## 참고 자료

- Y. Benjamini, Y. Hochberg, "Controlling the false discovery rate: a practical and powerful approach to multiple testing," *Journal of the Royal Statistical Society: Series B* 57(1), 289–300 (1995)
- Y. Benjamini, D. Yekutieli, "The control of the false discovery rate in multiple testing under dependency," *The Annals of Statistics* 29(4), 1165–1188 (2001)
- MIT OCW, [18.05 Introduction to Probability and Statistics (Spring 2022)](https://ocw.mit.edu/courses/18-05-introduction-to-probability-and-statistics-spring-2022/), 유의성 검정 단원
