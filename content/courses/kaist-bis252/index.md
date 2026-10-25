---
title: BiS252 바이오계측 회로 기초
description: 저항 회로와 절점해석에서 Thevenin 등가, 연산증폭기, RC/RL 회로로 이어지는 생체계측 회로 기록.
aliases: [BiS252]
---

생체계측기는 센서만으로 완성되지 않는다. 작은 전압·전류를 다음 단계가 읽을 수 있게 만들고, 원하는 대역을 남기며, ADC 범위 안에 넣는 아날로그 회로가 필요하다.

## 계산과 설계

| 작업 | 본문 |
| --- | --- |
| 전압·전류·단자 등가 | [[thevenin-node-analysis#kcl-방정식의-구성\|절점해석 예제]] · [[thevenin-node-analysis#단자-등가의-절차\|시험 전원과 Thevenin]] |
| 센서의 로딩 오차 | [[thevenin-node-analysis#로딩과-최대전력-계산\|입력저항 요구량]] |
| 증폭 방식과 저항 선택 | [[op-amp-circuit-families#회로별-빠른-선택\|회로 선택표]] · [[op-amp-circuit-families#기준전압이-있는-반전-회로\|단일전원 기준전압]] |
| 주파수·큰 신호 제한 | [[op-amp-circuit-families#noise-gain과-대역폭\|Noise gain·대역폭·slew rate]] |
| 차동·공통모드 계산 | [[difference-amplifier-cmrr#두-입력으로의-역변환\|Ad·Acm 유도]] · [[difference-amplifier-cmrr#cmrr-요구량의-역산\|허용오차에서 CMRR]] |
| 이득을 단별로 배분 | [[op-amp-biosignal-front-end#이득-배분과-헤드룸\|DC 오프셋·출력 범위]] |
| 필터·과도응답 | [[first-order-rc-rl#세-값으로-푸는-스위칭-예\|초기값·최종값·시간상수]] |

## 단원

| 단원               | 핵심 질문                                  | 공개 글                      |
| ------------------ | ------------------------------------------ | ---------------------------- |
| 회로 요소와 저항망 | 전압·전류·전력은 어떻게 연결되는가         | [[resistive-mesh-networks\|전력·직병렬·분압]] · [[thevenin-node-analysis\|절점해석과 Thevenin 등가]]   |
| 절점해석·중첩      | 복잡한 선형 회로를 어떻게 나눠 푸는가      | [[thevenin-node-analysis\|절점해석과 Thevenin 등가]]   |
| 연산증폭기         | 작은 차동 신호를 어떻게 증폭하는가         | [[op-amp-biosignal-front-end\|연산증폭기와 생체신호 앞단]] · [[difference-amplifier-cmrr\|차동 증폭기와 CMRR]] |
| 연산증폭기 기본 연결 | 피드백과 KCL로 이득을 어떻게 구하는가 | [[op-amp-circuit-families\|반전·비반전·가산·버퍼·TIA]] |
| RC/RL 회로         | 저장소가 과도응답과 필터를 어떻게 만드는가 | [[first-order-rc-rl\|RC·RL 1차 회로]] |

## 원자료와의 대응

| 기록된 파일 묶음 | 본문 | 대조 범위 |
| --- | --- | --- |
| Week01 소개·계측·회로요소 | [[biosignal-measurement-chain\|측정 사슬]] · [[resistive-mesh-networks\|회로요소와 전력]] | 파일명과 공개 기초 개념 |
| Week02 저항·절점 | [[resistive-mesh-networks\|직병렬·분압]] · [[thevenin-node-analysis\|절점 방정식]] | 새 회로와 검산 |
| Week03 Thevenin·중첩 | [[thevenin-node-analysis\|단자 등가·중첩·시험 전원]] | 단자 규약과 로딩 |
| Week04–07 OP AMP와 Categories 텍스트 | [[op-amp-circuit-families\|회로군]] · [[difference-amplifier-cmrr\|차동·CMRR]] · [[op-amp-biosignal-front-end\|신호 앞단]] | 텍스트를 대조하고 상세 유도 보충 |
| Week07 RC/RL | [[capacitors-inductors\|저장소자]] · [[first-order-rc-rl\|초기값·최종값·시간상수]] | 과도응답 계산 |
| 이후 주차·syllabus 세부 | 아직 확인하지 못함 | Week07까지의 파일 목록을 전체 학기와 동일시하지 않음 |

> [!note] 근거
> 2024 Fall `Studies / BiS252`의 강의 파일 목록과 Op-Amp 텍스트 기록을 확인했다. 첨부 강의 PDF 전체의 본문과 전체 학기 syllabus를 모두 대조한 상태는 아니다.
