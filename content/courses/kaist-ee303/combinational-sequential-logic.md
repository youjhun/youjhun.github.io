---
title: 조합논리와 순차논리
aliases: [combinational logic, sequential logic, finite state machine]
tags: [EE303, 디지털설계]
date: 2026-10-20
description: 현재 입력만 보는 회로와 상태를 기억하는 회로를 분리하고 최소화와 상태기계를 연결한다.
---

> [!abstract] 한눈에
> 조합논리의 출력은 현재 입력만으로 결정된다. 순차논리는 현재 입력과 저장된 상태로 다음 상태와 출력을 만든다. 회로를 읽을 때 먼저 피드백과 저장소의 존재를 찾는다.

## 조합논리

불 함수는 진리표, 논리식, 게이트 회로로 표현할 수 있다. 카르노 맵이나 대수적 변형은 같은 함수를 더 적은 항과 게이트로 구현하도록 돕는다. 항 수 외에 지연, fan-out, 사용할 수 있는 게이트와 hazard도 고려해야 한다.

멀티플렉서는 선택 신호에 따라 입력 하나를 고르고, 디코더는 이진 코드를 여러 출력 중 하나로 펼친다. 가산기, 비교기, encoder 같은 블록을 조합하면 더 큰 데이터 경로를 만든다.

## 순차논리

순차회로는 상태 $q$를 가진다.

$$
q_{next}=F(q,input),\qquad output=G(q,input)
$$

플립플롭은 클록 경계에서 상태를 저장한다. 레지스터는 여러 비트를 함께 저장하고, 카운터는 정해진 전이 규칙을 반복한다.

유한상태기계에서는 상태가 무엇을 기억해야 하는지를 먼저 정하고 상태 전이도와 출력 규칙을 만든 뒤 인코딩과 논리식을 정한다. Moore 출력은 상태에만, Mealy 출력은 상태와 현재 입력에 의존한다.

## 피드백과 클록

조합회로의 피드백은 안정된 논리값을 보장하지 않으며 진동하거나 메타안정한 상태를 만들 수 있다. 순차회로는 저장소와 클록 규칙으로 피드백의 시간을 분리한다. 그래서 논리식이 맞는지뿐 아니라 [[timing-memory-rtl|타이밍 제약]]을 만족하는지도 검증해야 한다.


## 수 표현과 오버플로

부호 없는 $n$비트는 $0$부터 $2^n-1$까지 표현한다. 2의 보수는 $-2^{n-1}$부터 $2^{n-1}-1$까지 표현하며, 최상위 비트의 가중치가 음수다. 덧셈기의 carry-out과 signed overflow는 다른 조건이다. 같은 부호의 두 수를 더했는데 결과 부호가 반대라면 signed overflow를 의심한다. 고정 비트 폭의 덧셈을 무한 정밀도 정수 연산과 구분한다.

## 최소화와 조합 블록

드모르간 법칙으로 AND/OR와 반전을 바꿀 수 있다. 카르노 맵에서는 인접 칸의 한 비트 차이를 이용해 항을 합친다. Don't-care를 쓰려면 해당 입력이 실제로 발생하지 않거나 출력 규약에 허용된다는 근거가 필요하다. 논리식의 항 수를 줄여도 물리 배선과 fan-out 때문에 지연이 반드시 줄지는 않는다.

멀티플렉서로 불 함수를 구현하거나 decoder의 출력 조합으로 minterm을 구성할 수 있다. Ripple-carry 가산기의 carry는 단계별로 전달되어 지연이 누적된다. 병렬화된 carry 계산은 면적과 배선 비용을 늘릴 수 있다.

## 상태 설계

이력 중 미래 출력에 필요한 정보만 상태에 보존한다. 상태표에서 현재 상태·입력·다음 상태·출력을 분리하고, reset 뒤의 상태와 사용하지 않는 인코딩의 동작을 정한다. 이진 인코딩은 상태 비트를 줄이고 one-hot은 상태당 한 비트를 사용해 일부 논리를 단순화할 수 있지만, 어느 쪽이 유리한지는 구현에 따라 달라진다.

Enable이 있는 레지스터는 조건이 참일 때 새 값을 저장하고 그렇지 않으면 이전 값을 유지한다. Counter도 비트 폭, rollover, enable과 reset의 우선순위가 규약의 일부다. Level-sensitive latch와 edge-triggered flip-flop은 저장 시점이 다르다.


## 표현과 산술의 복원

이진수 $b_{n-1}\cdots b_0$의 unsigned 값은 $\sum_{k=0}^{n-1}b_k2^k$다. 2의 보수 signed 값은 $-b_{n-1}2^{n-1}+\sum_{k=0}^{n-2}b_k2^k$다. 예를 들어 4비트 `1101`은 unsigned로 13, signed로 −3이다. Signed 확장은 최상위 부호 비트를 복제하며, unsigned 확장은 0을 붙인다.

4비트에서 `0111 + 0011 = 1010`은 signed로 $7+3$의 범위를 넘어 −6으로 해석되며 overflow다. 반면 `1111 + 0001 = 0000`의 carry-out은 unsigned에서의 초과를 알리지만, signed의 $-1+1=0$에는 overflow가 없다. Signed 덧셈의 overflow는 같은 부호의 입력에서 출력 부호가 달라지는 조건으로 검사한다.

## 진리표에서 최소식

새 예제로 $F(A,B,C)=\sum m(1,3,6,7)$을 잡는다. 변수 순서를 A가 최상위, C가 최하위로 고정한다.

| A | B | C | F |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 0 | 1 | 1 |
| 0 | 1 | 0 | 0 |
| 0 | 1 | 1 | 1 |
| 1 | 0 | 0 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 0 | 1 |
| 1 | 1 | 1 | 1 |

카르노 맵은 Gray-code 순서로 인접 칸이 한 비트만 달라지게 놓는다. 1과 3을 묶으면 B가 사라져 $\overline A C$, 6과 7을 묶으면 C가 사라져 $AB$다. 따라서 $F=\overline A C+AB$다. 항을 합친 뒤 진리표의 모든 행으로 동치를 검산한다. 그룹 크기는 1,2,4,8처럼 2의 거듭제곱이고 가장자리끼리도 이어질 수 있다.

이 식은 A를 select로 쓰는 2:1 MUX에서 $D_0=C$, $D_1=B$로 구현할 수 있다. 일반적인 Shannon 전개 $F=\overline S F|_{S=0}+S F|_{S=1}$를 사용한 것이다.

## 전파 지연과 hazard

$B=C=1$일 때 위 식의 출력은 A와 무관하게 1이다. 그러나 A의 직접 경로와 반전 경로의 지연이 다르면 A가 바뀔 때 출력이 잠깐 0이 되는 static-1 hazard가 생길 수 있다. Consensus 항 $BC$를 추가한 $F=\overline A C+AB+BC$는 이상 논리값을 바꾸지 않으면서 이 두 단계 AND–OR 구현의 해당 단일 입력 전이 hazard를 덮을 수 있다. 실제 매핑과 다중 입력 동시 전이까지 모든 glitch를 보증하는 방법은 아니다.

## 가산기의 구성

Full adder의 입력 A,B,$C_{in}$에 대해 sum은 $A\oplus B\oplus C_{in}$이고 carry는 $AB+AC_{in}+BC_{in}$다. 입력 3비트의 합을 2비트 출력으로 표현하는 회로다. Ripple-carry 구조는 각 자리의 carry가 다음 자리로 전파되므로 최악 경로가 여러 자리를 지난다.

다음은 과제에서 옮기지 않고 만든 조합논리 예다. 폭을 명시해 carry를 버리지 않는다.

```systemverilog
module full_adder_ref (
    input  logic a, b, cin,
    output logic sum, cout
);
    assign {cout, sum} = {1'b0, a} + {1'b0, b} + {1'b0, cin};
endmodule
```

검산은 8개 입력 조합에 대해 `{cout,sum}`의 unsigned 값이 `a+b+cin`인지 확인한다. 게이트식에서 XOR를 OR로 바꾸면 A=B=1인 조합 등에서 결과가 달라진다.

## 상태표에서 동기회로

새 예제는 입력 din이 두 클록 이상 연속 1이면 hit를 1로 유지하고, 0을 받으면 해제하는 Moore 기계다. 상태는 IDLE(직전 0 또는 초기), ONE(연속 1을 한 번 받음), TWO(두 번 이상 받음)다. din은 클록에 동기화되어 setup/hold를 만족한다고 가정한다.

| 현재 상태 | din=0의 다음 상태 | din=1의 다음 상태 | 현재 상태의 hit |
| --- | --- | --- | --- |
| IDLE | IDLE | ONE | 0 |
| ONE | IDLE | TWO | 0 |
| TWO | IDLE | TWO | 1 |

다음 코드는 동기 active-high reset을 사용한다. `always_comb`는 next state만 계산하고, `always_ff`가 양의 클록 에지에서 상태를 저장한다. default는 사용하지 않는 인코딩의 복귀를 정의한다.

```systemverilog
module consecutive_high_ref (
    input  logic clk, reset, din,
    output logic hit
);
    typedef enum logic [1:0] {IDLE, ONE, TWO} state_t;
    state_t state, next_state;

    always_comb begin
        next_state = IDLE;
        case (state)
            IDLE: next_state = din ? ONE : IDLE;
            ONE:  next_state = din ? TWO : IDLE;
            TWO:  next_state = din ? TWO : IDLE;
            default: next_state = IDLE;
        endcase
    end

    always_ff @(posedge clk) begin
        if (reset) state <= IDLE;
        else       state <= next_state;
    end

    assign hit = (state == TWO);
endmodule
```

## 에지별 추적

Reset을 한 번 적용한 뒤 din을 1,1,0,1,1 순서로 표본화하면 에지 직후 상태는 ONE,TWO,IDLE,ONE,TWO이고 hit는 0,1,0,0,1이다. 두 번째 1이 에지에서 받아들여진 뒤 hit가 올라간다. Mealy 식 `hit=(state==ONE)&&din`은 에지 전 입력에도 반응할 수 있어 지연과 출력 규약이 다르다.

상태부의 reset을 동기에서 비동기로 바꾸려면 sensitivity와 reset 해제 조건도 바뀐다. 입력이 실제 버튼이면 동기화와 debounce가 추가로 필요하며, 이 예제는 그 기능을 포함하지 않는다.

## 설계 순서

입출력 규약과 관측 에지를 문장으로 정한다. 과거 입력 중 보존할 정보만 상태로 정하고 상태표를 만든다. Reset과 사용하지 않는 상태를 정의한 뒤, 조합 next-state와 순차 state register를 나누어 쓴다. 짧은 정상 입력뿐 아니라 reset·유지·연속 입력을 에지별로 추적한다. 기능 확인 뒤에는 합성·타이밍 검증을 별도로 수행한다.

## 유의점

- 논리식의 동치와 전파 지연까지 포함한 파형의 동치를 구분한다.
- Mealy 출력은 입력의 조합 지연과 glitch 영향을 받을 수 있다.
- 조합논리에서 누락된 할당으로 생기는 latch를 의도적인 상태 저장과 혼동하지 않는다.

## 관련 개념

- [[timing-memory-rtl|시간 제약과 RTL]]

## 참고 자료

- 개인 학습 기록, Notion `Studies / 2024 Spring / EE303 디지털시스템설계`, Boolean Algebra, Logic Minimization, Combinational and Sequential Logic
