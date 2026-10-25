---
title: EE201 회로이론
description: 선형 회로를 방정식, 등가회로와 동적 시스템으로 읽는 회로이론 과목 기록.
aliases: [EE201]
---

선형 회로를 키르히호프 법칙, 등가회로, 저장 소자가 만드는 동적 응답으로 다루는 과목이다.

## 계산과 검산

| 작업 | 본문 |
| --- | --- |
| DC 회로를 연립방정식으로 구성 | [[thevenin-node-analysis#kcl-방정식의-구성\|KCL·supernode]] |
| 저장 상태의 초기값 | [[capacitors-inductors#초기조건을-정하는-순서\|0−·0+와 연속성]] |
| RC·RL 과도응답 | [[first-order-rc-rl#세-값으로-푸는-스위칭-예\|6단계 계산 예]] · [[first-order-rc-rl#rl-회로의-같은-계산\|RL 검산]] |
| 필터 뒤에 부하 연결 | [[first-order-rc-rl#필터의-부하와-재설계\|DC 이득·pole 재계산]] |
| RLC 계수와 초기조건 | [[second-order-rlc#초기-기울기와-상수-결정\|초기 기울기·자연응답]] |
| 진동·overshoot·공진 | [[second-order-rlc#수치-응답-예\|수치 예]] · [[second-order-rlc#q와-주파수응답\|출력별 Q와 대역폭]] |

## 단원

| 단원 | 주제 | 본문 |
| --- | --- | --- |
| 회로 기초 | 전력·직병렬·분압·망전류·전원 변환·Y–Δ | [[resistive-mesh-networks\|저항망과 망전류]] |
| 절점과 단자 등가 | KCL·supernode·중첩·종속 전원 | [[thevenin-node-analysis\|절점·Thevenin·Norton]] |
| 증폭기 | 이상 op-amp·회로군·비이상성 | [[op-amp-circuit-families\|연산증폭기]] |
| 저장 소자 | 전압-전류 관계, 연속성, 저장 에너지 | [[capacitors-inductors\|커패시터와 인덕터]] |
| 1차 회로 | 계단 응답, 시간상수, 1차 필터 | [[first-order-rc-rl\|RC·RL 1차 회로]] |
| 2차 회로 | 특성근, 감쇠와 공진 | [[second-order-rlc\|RLC 2차 회로]] |

## 다른 과목에서 다룬 기초

- [[thevenin-node-analysis|절점해석과 Thevenin 등가]]: KCL, 중첩, 단자 등가회로
- [[op-amp-biosignal-front-end|연산증폭기와 생체신호 앞단]]: 음의 피드백, 입력 임피던스와 포화
- [[difference-equations-feedback|차분방정식과 피드백]]: 1차 회로의 이산시간 대응

## 강의 범위 밖

- [[phasor-ac-power|페이저·임피던스·교류전력]]: 교재 8–9장에 해당하는 보충. Notion의 `ch8` 파일과 교재 8장이 같은 단원인지는 첨부 본문을 확인하지 못해 확정하지 않는다.
- [[laplace-transform|라플라스 회로 해석]]: 교재 13–14장의 수학적 기반.

## 범위 대조

Notion에는 강의 파일 ch0–ch8과 11판 교재 이름이 있다. 파일 번호만으로 그 안의 단원 제목을 확정하지 않는다. 출판사 교재 목차와의 대응은 다음과 같다.

| 교재 단원 묶음 | 연결 글 | 강의 포함 여부 |
| --- | --- | --- |
| 1–5 기본·저항·절점/루프·op-amp·등가 | 위 기초 세 글 | 수업 파일 세부 목차 대조 필요 |
| 6–7 저장소자·과도응답 | C/L·RC/RL·RLC | 기존 개념 기록 보강 |
| 8–9 교류 정상상태·전력 | [[phasor-ac-power\|교류 계산]] | 교재 기준 보충 |
| 10–11 결합회로·다상 | 독립 상세 글 없음 | 수업 포함 여부 미확인 |
| 12 주파수응답 | [[bode-plot\|보드 선도]] · [[second-order-rlc\|공진]] | 교재 기준 연결 |
| 13–14 Laplace·회로 응용 | [[laplace-transform\|변환과 초기조건]] | 교재 기준 보충 |
| 15 Fourier | [[fourier-series\|급수]] · [[fourier-transform\|변환]] | 교재 기준 연결 |

교재 전체와 실제 한 학기의 범위는 구분한다. 결합회로·다상 등 아직 본문이 없는 항목을 기재해 범위의 공백을 남겨 둔다.

## 참고 자료

- 강의에 기록된 교재: *Engineering Circuit Analysis*, 11판. [Wiley 단원표](https://bcs.wiley.com/he-bcs/Books?action=contents&bcsId=9563&itemId=1118960637).
