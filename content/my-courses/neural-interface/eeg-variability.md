---
title: MI-BCI의 EEG 변이성
aliases: [BCI nonstationarity]
tags: [EEG, BCI, 변이성]
date: 2026-10-20
description: MI-BCI 성능을 흔드는 EEG 변화를 시간·공간·주파수와 trial 계층으로 나누어 진단한다.
---

> [!abstract] 한눈에
> EEG 변이성이 크다는 한 숫자만으로는 무엇을 고쳐야 할지 알 수 없다. 변화가 시간축의 timing인지, 채널 분포인지, 주파수 패턴인지 분리하고, 한 trial 안·trial 사이·trial 묶음 사이 중 어디에서 생기는지 함께 봐야 한다.

## variability와 nonstationarity

variability는 관측들이 서로 달라지는 정도다. nonstationarity는 신호를 만드는 분포가 시간에 따라 바뀌는 성질이다. nonstationarity는 within-user variability의 중요한 원인이지만 둘은 같은 말이 아니다. 측정 잡음이나 과제 수행 차이도 variability를 만든다.

## 세 표현축

| 축     | 묻는 질문                                     | 예시 표현                     |
| ------ | --------------------------------------------- | ----------------------------- |
| 시간   | ERD 시작 시점과 지속 시간이 trial마다 같은가? | envelope, latency, trajectory |
| 공간   | 어느 채널·피질 영역이 강한가?                 | covariance, topography        |
| 주파수 | 반응 대역과 스펙트럼 모양이 같은가?           | band power, PSD               |

주파수는 시간 신호의 다른 표현이므로 완전히 독립은 아니다. 여기서 `분리`는 원인을 단정한다는 뜻이 아니라 진단 가능한 좌표로 나눈다는 뜻이다.

## 세 비교 계층

- **within-trial**: 한 trial 안에서 짧은 epoch들의 표현이 얼마나 움직이는가.
- **between-trial**: 같은 class의 trial들이 얼마나 다른가.
- **between-trial-group**: 세션, 날짜, 사용자 같은 묶음 사이가 얼마나 다른가.

공분산 행렬을 쓰면 일반 유클리드 공간이 아니라 양의 정부호 행렬의 기하를 고려할 수 있다. trial을 짧은 epoch로 나눈 뒤 공분산 궤적의 퍼짐을 보면 한 trial 내부와 trial 사이 변화를 함께 볼 수 있다.

## 분류와의 관계

transfer learning, domain adaptation, distribution alignment는 변이성이 있어도 분류 성능을 유지하려는 방법이다. 변이성 지표의 역할은 그보다 앞선다. **어느 축과 계층이 흔들리는지 진단**해 어떤 적응이 필요한지 고르는 것이다.

## 해석 경계

특정 변이성 지표가 낮은 정확도와 상관돼도, 그 변이성을 줄이면 정확도가 반드시 올라간다는 인과관계는 증명되지 않는다. 지표는 우선 diagnostic tool이고, 실제 개선은 그 지표를 표적으로 한 전처리나 모델을 별도 실험해야 한다.

## 자주 하는 오해

- 사용자 간 변화와 한 사용자의 세션 간 변화를 한 지표로 섞으면 원인을 잃는다.
- 평균 ERD 크기만 같아도 시간·공간 패턴은 다를 수 있다.
- domain adaptation 뒤 정확도가 올라갔다고 생리적 변이성이 줄었다고 말할 수는 없다.

## 관련 개념

- [[motor-imagery-eeg|운동상상 EEG와 ERD·ERS]]
- [[svd|특잇값 분해]]
- [[confidence-interval-hypothesis-test|신뢰구간과 가설검정]]
