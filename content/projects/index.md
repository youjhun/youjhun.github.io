---
title: 프로젝트
description: 문제를 정의하고, 데이터를 다듬고, 실험으로 주장과 한계를 확인한 기록.
---

## 신경 신호와 BCI

- [[event-driven-neural-decoding|이벤트 기반 신경 디코더의 오류 내성]]: 신경 스파이크 전송 오류가 Kalman·Ridge·MLP·LSTM 디코더에 미치는 영향을 비교한다.
- [[neural-data-augmentation|VAE 기반 신경 스파이크 데이터 증강]]: 적은 trial로 디코더를 학습해야 할 때 합성 데이터가 실제로 도움이 되는지 검증하는 실험 설계.
- [[schizophrenia-eeg|EEG로 조현병 분류하기 (실습)]]: 뇌파 특징과 사람 단위 교차검증
- 배운 것: [[data-leakage|데이터 누수와 검증 단위]]

## 아날로그 계측

- [[emg-afe-kicad|EMG 앞단 회로 시뮬레이션]]: 기준전압·증폭·필터·정류·평활·히스테리시스를 구성하고 실제 EMG 기록으로 활동을 판정한다.
- [[emg-afe-design-reasoning|EMG 설계 질문과 계산]]: 소자·기준전압·이득·문턱의 유도를 단계별로 정리한다.
- [[emg-afe-replay-validation|EMG 재생과 검증]]: WFDB·PWL·측정과 문턱 보정의 한계를 기록한다.

## 프로젝트와 개념의 연결

디코더의 수학은 [[linear-regression|선형 회귀]], [[least-squares|최소제곱]], [[svd|SVD]]와 이어진다. 무선 전송 오류의 배경은 [[asbit-wireless-sensor-network|ASBIT]]에 있다.
