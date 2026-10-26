---
title: "Versatile On-Chip Programming of Circuit Hardware for Wearable and Implantable Biomedical Microdevices"
aliases: [Versatile On-Chip Programming, metal fuse, anti-fuse]
tags: [논문, ASIC, 신경공학, 회로]
date: 2026-10-20
description: 초소형 바이오 ASIC에 metal fuse와 anti-fuse를 넣고 laser·FIB로 제작 후 회로 파라미터를 편집하는 방법.
---

> [!abstract] 한눈에
> ASIC은 한 번 tape-out하면 회로가 고정된다. 이 논문은 칩의 최상층 금속에 fuse와 anti-fuse를 미리 배치하고, foundry 제작 뒤 laser로 끊거나 FIB로 이어서 주소·바이어스·RF 회로를 바꾸는 방법을 제안한다. SRAM이나 EEPROM 없이도 전력을 쓰지 않는 영구 설정을 얻는다.

|      |                                                                                                        |
| ---- | ------------------------------------------------------------------------------------------------------ |
| 제목 | Versatile On-Chip Programming of Circuit Hardware for Wearable and Implantable Biomedical Microdevices |
| 게재 | _Advanced Science_ 10, 2306111 (2023)                                                                  |
| DOI  | [10.1002/advs.202306111](https://doi.org/10.1002/advs.202306111)                                       |

## 필요성

초소형 배터리 없는 바이오 칩은 pad, 메모리, 디지털 제어기를 추가할 면적과 전력이 거의 없다. 그런데 실제 RF 결합, 전원, 아날로그 바이어스는 공정 편차와 사용 환경 때문에 첫 설계값만으로 맞지 않을 수 있다.

여러 버전을 다시 tape-out하는 대신 한 칩 안에 선택지를 넣어 두고 제작 뒤 필요한 연결만 남기면 개발 회전을 줄일 수 있다.

## 두 편집 연산

### Fuse로 연결 끊기

최상층 aluminium trace 위 passivation을 355 nm UV laser로 열고, 532 nm pulsed laser로 금속을 절단한다. 65 nm 공정의 설계 규칙에서 약 $3\times3\ \mu m$ 구조까지 다뤘다. 저자들은 주변 회로가 없는 영역에 fuse를 배치해 깊은 활성층 손상을 피했다.

### Anti-fuse로 연결 만들기

분리된 두 금속 노드 사이에 FIB로 platinum을 증착해 도통시킨다. 이미 끊은 fuse를 다시 연결하거나 원래 열린 선택지를 닫을 수 있다.

둘 다 칩이 켜진 동안 값을 바꾸는 firmware programming과 다르다. 현미경 장비로 물리 배선을 영구 편집하는 **post-foundry hardware programming**이다.

## 적용 사례

- 무선 EEG sensor의 analog front-end 파라미터 조정
- microstimulator 칩의 고유 주소 설정
- RF energy harvesting 회로의 동작점 선택
- supply voltage와 내부 회로 조건 최적화

설정 상태를 유지하는 데 정적 전력이 들지 않고, 별도 programming pad나 비휘발성 메모리를 크게 넣지 않아도 된다는 장점이 있다.

## 장점과 비용

| 장점                                  | 비용                                 |
| ------------------------------------- | ------------------------------------ |
| 매우 작은 면적과 0에 가까운 유지 전력 | 칩마다 물리 가공이 필요함            |
| tape-out 하나로 여러 회로 조합 탐색   | 자동화하지 않으면 대량 생산성이 낮음 |
| 주소·아날로그·RF를 같은 원리로 설정   | 재설정 횟수와 가역성이 제한됨        |
| 패키징 전 개별 보정 가능              | laser/FIB 장비와 정렬 공정이 필요함  |

## 읽으며 든 질문

- 연구용 소량 칩의 빠른 탐색에는 강하지만, 수천 개 노드에 각기 다른 설정을 새길 때 처리량은 어떻게 확보할까?
- 공정 편차를 보정하기 위한 fuse가 또 다른 가공 편차를 만들 수 있다. 편집 뒤 전기적 검증을 어느 수준까지 자동화할 수 있을까?
- PUF처럼 스스로 생긴 주소와 laser로 명시적으로 쓴 주소 중, 발견 비용·충돌 위험·추적 가능성을 어떻게 절충할까?

## 관련 논문

- [[neurograin-wireless-microimplants|Neurograin]]
- [[patterned-wireless-brain-stimulation|Patterned wireless brain stimulation]]

## 참고 자료

- A.-H. Lee et al., "Versatile On-Chip Programming of Circuit Hardware for Wearable and Implantable Biomedical Microdevices," _Advanced Science_ 10, 2306111 (2023). [원문](https://advanced.onlinelibrary.wiley.com/doi/10.1002/advs.202306111)
