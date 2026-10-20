---
title: "논문 리뷰: 무선 마이크로임플란트 네트워크, Neurograin"
aliases: [Neurograin, Neural recording and stimulation using wireless networks of microimplants]
tags: [논문, 신경공학, 무선전력, BCI]
date: 2026-10-20
description: 독립된 초소형 칩들을 피질 위에 분산 배치하고 무선 전력·통신으로 기록과 자극을 수행한 Neurograin 시스템.
---

> [!abstract] 한눈에
> 한 장의 큰 전극 배열을 확장하는 대신, 기록·자극·무선 통신을 넣은 작은 칩을 여러 개 흩어 놓는다. 이 논문은 48개 neurograin을 쥐 피질 위에서 개별 식별해 신경 기록과 자극을 시연하고, 맞춤형 TDMA로 더 큰 네트워크를 만드는 경로를 제시했다.

|      |                                                                           |
| ---- | ------------------------------------------------------------------------- |
| 제목 | Neural recording and stimulation using wireless networks of microimplants |
| 게재 | _Nature Electronics_ 4, 604–614 (2021)                                    |
| DOI  | [10.1038/s41928-021-00631-8](https://doi.org/10.1038/s41928-021-00631-8)  |

## 문제: 큰 배열 한 장의 구조적 한계

기존 피질 인터페이스는 수백 접점을 한 기판이나 케이블에 묶는다. 채널을 수천 개로 늘리면 배선, 데이터 전송, 이식 크기가 함께 커지고 서로 떨어진 피질 영역에 자유롭게 배치하기 어렵다.

Neurograin은 반대로 각 접점을 독립된 SoC 노드로 만든다. 개별 노드는 작고 배치가 자유롭지만, 이제 무선 전력, 주소, 충돌, 대역폭을 네트워크 차원에서 해결해야 한다.

## 시스템

- **칩**: TSMC 65 nm RF CMOS, 약 $650\times650\times250\ \mu m$, 부피 약 $0.1\ mm^3$.
- **링크**: 약 1 GHz 근접장 결합. 외부 Tx 코일과 피하 relay coil이 칩의 전력 수확과 양방향 통신을 맡는다.
- **기록 칩**: 1 kHz, 8-bit로 ECoG형 신호를 기록하는 AFE·ADC와 BPSK uplink.
- **자극 칩**: programmable biphasic pulse를 만들고 ASK-PWM downlink 명령을 받는다.
- **주소**: laser로 새긴 metal trace 주소 또는 공정 편차에서 얻은 PUF 주소.

## 두 TDMA 방식

### Autonomous TDMA

칩마다 자유 발진기로 정한 의사무작위 시간에 100 ms 분량 데이터를 보낸다. 회로는 단순하지만 동기화가 없어 노드가 늘면 충돌한다. 64개 칩 벤치 실험에서 충돌이 BER의 주된 원인이었다.

### Call-and-respond TDMA

외부 허브가 PUF 주소로 특정 칩을 부르면 그 칩이 응답한다. 회로와 downlink가 더 필요하지만 충돌을 피하고 원하는 채널만 읽을 수 있다. 32개 칩 실험에서 개별 호출·응답을 시연했고, 저자들은 100 ms 안에 425개, 더 짧은 call을 쓰면 최대 770개까지 가능한 구조를 계산했다.

## 무엇을 실제로 보였나

| 범위          | 검증                                                           |
| ------------- | -------------------------------------------------------------- |
| 단일 칩       | 무선 전력, 기록 AFE, 자극 회로, uplink/downlink                |
| 벤치 네트워크 | autonomous 64개, call-and-respond 32개 통신                    |
| 동물          | 쥐 피질 위 48개 칩의 개별 주소 식별과 급성 기록·자극           |
| 확장성        | 770개는 실제 이식 수가 아니라 프로토콜 시간 예산에 근거한 계산 |

따라서 이 논문의 핵심 성취는 `수백 개를 이미 이식했다`가 아니라, 분산 칩을 하나의 무선 네트워크로 묶는 전체 경로를 실제 ASIC과 동물에서 닫았다는 데 있다.

## 읽으며 든 질문

- 자유 발진기 편차와 충돌을 줄이려면 노드가 늘수록 downlink·스케줄러가 복잡해진다. 네트워크 규모와 칩 단순성 사이의 최적점은 어디인가?
- 48개 기록은 쥐 해부학이 정한 규모다. 더 큰 피질에서 WPT 균일도와 near–far 문제가 주소 충돌보다 먼저 한계가 될 수 있다.
- 기록과 자극 기능은 같은 플랫폼에 있지만 완전한 만성 폐루프를 한 시스템에서 시연한 것은 아니다.

## 이후 연구와 연결

- [[asbit-wireless-sensor-network|ASBIT]]는 고정 TDMA 대신 희소 사건과 Gold code를 사용해 기록 uplink의 확장성을 밀어붙였다.
- [[patterned-wireless-brain-stimulation|패턴형 무선 뇌 자극]]은 자극 쪽을 30개 만성 이식과 행동 실험으로 확장했다.
- [[on-chip-fuse-programming|on-chip fuse programming]]은 칩 주소와 회로 파라미터를 제작 뒤에 바꾸는 방법을 다룬다.

## 참고 자료

- J. Lee et al., "Neural recording and stimulation using wireless networks of microimplants," _Nature Electronics_ 4, 604–614 (2021). [원문](https://www.nature.com/articles/s41928-021-00631-8)
