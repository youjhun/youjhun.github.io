---
title: VAE 기반 신경 스파이크 데이터 증강
aliases: [neural spike VAE, BCI data augmentation]
tags: [프로젝트, BCI, VAE, 데이터증강]
date: 2026-10-20
description: 적은 신경 기록 trial에서 VAE 합성 데이터가 운동 디코더를 개선하는지 검증하는 실험 설계.
---

> [!abstract] 한눈에
> 실제 BCI에서는 긴 교정 세션이 환자를 지치게 한다. 이 실험은 실제 데이터가 100 trial뿐일 때, 그 데이터로 학습한 VAE가 만든 `(spike window, velocity)` 쌍을 더하면 디코더가 나아지는지 확인한다.

## 세 조건

| 조건                 | 학습 데이터           | 역할                 |
| -------------------- | --------------------- | -------------------- |
| Full data            | 전체 trial            | 도달 가능한 상한선   |
| Low data             | 실제 100 trial        | 증강이 필요한 기준선 |
| Low data + augmented | 실제 100 + 합성 trial | 증강 효과 측정       |

train/test 분할을 먼저 하고, VAE와 디코더는 train fold 안에서만 학습해야 한다. 전체 데이터로 VAE를 먼저 학습하면 test 분포가 생성 모델을 통해 새어 들어간다.

## 생성 대상

한 샘플은 `20 bins × neurons`의 스파이크 창과 대응하는 $(v_x,v_y)$다. encoder는 둘을 잠재변수 $z$로 압축하고, decoder는 스파이크와 속도를 함께 복원한다.

$$
\mathcal L
=\mathcal L_{spike}
+\lambda_v\mathcal L_{velocity}
+\beta D_{KL}(q_\phi(z\mid x)\|p(z))
$$

스파이크는 희소한 count 자료이므로 단순 MSE가 적절한지 Poisson 또는 negative-binomial likelihood와 비교해야 한다. 속도도 함께 복원하는 목적은 겉모양만 그럴듯한 데 그치지 않고 운동 정보가 보존된 스파이크를 만드는 데 있다.

## 생성 데이터 품질

디코더 성능을 보기 전에 생성 자체를 검사한다.

- 평균 발화율과 희소성
- 뉴런 간 공분산과 시간 자기상관
- 실제·합성 잠재분포의 겹침
- 합성 데이터만으로 학습한 간단한 Ridge 디코더의 운동 정보

UMAP 그림이 겹친다는 사실만으로 분포가 같다고 결론내리면 안 된다. 시각화는 진단이고, 정량 지표와 downstream 성능이 검증이다.

## 증강 비율 실험

실제 100 trial에 합성 데이터를 1:1, 1:3, 1:9로 더한다. 합성 비율이 커질수록 항상 좋아질 이유는 없다. 생성 분포의 작은 편향이 다수를 차지하면 오히려 실제 분포에서 멀어지는 **augmentation degradation**이 생길 수 있다.

## 가능한 결론

- 성능이 유의하게 상승하면 저데이터 BCI 교정에 증강이 유효하다는 근거가 된다.
- 변화가 작으면 생성 스파이크의 운동 일관성이 부족한지 확인한다.
- 성능이 하락하면 기본 VAE 대신 velocity-conditioned VAE나 오류 인지형 생성이 필요하다는 결론으로 이어진다.

세 경우 모두 먼저 정한 평가 절차를 지키면 유효한 결과다. 아직 실험 전인 항목은 결과처럼 쓰지 않는다.

## 관련 개념

- [[event-driven-neural-decoding|이벤트 기반 신경 디코더의 오류 내성]]
- [[bayes-update|베이즈 갱신]]: 잠재변수 모형의 사후분포를 이해하는 출발점.
- [[svd|특잇값 분해]]: 잠재 표현과 차원축소의 선형 기준선.
