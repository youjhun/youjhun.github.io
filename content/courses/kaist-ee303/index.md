---
title: EE303 디지털 시스템 설계
description: 불 대수와 조합논리에서 순차논리, 메모리, RTL과 ASM으로 이어지는 디지털 설계 과목 기록.
aliases: [EE303]
---

디지털 시스템을 ‘0과 1로 된 회로’라고만 보면 타이밍과 상태를 놓친다. 이 과목은 논리식을 회로로 바꾸는 조합논리에서 시작해, 클록과 저장소가 있는 순차논리, RTL 수준의 시스템 설계로 확장한다.

## 설계와 검산

| 작업 | 본문 |
| --- | --- |
| 비트열의 signed/unsigned 해석 | [[combinational-sequential-logic#표현과-산술의-복원\|2의 보수·overflow]] |
| 진리표를 논리식·MUX로 변환 | [[combinational-sequential-logic#진리표에서-최소식\|카르노 맵 계산 예]] |
| 논리식은 맞는데 glitch 발생 | [[combinational-sequential-logic#전파-지연과-hazard\|경로 지연·consensus]] |
| 상태표에서 RTL 작성 | [[combinational-sequential-logic#상태표에서-동기회로\|Moore 기계와 코드]] |
| 최대 클록과 hold 위반 | [[timing-memory-rtl#도착시각에서-부등식-구성\|Skew 포함 유도]] · [[timing-memory-rtl#시간-예산-계산-예\|Slack 계산]] |
| 같은 에지의 대입 의미 | [[timing-memory-rtl#nonblocking-assignment의-시간-의미\|이전 값과 갱신 값]] |
| 메모리 읽기·쓰기 규약 | [[timing-memory-rtl#메모리의-표본화-규약\|Read-first RTL와 추적]] |

## 단원

| 축          | 단원                                 | 공개 글                          |
| ----------- | ------------------------------------ | -------------------------------- |
| 표현        | 수 체계, 불 대수, 논리 최소화        | [[combinational-sequential-logic\|조합논리와 순차논리]] |
| 조합논리    | 조합회로 설계                        | [[combinational-sequential-logic\|조합논리와 순차논리]] |
| 상태 | 순차회로, 레지스터, 카운터 | [[combinational-sequential-logic\|상태표와 FSM]] · [[registers-counters-asm\|래치·여기표·시프트·modulo 카운터]] |
| 시간        | setup/hold, 타이밍 분석              | [[timing-memory-rtl\|타이밍·메모리·RTL]]   |
| 저장과 구현 | 메모리, programmable logic, RTL, ASM | [[timing-memory-rtl\|타이밍·메모리·RTL]] · [[registers-counters-asm\|ASM과 데이터 경로]] |

## 강의 목록과의 대응

| 강의 묶음 | 연결 글 | 세부 대조 |
| --- | --- | --- |
| L1 수 체계 | [[combinational-sequential-logic\|수 표현과 산술]] | signed·unsigned·overflow 계산 |
| L2–3 Boolean·최소화 | [[combinational-sequential-logic\|진리표·최소식·hazard]] | 한 함수의 진리표·MUX 변환 |
| L4 조합회로 | [[combinational-sequential-logic\|가산기와 조합 블록]] | 새 가산기 RTL |
| L5 순차회로 I–III | [[registers-counters-asm\|저장소·여기표]] · [[combinational-sequential-logic\|FSM]] | 상태표·에지 추적 |
| L6 레지스터·카운터·시간 | [[registers-counters-asm\|시프트·카운터]] · [[timing-memory-rtl\|타이밍]] | reset·enable·setup/hold |
| L7 메모리·programmable logic | [[timing-memory-rtl\|메모리 RTL]] · [[registers-counters-asm\|구현 자원]] | read-first·용량·LUT |
| L8 RTL·ASM | [[registers-counters-asm\|제어와 데이터 경로]] | 조건 분기·누산기 규약 |
| L9 Special Design | 세부 주제 미확인 | 제목만 확인했고 내용 완료로 세지 않음 |

> [!note] 근거
> 2024 Spring `Studies / EE303 디지털시스템설계`의 단원 목록과 Verilog SRAM 기록을 확인했다. 첨부 강의 전체는 확인하지 못했으며 공개 RTL 예제는 새로 작성했다.
