---
title: MIT HST.582J Biomedical Signal and Image Processing
description: MIT HST.582J Biomedical Signal and Image Processing을 따라가며 정리한 개념.
---

신호처리 이론을 심전도, 뇌파, 의료 영상 같은 생체 데이터에 적용하는 과목이다. [[courses/mit-6003/index|6.003]]의 신호·시스템 이론과 [[courses/mit-1805/index|18.05]]의 확률을 생체 신호 위에서 잇는다. 공개 강의 자료는 [MIT OpenCourseWare HST.582J](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007/)에 있다.

## 단원

| 단원               | 다루는 것                                   | 글                                                                                |
| ------------------ | ------------------------------------------- | --------------------------------------------------------------------------------- |
| 생체 신호 획득     | ADC, 샘플링, 디지털 필터                    | [[quantization-adc\|양자화와 ADC]] · [[sampling-aliasing\|샘플링과 앨리어싱]] · [[digital-filters-convolution\|디지털 필터와 컨볼루션]] |
| 이산 스펙트럼 방법 | DTFT, DFT, Z 변환, STFT                     | [[dtft\|이산시간 푸리에 변환]] · [[dft-fft\|DFT와 FFT]] · [[z-transform\|z 변환]] · [[stft-spectrogram\|단시간 푸리에 변환과 스펙트로그램]] |
| 랜덤 생체 신호     | 상관, 전력 스펙트럼 밀도, LTI를 지나는 잡음 | [[random-signals-autocorrelation\|랜덤 신호와 자기상관]] · [[power-spectrum-wiener-filter\|전력 스펙트럼과 위너 필터]] |
| 확률과 판정        | 검출, 분류, ROC                             | [[bayes-classifier-detection\|판정과 베이즈 분류기]] |
| 심전도 응용 | ECG 생리와 파형 | [[ecg\|ECG 측정 원리]] |
| 고급 방법          | 선형 예측, 블라인드 신호 분리               | [[linear-prediction\|선형 예측]] · [[blind-source-separation\|혼합 모형·PCA·ICA]] |
| 의료 영상 | 공간 필터·분할·정합·모달리티 | [[image-segmentation-registration\|분할과 정합]] · [[medical-imaging-physics\|영상 물리]] |

## 강의별 대조 범위

공개 [강의 목록](https://ocw.mit.edu/courses/hst-582j-biomedical-signal-and-image-processing-spring-2007/pages/lecture-notes/)에서 L1–6은 획득·필터·ECG·변환, L7–8은 음성·예측, L9–17은 영상·판정·분할·정합·모달리티, L18–20은 랜덤 신호·BSS에 대응한다. 위 글은 이 묶음들의 기초 모형과 계산을 다룬다. Z 변환은 원강의에서 수업 외 배포 자료다. L21 MRI의 시퀀스별 상세, L22 surgical applications, L23 Random Signals III의 세부, L24 종합은 독립 본문으로 다루지 않았다. 각 강의의 모든 유도·실습을 완료한 상태로 세지 않는다.
