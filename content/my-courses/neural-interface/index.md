---
title: Human Sensing & Neural Interface Foundations
description: 몸의 신호를 재고, 무선으로 보내고, 전극으로 자극하는 시스템을 처음부터 끝까지 이해하기 위해 짠 과목.
---

뇌에 심는 무선 센서가 신호를 재서 밖으로 보내기까지는 여러 층을 거친다. 전극과 조직의 경계, 아날로그 앞단(AFE)과 ADC, 무선 통신 채널, 전력 전달, 그리고 이것들을 하나로 묶는 시스템 설계다. 이 과목은 그 층들을 하나의 경로로 이어서 다룬다.

신호처리와 생체 신호의 기반은 [[courses/mit-6003/index|MIT 6.003]]과 [[courses/mit-hst582j/index|MIT HST.582J]]에서 가져오고, 이 과목에는 그 강의들이 다루지 않는 부분만 둔다.

## 단원

| 단원               | 다루는 것                                           | 참고하는 강의        | 글                                                                |
| ------------------ | --------------------------------------------------- | -------------------- | ----------------------------------------------------------------- |
| 측정 경로 점검     | 전극에서 아날로그 앞단, 증폭, ADC까지의 경로와 잡음 | 회로이론, 바이오계측 | [[quantization-adc\|양자화와 ADC]]                                |
| 무선 원격 측정     | 잡음과 물리 채널, 변조, 다중 접속                   | MIT 6.02, Smart Sensors 11–12장 | [[matched-filter\|정합 필터]], [[low-power-mac\|저전력 센서 네트워크의 MAC]], [[wakeup-scheduling-time-sync\|깨어남 일정과 시간 동기화]] |
| 전극–조직 경계     | 전극 계면과 조직 반응, 기록 임피던스                | Smart Sensors 4장    | [[electrode-tissue-interface\|전극–조직 경계]] |
| 무선 전력과 전자기 | 준정적 결합, 공진, RF 링크                          | MIT 6.013, Smart Sensors 3장 | [[wireless-power-telemetry\|무선 전력과 원격 측정]] |
| 시스템 통합        | 측정부터 전송까지 한 시스템으로 묶기                | 위 단원 전체와 논문  | [[asbit-wireless-sensor-network\|논문: ASBIT 무선 센서 네트워크]] |
| 비침습 BCI         | 운동상상, ERD·ERS, 공간필터                         | EEG·BCI 자료         | [[motor-imagery-eeg\|운동상상 EEG와 ERD·ERS]]                     |
| 신호 변이성        | trial·세션·사용자 사이의 분포 변화                  | 통계·리만 기하       | [[eeg-variability\|MI-BCI의 EEG 변이성]]                          |
