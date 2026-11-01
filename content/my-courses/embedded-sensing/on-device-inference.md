---
title: 기기 안 추론을 설계하는 법
aliases: [TinyML, Edge AI]
tags: [Embedded Sensing, Machine Learning]
date: 2026-10-21
description: 센서 기기에서 모델의 정확도와 메모리·연산·지연·에너지를 함께 맞추는 절차.
---

> [!abstract] 한눈에
> 기기 안 추론(on-device inference)은 센서 입력을 제한된 메모리·전력·시간 안에서 처리하는 과정이다. 모델 가중치 외에도 입력 버퍼, 중간 activation, 전처리 상태와 runtime이 필요하다. 검증 대상은 연속 신호가 들어오는 전체 처리 경로다.

## 저장 공간과 실행 메모리

Flash에는 프로그램과 상수 가중치를 둘 수 있고, RAM에는 입력·중간 결과·변하는 상태를 둔다. 모델 파일이 Flash에 들어가도 실행할 때 RAM이 부족할 수 있다. 반대로 가중치를 RAM으로 복사하는 구현은 두 공간을 모두 사용한다.

설계 연습으로 가중치 20,000개, 8채널·500 Hz·1초 float32 입력, 중간 activation 최대 24,000 byte를 가정한다.

| 항목                   | 크기        | 확인할 조건                            |
| ---------------------- | ----------- | -------------------------------------- |
| float32 가중치         | 80,000 byte | 상수로 Flash에서 읽을 수 있는가        |
| int8 가중치            | 20,000 byte | scale·bias·파일 metadata는 별도다      |
| 입력 창                | 16,000 byte | 원자료와 모델 입력을 중복 보관하는가   |
| 중간 activation        | 24,000 byte | 동시에 살아 있는 tensor의 최대값인가   |
| 입력과 activation의 합 | 40,000 byte | stack·runtime·DMA·필터 상태는 제외했다 |

입력과 activation을 별도 버퍼에 둔 이 예에서 가중치만 int8로 줄여도 위 RAM 합은 그대로다. 실제 runtime이 tensor 메모리를 재사용하면 할당 구조가 달라지므로 실행 중 최대 사용량을 측정한다. 숫자는 특정 모델의 실측값이 아니다.

## 정수 양자화

균일한 affine quantization은 실수 $x$와 정수 $q$를 scale $s>0$, zero-point $z$로 연결한다.

$$x\approx s(q-z),\qquad q=\operatorname{clip}\left(\operatorname{round}(x/s)+z\right)$$

예를 들어 $s=0.02$, $z=-3$이면 $x=0.10$은 $q=2$가 된다. int8 범위를 벗어난 입력은 잘리므로 학습 때 드물던 큰 아티팩트가 들어오면 오차가 커질 수 있다. ADC의 물리 전압 양자화와 모델 tensor의 양자화는 서로 다른 단계다.

대표 입력으로 activation 범위를 정할 때는 훈련 자료에서 실제 전처리를 거친 창을 사용한다. test 자료로 범위를 조정하면 평가 정보가 배포 설정에 들어간다. 정수 곱셈의 누적과 bias가 더 넓은 정수형을 사용할 수 있으므로 모든 데이터가 1 byte가 된다고 계산하지 않는다.

## 전처리와 모델의 계약

센서에서 모델까지 다음 조건을 함께 고정한다.

- 채널 순서, 단위, 전극 기준과 표본화 주파수
- 필터 계수, 초기 상태, warm-up 구간과 결측 처리
- 창 길이와 갱신 간격, 정규화 상수
- 입력 tensor의 shape·dtype·scale·zero-point
- 출력의 의미, 문턱, 연속 판정 횟수와 상태 초기화 조건

학습에서 앞뒤로 거르는 zero-phase 필터를 썼다면 미래 표본이 없는 스트리밍 구현과 출력이 달라진다. IIR 필터를 창마다 초기화하면 창 경계에 과도응답이 반복되므로 연속 입력에서는 상태 유지 방식을 확인한다.

## 처리 시간과 에너지

모델의 multiply-accumulate 횟수가 같아도 메모리 접근과 지원 kernel에 따라 실행시간이 달라진다. 전처리·추론·후처리 시간을 따로 재고, [[system-budgets-latency-power|갱신 간격]] 안에 처리가 끝나는지 확인한다. DMA와 CPU가 같은 버퍼를 동시에 수정하지 않도록 소유권도 정한다.

에너지는 $E=\int P(t)dt$로 계산한다. sleep 기준 대비 추론의 추가 에너지 $E_{\mathrm{extra}}$를 재었다면, 초당 추론 횟수 $f_{\mathrm{infer}}$에서 평균 기여는 $E_{\mathrm{extra}}f_{\mathrm{infer}}$다. 가상 측정값 0.2 mJ/inference를 초당 10번 실행하면 2 mW가 추가된다.

## 경량화 방법

| 방법                   | 줄이려는 비용                 | 확인할 조건                         |
| ---------------------- | ----------------------------- | ----------------------------------- |
| int8 quantization      | 가중치·activation과 연산 비용 | 정수 kernel 지원, clipping과 정확도 |
| pruning                | 연결 수                       | sparse 표현과 연산 지원             |
| distillation           | 작은 모델의 성능 손실         | 작은 모델 자체의 메모리·지연        |
| 특징 기반 선형 모델    | 신경망의 계산과 메모리        | 특징 계산·정규화까지 포함한 비용    |
| event-driven inference | 실행 횟수                     | trigger의 소비와 사건 누락          |

불규칙하게 0이 많아져도 dense kernel을 그대로 쓰면 속도가 거의 줄지 않을 수 있다. 간단한 선형 모델을 기준선으로 두면 복잡한 모델의 추가 성능이 비용에 맞는지 비교할 수 있다.

## 스트리밍 검증

같은 원자료를 PC와 기기에 차례로 넣어 전처리 결과, 모델 입력, 출력 점수를 대조한다. 양자화 전후의 수치 오차가 허용 범위에 있는지 확인한 뒤 실제 연속 입력으로 넘어간다.

겹치는 창들은 독립 표본이 아니므로 새 사용자나 새 세션에 대한 평가에서는 그 단위로 분리한 뒤 창을 만든다. 전처리 상수와 모델을 함께 고정한 test stream에서 사건별 검출률, false alarm/hour, 검출 지연, 버퍼 손실과 평균 전력을 잰다. 시작 직후, 긴 결측 뒤 복귀, 아티팩트 구간도 따로 확인한다.

## 유의점

- 모델 파일 크기로 최대 RAM 사용량을 추정하지 않는다.
- 짧게 자른 창의 정확도만으로 연속 사용의 오경보 빈도를 판단하지 않는다.
- calibration 자료의 범위가 좁으면 실제 입력이 정수 범위를 넘어갈 수 있다.
- runtime과 연산 지원은 배포할 버전을 기준으로 확인한다.

## 관련 개념

- [[system-budgets-latency-power|전력·지연·데이터율 예산]]
- [[quantization-adc|양자화와 ADC]]
- [[projects/data-leakage|생체신호 데이터 누수]]
- [[projects/event-driven-neural-decoding|이벤트 기반 신경 디코딩]]

## 참고 자료

- Google AI Edge, [LiteRT for Microcontrollers](https://developers.google.com/edge/litert/microcontrollers/overview), [Build and convert models](https://developers.google.com/edge/litert/microcontrollers/build_convert).
- Google AI Edge, [LiteRT 8-bit quantization specification](https://developers.google.com/edge/litert/conversion/tensorflow/quantization/quantization_spec): scale·zero-point와 정수형 조건.
- 메모리·양자화·에너지의 수치 예제는 직접 정한 조건으로 계산했다.
