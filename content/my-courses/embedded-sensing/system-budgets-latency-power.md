---
title: 센서 시스템의 전력·지연·데이터율 예산
aliases: [Power Budget, Latency Budget, Data Rate]
tags: [Embedded Sensing, 시스템설계]
date: 2026-10-21
description: 센서부터 무선 전송까지 각 단계의 비용을 숫자로 닫는 시스템 예산표.
---

## 사양을 단계별 합으로 바꾸기

채널 수 $C$, 샘플링 주파수 $f_s$, 표본당 비트 수 $b$라면 가공 전 데이터율은

$$R_{raw}=C f_s b$$

이다. packet header, error correction, retransmission이 붙으면 실제 무선 데이터율은 더 커진다. 압축은 전송 에너지를 줄일 수 있지만 계산 에너지와 지연, 정보 손실을 추가한다.

평균 전력은 상태별 전력과 duty cycle로 계산한다.

$$P_{avg}=\sum_i d_iP_i$$

sleep 전력이 작아도 자주 깨거나 radio startup이 길면 이득이 줄 수 있다. 배터리 수명은 단순히 정격 에너지/$P_{avg}$로 먼저 추정하되 regulator 효율, self-discharge, peak current와 온도를 반영해 검증한다.

## 지연 예산

$$T_{total}=T_{acq}+T_{window}+T_{compute}+T_{queue}+T_{tx}+T_{decision}$$

실시간 분류에서는 창 길이가 흔히 가장 큰 지연이다. 빠른 모델만 최적화해도 2초짜리 창을 기다리면 2초 지연은 남는다. 평균뿐 아니라 worst-case와 jitter를 본다.

## 예산을 닫는 순서

1. 사용자에게 필요한 반응시간과 정확도를 정한다.
2. 신호 대역에서 샘플링·ADC 조건을 정한다.
3. raw 데이터율과 저장·전송 비용을 계산한다.
4. 각 블록의 평균·peak 전력을 더한다.
5. worst-case 링크, 온도와 배터리에서 margin을 확인한다.
6. 측정값으로 추정을 갱신한다.

## 시스템 교환관계

샘플링률과 bit 수를 늘리면 정보량과 전력·데이터율이 함께 늘고, 긴 창은 추정을 안정시키지만 지연과 메모리를 키운다. 한 블록의 최적값이 전체 시스템의 최적값은 아니다.
