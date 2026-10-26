---
title: 저장소·레지스터·카운터·ASM
description: 래치와 플립플롭, 카운터의 다음 상태식과 제어·데이터 경로를 복원한다.
date: 2026-10-25
---

> [!abstract] 한눈에
> 래치는 활성 레벨 동안 입력을 통과시키고 플립플롭은 지정한 에지에서 표본화한다. 레지스터와 카운터는 다음 상태식, enable, reset 우선순위로 동작을 정한다. ASM은 상태별 제어와 조건부 동작을 데이터 경로의 저장 시점에 연결한다.

## 저장소의 특성식

| 저장소 | 입력 | 다음 저장값 | 제한 |
| --- | --- | --- | --- |
| active-high NOR SR latch | S,R | 00 유지, 10 설정, 01 해제 | 11은 금지 조합 |
| D latch | D,E | E=1이면 D, E=0이면 유지 | 활성 구간 동안 투명 |
| D flip-flop | D | 유효 에지에서 D | setup·hold 필요 |
| T flip-flop | T | $Q^+=Q\oplus T$ | 에지마다 토글 여부 결정 |
| JK flip-flop | J,K | $Q^+=J\overline Q+\overline KQ$ | 11이면 토글 |

SR의 금지 조합은 회로와 active 수준에 따라 달라진다. NOR active-high와 NAND active-low 표를 섞지 않는다. D latch를 에지 저장소처럼 사용하면 enable이 켜진 동안 조합 경로가 통과하는 효과를 놓친다.

## 여기표와 상태 설계

특성표는 입력에서 다음 Q를 구하고, 여기표는 원하는 $Q\to Q^+$를 만들 입력을 구한다. D flip-flop은 항상 $D=Q^+$다.

T flip-flop은 전이할 때만 T=1이므로 $T=Q\oplus Q^+$다. JK에서는 $0\to0$에 J=0,K=X, $0\to1$에 J=1,K=X, $1\to0$에 J=X,K=1, $1\to1$에 J=X,K=0이다. X는 그 전이에서 출력에 영향이 없는 선택값이다.

이후 상태표의 각 비트에 여기표를 적용하고 논리를 최소화한다. 사용하지 않는 상태를 don't-care로 처리하면 복구 동작이 없어질 수 있으므로 초기화 이후 도달 가능성과 오류 복구 요구를 먼저 정한다.

## Enable과 시프트 레지스터

동기 레지스터는 $Q^+=E D+\overline E Q$로 enable을 표현한다. 동기 reset의 우선순위가 가장 높으면 reset→load→shift→hold 순서처럼 동작을 정한다. 조합 입력을 바꿔 저장을 막는 clock enable과 클록 자체를 AND 게이트로 자르는 것은 타이밍·glitch 관점에서 다르다.

4비트 오른쪽 시프트의 한 규약은 $Q^+=\{serial\_in,Q[3:1]\}$다. 초기 `1010`에 serial_in을 1,0 순서로 넣으면 `1101`, `0110`이 된다. 시프트 방향은 도면의 좌우보다 비트 인덱스 식으로 정의한다. 병렬 load와 shift가 동시에 참일 때 어느 쪽이 우선인지도 정한다.

## 동기 이진 카운터

모든 비트가 같은 클록을 쓰는 unsigned 증가 카운터에서 최하위 비트는 매번 토글한다. 높은 비트는 아래 비트가 모두 1일 때 토글한다.

$$
T_0=1,\quad T_1=Q_0,\quad T_2=Q_1Q_0,\quad
Q_k^+=Q_k\oplus\prod_{j=0}^{k-1}Q_j.
$$

Enable E가 있으면 각 T식에 E를 곱한다. Ripple counter는 앞 비트 출력을 다음 클록으로 써 전이가 시간차로 전파된다. 여러 비트를 조합 디코딩할 때 중간 값과 glitch가 생길 수 있다. 동기 카운터도 출력들의 물리적 지연이 완전히 같다는 보장은 없으므로 조합 디코드의 관측 시점을 정한다.

## Modulo 카운터

새 예는 0–5를 세는 3비트 카운터다. 동기 reset이 최우선이고 enable=0에서는 유지한다. Enable=1에서 5 이상은 0으로 복귀해 미사용 코드 6,7도 처리한다.

```systemverilog
module mod6_reference (
    input logic clk, reset, enable,
    output logic [2:0] q
);
    always_ff @(posedge clk) begin
        if (reset) q <= 3'd0;
        else if (enable) begin
            if (q >= 3'd5) q <= 3'd0;
            else q <= q + 3'd1;
        end
    end
endmodule
```

Reset 이후 enable을 1,1,0,1,1,1,1로 주면 에지 직후 값은 1,2,2,3,4,5,0이다. Terminal count를 `q==5`로 조합 생성하면 q=5인 주기 동안 1이다. 그 주기 말에서 0으로 넘어가는 에지에만 한 번 사건을 만들려면 enable과 출력의 등록 규약을 함께 정의한다.

## ASM과 데이터 경로

ASM의 state box에는 상태가 유지되는 주기의 무조건 제어를, decision에는 조건을, conditional output에는 조건에 따른 제어를 둔다. 같은 ASM block의 조건 분기는 별도의 클록을 소비하지 않는다. 다음 상태로 이동하는 에지에서 레지스터가 갱신된다.

예로 입력 x 네 개를 받아 합하는 장치를 구성한다. 데이터 경로에는 10비트 누산기 A, 3비트 개수 C, 가산기와 enable을 둔다. 8비트 unsigned 네 개의 최대 합은 1020이어서 10비트가 필요하다. 새 입력은 valid가 참인 주기 끝에서만 받아들인다.

| 상태 | 그 주기의 제어 | 주기 말 전이 |
| --- | --- | --- |
| IDLE | start이면 A←0,C←0 | start이면 RUN |
| RUN | valid이면 A←A+x,C←C+1 | valid이고 기존 C=3이면 DONE, 아니면 RUN |
| DONE | done=1, 합 유지 | IDLE |

RUN에서 C=3인 에지에 네 번째 x도 합산한다. 조건은 갱신 전 C로 평가된다.

start와 함께 들어온 x는 IDLE 규약상 받지 않으므로 생산자가 RUN 이후부터 valid를 내도록 인터페이스를 정한다. valid=0이면 저장값과 카운트를 모두 유지한다. DONE은 한 주기이고 결과를 더 오래 유지할 필요가 있으면 완료 확인 신호를 추가한다.

입력 4,7,2,9를 중간 valid=0 주기와 함께 주어도 받아들인 값만 더해 22가 나와야 한다. 상태만 추적하고 A와 C를 따로 확인하지 않으면 마지막 입력 누락이나 한 주기 지연을 찾기 어렵다.

## 메모리와 구현 자원

ROM은 주소에서 저장된 값을 읽는 조합 또는 등록된 함수로, RAM은 쓰기 가능한 상태로 모델링한다. $2^a\times w$ 메모리는 주소 a비트, 데이터 w비트, 총 $2^aw$비트를 가진다. Read latency, enable, 동시 읽기·쓰기 규약은 용량과 별도로 정한다.

PLA는 programmable AND·OR 배열로 SOP를 구성하고, PAL은 배열의 프로그램 가능 구조가 다르다. FPGA는 LUT·flip-flop·배선·메모리 자원으로 논리를 매핑한다. 이들에서 같은 RTL 기능이 같은 면적·지연을 갖는다고 가정하지 않는다.

## 유의점

- 비동기 입력은 클록 도메인의 setup·hold를 자동으로 만족하지 않는다.
- 한 비트 동기화기는 다중 비트 버스의 원자적 전달이나 버튼 debounce를 보장하지 않는다.
- 카운터 폭, reset, wrap, hold를 각각 검증한다.

## 관련 개념

- [[combinational-sequential-logic|불 함수와 상태표]]
- [[timing-memory-rtl|Setup·hold·메모리 RTL]]

## 참고 자료

- Notion Studies / EE303 강의 목록, Sequential Logic I–III, Registers, Counters, RTL Design, ASM. 첨부 파일의 세부 사례 전체는 확인하지 못했다.
- [Steve Ward, Computation Structures, Sequential Logic](https://computationstructures.org/notes/sequential_logic/notes.html), latch와 에지 저장소의 공개 보충 자료.
- M. Morris Mano and Michael Ciletti, Digital Design, 순차회로·레지스터·카운터·ASM. 회로 규약과 예제는 별도로 작성했다.
