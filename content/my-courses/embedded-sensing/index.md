---
title: Embedded Sensor Systems
description: 센서에서 기기 안의 추론까지를 하나의 시스템으로 보기 위해 짠 과목.
---

센서, 아날로그 앞단, ADC, 샘플링, 전력, 실시간 처리와 기기 안 추론(on-device inference)을 하나의 시스템으로 묶어 보는 과목이다. 신호처리 이론을 실제로 제한된 전력과 계산 안에서 돌릴 때 무엇을 포기하고 무엇을 지켜야 하는지를 다룬다.

## 관련 글

[[quantization-adc|양자화와 ADC]]와 [[dft-fft|DFT와 FFT]]가 이 과목의 출발점이 된다.

- [[system-budgets-latency-power|전력·지연·데이터율 예산]]
- [[on-device-inference|기기 안 추론과 모델 경량화]]

## 설계 연결

| 단계        | 연결 글                                                                                             | 계산할 값                          |
| ----------- | --------------------------------------------------------------------------------------------------- | ---------------------------------- |
| 센서·앞단   | [[biosignal-measurement-chain\|생체신호 측정 사슬]] · [[op-amp-biosignal-front-end\|아날로그 앞단]] | 입력 범위·잡음·감쇠                |
| 표본화·저장 | [[quantization-adc\|양자화와 ADC]]                                                                  | 표본 크기·입력 환산 LSB            |
| 전송·전원   | [[system-budgets-latency-power\|시스템 예산]] · [[wireless-power-telemetry\|무선 전력과 원격 측정]] | payload rate·평균 전력·링크 margin |
| 실시간 처리 | [[on-device-inference\|기기 안 추론]]                                                               | 최대 RAM·갱신 간격·실행시간        |

8채널·500 Hz 신호의 데이터율 계산에서 시작해, 1초 입력 창의 메모리와 100 ms 갱신 조건을 함께 비교할 수 있다. 시스템 예산과 추론 글의 수치는 같은 가상 입력 조건을 사용한다.
