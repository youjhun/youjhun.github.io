---
title: 타이밍·메모리·RTL
aliases: [setup time, hold time, RTL, SRAM]
tags: [EE303, 디지털설계, Verilog]
date: 2026-10-20
description: 레지스터 사이 경로의 시간 예산, 메모리의 읽기·쓰기 규약과 RTL 기술의 관계.
---

## 레지스터 사이의 시간 예산

동기식 경로는 출발 레지스터의 clock-to-Q 지연, 조합논리 지연, 도착 레지스터의 setup time을 한 클록 주기 안에 담아야 한다.

$$
T_{clk}\ge t_{cq}+t_{comb}+t_{setup}+t_{skew}
$$

hold time은 같은 클록 경계 직후 입력이 너무 빨리 바뀌지 않아야 한다는 최소 지연 조건이다. 클록 주기를 늘리면 setup 위반은 완화할 수 있지만 hold 위반은 일반적으로 해결되지 않는다.

## 메모리는 동작 규약까지 설계한다

메모리를 주소와 데이터 배열로만 보면 동시에 읽고 쓸 때의 의미를 놓친다. 동기 읽기인지 비동기 읽기인지, 같은 주소에 read/write가 겹칠 때 old data·new data·undefined 중 무엇이 나오는지 명시해야 한다.

dual-port SRAM은 두 포트가 독립적으로 접근할 수 있지만 같은 주소 충돌 규칙이 필요하다. RTL 시뮬레이션이 원하는 값을 보여도 합성 대상 메모리 매크로의 실제 규약과 다를 수 있다.

## RTL은 회로의 시간 구조를 적는다

RTL은 매 클록에서 레지스터가 어떤 다음 값을 받는지와 그 사이 조합논리를 표현한다.

- 조합 블록은 모든 경로에서 출력이 할당되어야 의도치 않은 latch를 피한다.
- 순차 블록은 같은 클록과 reset 규칙을 일관되게 사용한다.
- blocking/nonblocking assignment는 단순 문법 취향이 아니라 시뮬레이션 의미에 영향을 준다.
- 테스트벤치는 정상 입력뿐 아니라 경계, reset, 동시 접근과 충돌을 검사한다.

ASM 차트는 상태 전이, 조건 판단과 레지스터 동작을 함께 보여 주어 제어부와 데이터 경로를 연결한다.

## 출처

- 개인 학습 기록, Notion `Studies / 2024 Spring / EE303 디지털시스템설계`, Timing Analysis, Memory, RTL, ASM, dual-port SRAM
