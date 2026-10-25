---
title: "논문 리뷰: 분산 무선 칩으로 패턴형 뇌 자극하기"
aliases: [Patterned electrical brain stimulation by a wireless network of implantable microdevices]
tags: [논문, 신경자극, BCI, 무선전력]
date: 2026-10-20
description: 30개 무선 microstimulator를 쥐 피질에 만성 이식해 공간·시간 패턴 자극과 행동 반응을 보인 연구.
---

> [!abstract] 한눈에
> BCI가 뇌에서 읽는 것만 아니라 감각을 다시 써 넣으려면 여러 피질 지점에 정교한 자극 패턴을 보내야 한다. 이 논문은 30개의 독립 무선 microstimulator를 쥐 피질에 3개월 이식하고, 저듀티 RF 명령으로 칩마다 자극 진폭·위상폭·반복률을 정해 행동 변화를 만들었다.

|      |                                                                                          |
| ---- | ---------------------------------------------------------------------------------------- |
| 제목 | Patterned electrical brain stimulation by a wireless network of implantable microdevices |
| 게재 | _Nature Communications_ 15, 10093 (2024)                                                 |
| DOI  | [10.1038/s41467-024-54542-1](https://doi.org/10.1038/s41467-024-54542-1)                 |

## Neurograin 이후 달라진 점

2021년 [[neurograin-wireless-microimplants|Neurograin]] 논문은 분산 칩 네트워크에서 기록과 자극 가능성을 보였다. 이 연구는 자극 기능에 집중해 세 가지를 확장했다.

1. 자극 전류를 최대 $120\ \mu A$ peak-to-peak biphasic current로 키웠다.
2. 칩당 3 μs에 자극 파라미터를 설정하는 collision-free daisy-chain protocol을 만들었다.
3. 30개 칩을 자유행동 쥐에 3개월 만성 이식해 행동 과제까지 연결했다.

## 칩과 통신

칩은 65 nm RF CMOS로 만들고 선형 크기 300–500 μm다. 외부 약 1 GHz RF에서 전력을 얻고, 100 μm 간격의 tungsten microwire 한 쌍으로 피질에 biphasic current를 주입한다.

downlink는 1 Mbps ASK-PWM으로 `sync + 칩별 3-bit command`를 보낸다. 명령은 전류 진폭, phase당 지속 시간, 반복률의 조합을 고른다. 자극이 필요할 때만 RF를 켜므로 연속 전력 방식보다 평균 노출을 크게 줄인다.

`daisy-chain`이라는 이름과 달리 칩들은 선으로 연결되지 않는다. 미리 정한 순서대로 각 칩의 짧은 command slot을 이어 보내는 무선 register-mapping 방식이다.

## 실제 시연

- 급성 실험에서 선택한 칩의 국소 자극이 피질 LFP와 spike response를 유발했다.
- motor cortex 자극으로 머리 움직임, 여러 칩 동시 자극으로 whisker movement를 보였다.
- 30개 칩을 motor·sensory cortex에 만성 이식하고 lever discrimination 과제에서 자극 위치와 개수에 따른 행동 차이를 측정했다.
- 30개 동시 50 Hz 자극 조건에서 높은 정답률을 보였고, 낮은 duty cycle에서도 행동 효과가 유지됐다.

## 실측과 외삽

| 주장                        | 근거                             |
| --------------------------- | -------------------------------- |
| 30개 칩 만성 동작           | 실제 자유행동 쥐, 3개월          |
| 공간·시간 패턴 자극         | 급성·만성 동물 실험              |
| 1,000개 칩을 3 ms 안에 접근 | 칩당 3 μs protocol timing의 외삽 |
| 큰 동물·사람에서의 동작     | 아직 검증 전                     |

## 안전과 한계

저듀티 동작은 평균 RF power와 SAR을 낮추지만, 더 큰 뇌에서는 조직 두께와 면적 때문에 결합 효율이 떨어진다. 많은 칩을 배치할 수 있다는 통신 계산과 모든 칩에 안전하게 전력을 공급할 수 있다는 주장은 별개다.

전극 부착과 encapsulation도 남은 문제다. tungsten wire의 각도, epoxy 표면, 장기 조직 반응은 자극 위치와 전하 전달을 바꿀 수 있다. 논문은 신경과학의 최적 자극 코드를 찾은 연구라기보다, 그 코드를 탐색할 수 있는 기술 플랫폼의 proof of concept에 가깝다.

## 읽으며 든 질문

- 칩 조합, 진폭, phase width, 반복률의 조합 공간을 행동 피드백으로 어떻게 효율적으로 탐색할까?
- 여러 지점 동시 자극의 효과가 각 지점 효과의 합인지, 네트워크 상호작용인지 어떻게 분리할까?
- closed-loop BCI에서 기록 네트워크와 자극 네트워크의 clock·latency를 어떤 기준으로 묶어야 할까?

## 참고 자료

- A.-H. Lee et al., "Patterned electrical brain stimulation by a wireless network of implantable microdevices," _Nature Communications_ 15, 10093 (2024). [공개 원문](https://www.nature.com/articles/s41467-024-54542-1)
