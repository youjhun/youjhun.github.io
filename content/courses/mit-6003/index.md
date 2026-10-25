---
title: MIT 6.003 신호와 시스템
description: MIT 6.003 Signals and Systems (Fall 2011)를 따라가며 정리한 개념.
---

신호를 수학적 대상으로 다루고, 시스템이 신호를 어떻게 바꾸는지를 시간 영역과 주파수 영역 양쪽에서 보는 과목이다. 공개 강의 자료는 [MIT OpenCourseWare 6.003 (Fall 2011)](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/)에 있다.

## 단원

| 단원               | 다루는 것                                      | 글                                                                                                        |
| ------------------ | ---------------------------------------------- | --------------------------------------------------------------------------------------------------------- |
| 신호·시스템·동역학 | 신호 변환, 차분방정식, 블록 다이어그램, 피드백 | [[signals-transformations\|신호를 읽는 첫 문법]] · [[difference-equations-feedback\|차분방정식과 피드백]] |
| 변환과 극점        | Z·라플라스 변환, 극점과 영점                   | [[z-transform\|z 변환]]                                                                                   |
| 컨볼루션           | LTI 시스템의 입출력                            |                                                                                                           |
| 주파수 응답        | 보드 선도, 필터                                | [[bode-plot\|주파수 응답과 보드 선도]] |
| 연속시간 푸리에    | 푸리에 급수와 변환                             | [[fourier-series\|푸리에 급수]] · [[fourier-transform\|연속시간 푸리에 변환]] |
| 이산시간 푸리에    | DTFT, DFT, FFT, 네 가지 표현의 관계            | [[dtft\|이산시간 푸리에 변환]] · [[dft-fft\|DFT와 FFT]]                                                   |
| 푸리에 응용        | 필터링, 생체 신호                              |                                                                                                           |
| 샘플링·양자화      | 표본화 정리, 앨리어싱                          | [[sampling-aliasing\|샘플링과 앨리어싱]]                                                                  |
| 변조               | 진폭·주파수 변조, 무선 통신                    | [[modulation\|변조]] |

양자화는 [[courses/mit-hst582j/index|HST.582J]]의 [[quantization-adc|양자화와 ADC]]에 정리했다.
