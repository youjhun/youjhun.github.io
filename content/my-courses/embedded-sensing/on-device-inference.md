---
title: 기기 안 추론을 설계하는 법
aliases: [On-device Inference, TinyML, Edge AI]
tags: [Embedded Sensing, Machine Learning]
date: 2026-10-21
description: 센서 기기에서 모델의 정확도와 메모리·연산·지연·에너지를 함께 맞추는 절차.
---

## 모델 파일 크기만 보면 부족하다

기기 안 추론의 메모리는 가중치뿐 아니라 activation, 입력 buffer, 전처리 workspace와 runtime을 포함한다. 연산량(MACs)이 비슷해도 memory access 패턴과 하드웨어 가속 지원에 따라 에너지와 지연이 달라진다. 목표 보드에서 end-to-end로 재야 한다.

## 센서 파이프라인 전체를 배포한다

> 샘플링 → 보정·필터 → 창 buffer → 특징/모델 → 후처리 → 행동

학습 코드의 전처리와 배포 코드가 다르면 모델 가중치가 같아도 출력이 달라진다. 필터 초기조건, 정규화 상수, 축 순서, sample-rate drift와 결측 처리까지 모델 계약의 일부로 고정한다.

## 줄이는 방법

- quantization: float를 int8 등으로 줄여 메모리와 연산을 절약한다.
- pruning/sparsity: 중요도가 낮은 연결을 제거한다. 하드웨어가 sparse 연산을 지원해야 실제 속도 이득이 난다.
- knowledge distillation: 큰 모델의 출력을 작은 모델이 배우게 한다.
- feature/model co-design: raw waveform 대신 필요한 특징만 계산한다.
- event-driven inference: 변화가 있을 때만 무거운 모델을 켠다.

압축 전후에는 전체 정확도뿐 아니라 사람·활동·센서 위치별 성능과 calibration을 비교한다.

## 스트리밍 검증

미리 잘라 놓은 독립 창의 정확도는 실제 스트림 성능을 충분히 말하지 않는다. 연속 입력에서 중복 창, 상태 전환, false alarm/hour, 검출 지연, 배터리 소모를 함께 잰다. 학습·시험 분리는 deployment 단위, 예를 들어 새 사용자나 새 세션에 맞춰야 한다.

## 연결

- [[system-budgets-latency-power|센서 시스템의 전력·지연·데이터율 예산]]
- [[projects/event-driven-neural-decoding|이벤트 기반 신경 디코딩]]
- [[projects/data-leakage|생체신호 데이터 누수]]
