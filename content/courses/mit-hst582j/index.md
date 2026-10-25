---
title: MIT HST.582J 생체 신호·영상 처리
description: MIT HST.582J Biomedical Signal and Image Processing을 따라가며 정리한 개념.
---

신호처리 이론을 심전도, 뇌파, 의료 영상 같은 생체 데이터에 적용하는 과목이다. [[courses/mit-6003/index|6.003]]의 신호·시스템 이론과 [[courses/mit-1805/index|18.05]]의 확률을 생체 신호 위에서 잇는다. 공개 강의 자료는 [MIT OpenCourseWare HST.582J](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007/)에 있다.

## 단원

| 단원               | 다루는 것                                   | 글                                                                                |
| ------------------ | ------------------------------------------- | --------------------------------------------------------------------------------- |
| 생체 신호 획득     | ADC, 샘플링, 디지털 필터                    | [[quantization-adc\|양자화와 ADC]] · [[sampling-aliasing\|샘플링과 앨리어싱]] · [[digital-filters-convolution\|디지털 필터와 컨볼루션]] |
| 이산 스펙트럼 방법 | DTFT, DFT, Z 변환, STFT                     | [[dtft\|이산시간 푸리에 변환]] · [[dft-fft\|DFT와 FFT]] · [[z-transform\|z 변환]] · [[stft-spectrogram\|단시간 푸리에 변환과 스펙트로그램]] |
| 랜덤 생체 신호     | 상관, 전력 스펙트럼 밀도, LTI를 지나는 잡음 | [[random-signals-autocorrelation\|랜덤 신호와 자기상관]] · [[power-spectrum-wiener-filter\|전력 스펙트럼과 위너 필터]] |
| 확률과 판정        | 검출, 분류, ROC                             |                                                                                   |
| 심전도 응용        | ECG 생리와 파형                             |                                                                                   |
| 고급 방법          | 선형 예측, 블라인드 신호 분리               |                                                                                   |
| 의료 영상          | 분할, 정합, 영상 모달리티                   |                                                                                   |
