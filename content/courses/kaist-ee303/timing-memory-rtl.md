---
title: 타이밍·메모리·RTL
aliases: [setup time, hold time, RTL, SRAM]
tags: [EE303, 디지털설계, Verilog]
date: 2026-10-20
description: 레지스터 사이 경로의 시간 예산, 메모리의 읽기·쓰기 규약과 RTL 기술의 관계.
---

> [!abstract] 한눈에
> 레지스터 사이의 setup은 가장 늦은 데이터, hold는 가장 빠른 데이터의 도착을 제한한다. RTL의 에지별 갱신과 메모리 충돌 규약은 별도로 정한다. 기능·합성·타이밍 검증을 나누어 확인한다.

## 레지스터 사이의 시간 예산

동기식 경로는 출발 레지스터의 clock-to-Q 지연, 조합논리 지연, 도착 레지스터의 setup time을 한 클록 주기 안에 담아야 한다.

$$
T_{clk}\ge t_{cq}+t_{comb}+t_{setup}+t_{skew}
$$

hold time은 같은 클록 경계 직후 입력이 너무 빨리 바뀌지 않아야 한다는 최소 지연 조건이다. 클록 주기를 늘리면 setup 위반은 완화할 수 있지만 hold 위반은 일반적으로 해결되지 않는다.

## 메모리의 동작 규약

메모리를 주소와 데이터 배열로만 보면 동시에 읽고 쓸 때의 의미를 놓친다. 동기 읽기인지 비동기 읽기인지, 같은 주소에 read/write가 겹칠 때 old data·new data·undefined 중 무엇이 나오는지 명시해야 한다.

dual-port SRAM은 두 포트가 독립적으로 접근할 수 있지만 같은 주소 충돌 규칙이 필요하다. RTL 시뮬레이션이 원하는 값을 보여도 합성 대상 메모리 매크로의 실제 규약과 다를 수 있다.

## RTL과 회로의 시간 구조

RTL은 매 클록에서 레지스터가 어떤 다음 값을 받는지와 그 사이 조합논리를 표현한다.

- 조합 블록은 모든 경로에서 출력이 할당되어야 의도치 않은 latch를 피한다.
- 순차 블록은 같은 클록과 reset 규칙을 일관되게 사용한다.
- blocking/nonblocking assignment의 차이는 문법 취향에 그치지 않고 시뮬레이션 의미에 영향을 준다.
- 테스트벤치는 정상 입력뿐 아니라 경계, reset, 동시 접근과 충돌을 검사한다.

ASM 차트는 상태 전이, 조건 판단과 레지스터 동작을 함께 보여 주어 제어부와 데이터 경로를 연결한다.


## Setup과 hold의 부호

Capture clock 도착시각에서 launch clock 도착시각을 뺀 값을 $s$로 정의하면, jitter 등을 제외한 setup 조건은 $T\ge t_{cq,max}+t_{comb,max}+t_{setup}-s$다. Hold 조건은 $t_{cq,min}+t_{comb,min}\ge t_{hold}+s$다. Capture clock이 늦으면 setup에는 유리하고 hold에는 불리하다. 앞 절의 $t_{skew}$는 보수적인 불리한 skew 예산이며, 부호 있는 $s$와 같은 변수로 사용하지 않는다.

최대 지연과 최소 지연은 다른 코너에서 평가될 수 있다. 논리 단계를 줄여 속도를 높인 경로가 hold 위반을 만들 수도 있다. 다른 클록 도메인이나 비동기 입력에는 setup/hold 계산 외에 동기화와 메타안정성 처리가 필요하다.

## 동시 메모리 접근

동일한 주소에 두 쓰기가 겹치면 우선순위, 금지 조건 또는 정의되지 않은 동작을 명시해야 한다. 한 포트가 쓰고 다른 포트가 읽을 때의 반환값도 별도 규약이다. 같은 always 블록의 nonblocking assignment 오른쪽은 해당 사건 시점의 값을 평가하므로 소스코드 줄 순서를 순차적 메모리 갱신으로 해석하면 안 된다.

서로 다른 always 블록이 같은 배열을 쓰는 표현은 시뮬레이터에서 동작하더라도 합성 대상이 지원하는 메모리 패턴인지 확인해야 한다. 레지스터 배열 구현과 전용 block RAM 추론은 면적과 타이밍이 다르다. 원본의 과제 코드를 복제하지 않고 동작 규약만 분석했다.

## 제어부와 데이터 경로

데이터 경로는 레지스터, 연산기와 선택기로 구성하고 제어부는 enable·select·write 등의 신호를 만든다. ASM에서는 상태 상자의 레지스터 동작, 판단 조건, 조건부 출력을 분리한다. 매 클록에 어디서 값이 저장되는지 명시하면 조합 계산과 상태 갱신의 경계를 확인할 수 있다.


## 도착시각에서 부등식 구성

출발 레지스터의 기준 에지를 0, 도착 레지스터의 같은 번호 에지를 $s$로 둔다. 다음 capture 에지는 $T+s$다. Setup에서 데이터의 가장 늦은 도착은 $t_{cq,max}+t_{comb,max}$이고, 요구시각은 $T+s-t_{setup}$이므로

$$
\mathrm{slack}_{setup}=T+s-t_{setup}-t_{cq,max}-t_{comb,max}\ge0.
$$

Hold는 같은 capture 에지 직후의 보호 조건이다. 새 데이터의 가장 빠른 도착이 $s+t_{hold}$보다 늦어야 하므로

$$
\mathrm{slack}_{hold}=t_{cq,min}+t_{comb,min}-s-t_{hold}\ge0.
$$

여기서는 단일 주기 경로, 해당 에지 간 skew와 이상적 uncertainty 0을 가정했다. 실제 STA에서는 setup/hold별 uncertainty, 경로별 clock latency와 공통 경로 보정 등이 포함될 수 있다.

## 시간 예산 계산 예

새 예의 단위를 ns로 맞추고 $T=10$, $s=0.20$, $t_{cq,max}=0.80$, $t_{comb,max}=7.50$, $t_{setup}=1.00$으로 둔다. Setup slack은 $10+0.20-1.00-0.80-7.50=0.90$ ns다. 이 경로만 보면 최소 주기는 9.10 ns, 최대 주파수는 약 109.9 MHz다.

같은 경로의 $t_{cq,min}=0.15$, $t_{comb,min}=0.10$, $t_{hold}=0.30$이면 hold slack은 $0.15+0.10-0.20-0.30=-0.25$ ns로 위반이다. 주기를 20 ns로 늘려도 hold 식에는 T가 없어 같은 위반이 남는다. 최소·최대 모두 0.30 ns인 이상적인 추가 지연을 가정하면 hold slack은 0.05 ns, setup slack은 0.60 ns가 된다. 실제 delay cell의 min/max는 같지 않으므로 양쪽을 다시 분석한다.

## Nonblocking assignment의 시간 의미

다음 두 줄은 같은 에지에서 오른쪽의 이전 값을 읽고, 이후 왼쪽을 갱신한다.

```systemverilog
always_ff @(posedge clk) begin
    a <= din;
    b <= a;
end
```

초기 a=b=0이고 첫 에지에서 din=1이면 에지 후 a=1,b=0이다. 다음 에지에서 din=0이면 a=0,b=1이다. `b`가 같은 에지에서 새 a를 읽는다고 해석하지 않는다. Blocking `=`은 절차 안에서 즉시 값을 갱신하므로 코드를 그대로 바꾸면 시뮬레이션 의미와 의도한 레지스터 연결이 달라질 수 있다.

조합 블록에서는 출력과 임시값에 기본값을 먼저 주거나 모든 분기를 완전히 할당한다. `if(en) y=d;`만 쓰면 en=0일 때 y를 유지해야 해서 latch가 추론될 수 있다. 순차 블록에서 조건이 거짓일 때 레지스터를 유지하는 것은 의도된 enable 규약일 수 있다.

## 메모리의 표본화 규약

아래는 새로 작성한 8×8 단일포트 동기 메모리 예다. 매 에지에 주소가 표본화되고 old data가 dout으로 나온다. 같은 에지에서 we=1이면 그 주소의 메모리를 새 값으로 갱신한다. 배열과 dout의 초기값은 정의하지 않았다.

```systemverilog
module read_first_ram_ref (
    input  logic       clk, we,
    input  logic [2:0] addr,
    input  logic [7:0] din,
    output logic [7:0] dout
);
    logic [7:0] mem [0:7];
    always_ff @(posedge clk) begin
        dout <= mem[addr];
        if (we) mem[addr] <= din;
    end
endmodule
```

쓰기 전 `mem[3]=8'h12`라고 가정하고 addr=3,we=1,din=`8'hA5`를 적용하면 그 에지 직후 dout은 `12`, 저장값은 `A5`다. 다음 에지에 같은 주소를 읽으면 dout은 `A5`다. Reset 없이 아직 쓰지 않은 주소를 읽으면 정해진 0이 나온다고 가정하지 않는다.

이 예의 RTL read-first 의미와 특정 FPGA의 block RAM 추론 가능성은 구별한다. Write-first, no-change와 dual-port 충돌은 해당 장치·매크로의 규약을 확인한다. 읽기 레지스터만 reset하는 것과 전체 배열을 reset하는 것도 하드웨어 비용과 추론 결과가 다르다.

## Programmable logic와 데이터 경로

FPGA의 LUT는 작은 입력 조합함수를 저장된 진리표로 구현하고, flip-flop과 배선·메모리 자원으로 상태와 연결을 만든다. RTL의 `for` 반복문이 고정 범위에서 합성되면 여러 하드웨어 복제나 조합망으로 전개될 수 있으며, 소프트웨어처럼 루프 한 번당 클록 하나가 자동으로 생기지는 않는다.

레지스터 사이에 연산을 나누는 pipelining은 한 단계의 조합 지연을 줄일 수 있지만 latency와 레지스터 수, 제어 신호 정렬을 바꾼다. 처리율과 한 입력의 완료시간을 구분한다. ASM에서는 매 상태에서 어떤 enable과 select가 정해지고 어느 에지에서 값이 저장되는지 표시한다.

## 검증 순서

기능 시뮬레이션에서는 에지 이전의 입력, 에지 이후의 출력·상태를 분리해 관측한다. Reset·enable·경계 주소·동시 read/write·초기화되지 않은 메모리를 다룬다. 합성 후에는 latch·다중 드라이버·예상한 메모리 추론 여부를 확인하고, STA에서 최대경로 setup과 최소경로 hold를 각각 확인한다. 본문의 RTL은 동작 규약 설명용이며 파형 추적과 합성 도구 검증은 서로 대체되지 않는다.

## 유의점

- Hold는 클록 주기만 늘려 해결하는 제약이 아니다.
- Reset의 동기·비동기 방식과 해제 시점을 함께 정한다.
- RTL의 기능 시뮬레이션 통과가 합성 후의 타이밍 통과를 보장하지 않는다.

## 관련 개념

- [[combinational-sequential-logic|상태와 조합논리]]

## 참고 자료

- 개인 학습 기록, Notion `Studies / 2024 Spring / EE303 디지털시스템설계`, Timing Analysis, Memory, RTL, ASM, dual-port SRAM
- [AMD UG949, Reviewing Timing Slack](https://docs.amd.com/r/en-US/ug949-vivado-design-methodology/Reviewing-Timing-Slack), capture minus launch의 clock-skew 정의 및 setup/hold 분석.
- Intel Quartus Prime Design Recommendations, 동기 메모리와 read-during-write 규약. RTL 코드는 원본 과제를 재사용하지 않고 별도로 작성했다.
