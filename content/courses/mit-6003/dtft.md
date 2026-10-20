---
title: 이산시간 푸리에 변환 (DTFT)
aliases: [이산시간 푸리에 변환, Discrete-time Fourier transform]
tags: [신호처리, 6.003]
date: 2026-10-19
description: 숫자의 열을 주파수 성분으로 나누는 도구. 왜 스펙트럼이 2π마다 반복되고, 왜 가장 빠른 진동이 π인가.
---

> [!abstract] 한눈에
> 이산시간 신호 $x[n]$을 복소지수 $e^{j\omega n}$들의 합으로 분해해 주파수 $\omega$별 성분의 크기를 구하는 변환이 DTFT다. $n$이 정수여서 $\omega$와 $\omega + 2\pi$를 구별할 수 없으니 스펙트럼은 $2\pi$마다 반복되고, 실제로 볼 범위는 $-\pi$에서 $\pi$까지면 된다. 이산시간 신호는 $\omega = \pi$보다 빠르게 진동하지 못한다.

## 정의

신호 $x[n]$이 이산시간일 때 DTFT는 이렇게 정의한다.

$$
X(e^{j\omega}) = \sum_{n=-\infty}^{\infty} x[n]\, e^{-j\omega n}
$$

원래 신호로 되돌리는 식(역변환)은 한 주기 구간에서 적분한다.

$$
x[n] = \frac{1}{2\pi} \int_{-\pi}^{\pi} X(e^{j\omega})\, e^{j\omega n}\, d\omega
$$

역변환에서 $x[n]$은 $e^{j\omega n}$들의 가중합이고 각 항의 가중치가 $X(e^{j\omega})$다. 그 가중치를 뽑아내는 쪽이 정변환으로, $x[n]$과 $e^{j\omega n}$의 내적을 계산한다.

$\omega$는 **라디안/표본** 단위로 잰다. 이를 실제 주파수 $f$(Hz)로 환산할 때는 샘플링 주파수 $f_s$가 함께 있어야 한다.

$$
\omega = 2\pi \frac{f}{f_s}
$$

## 단위원

복소평면에서 $e^{j\omega}$는 반지름 1인 원 위에 놓인다. $\omega$를 0에서 $2\pi$까지 늘리면 이 점이 원을 한 바퀴 돌아 출발점에 돌아온다(그림 1). 이렇게 보면 DTFT는 z 변환의 값을 단위원 위에서만 읽은 것이다. 시스템 함수 $H(z)$에 $z = e^{j\omega}$를 대입한 결과가 주파수 응답 $H(e^{j\omega})$이고, 극점과 영점이 단위원의 어디에 가까이 있는지만 확인해도 어느 주파수가 커지고 어느 주파수가 작아질지 짐작할 수 있다.

![단위원과 주파수 ω](../../images/dtft/unit-circle.png)
*그림 1. 원의 오른쪽 끝이 $\omega = 0$, 왼쪽 끝이 $\omega = \pi$다. 한 바퀴를 다 돌면 출발한 점과 겹친다.*

## 2π 주기성

$n$이 정수일 때는 다음 등식이 늘 성립한다.

$$
e^{j(\omega + 2\pi)n} = e^{j\omega n} \cdot e^{j2\pi n} = e^{j\omega n}
$$

$\omega$로 만든 신호와 $\omega + 2\pi$로 만든 신호는 어느 표본을 골라도 값이 같다. 둘은 같은 신호이므로 DTFT에서도 한 성분으로 잡히고, $X(e^{j\omega})$는 $\omega$에 대해 주기가 $2\pi$인 함수가 된다. 길이 5인 사각 펄스로 그린 그림 2에서도 회색으로 칠한 한 주기 바깥은 같은 모양의 반복이다.

$$
x[n] = \begin{cases} 1 & 0 \le n \le 4 \\ 0 & \text{그 밖} \end{cases}
\quad\Longrightarrow\quad
X(e^{j\omega}) = e^{-j2\omega}\, \frac{\sin(5\omega/2)}{\sin(\omega/2)}
$$

![사각 펄스의 DTFT 크기](../../images/dtft/periodic-spectrum.png)
*그림 2. $\omega = 0$에서 $|X(e^{j\omega})|$의 값은 5(펄스의 합)이고 같은 모양이 $2\pi$마다 나타난다.*

[[sampling-aliasing|샘플링]]을 하면 스펙트럼 복사본이 $f_s$ 간격으로 생기는데, 이 반복도 같은 현상이다. 앞의 환산식에 $f = f_s$를 넣어 보면 $\omega = 2\pi$가 나온다.

## 가장 빠른 진동

연속시간 신호라면 주파수를 올리는 대로 진동이 끝없이 빨라진다. 이산시간 신호에서 $\cos(\omega n)$의 $\omega$를 0부터 올려 보면 $\pi$까지만 빨라지고 그 뒤로는 도로 느려진다(그림 3). $\omega = \pi$일 때 $\cos(\pi n) = (-1)^n$으로 부호가 표본마다 뒤집히는데, 이산시간에서 이보다 빠른 변화는 없다. $\omega = 7\pi/4$도 $-\pi/4$와 같은 점이어서 $\pi/4$만큼 느리게 진동한다.

![여러 ω에서 cos(ωn)](../../images/dtft/dt-frequencies.png)
*그림 3. $\omega = 0$, $\pi/4$, $\pi$, $7\pi/4$의 네 경우. 두 번째 줄과 마지막 줄의 신호가 같다.*

실제 주파수로 환산하면 $\omega = \pi$는 $f_s/2$로 나이퀴스트 주파수에 해당한다. 저역통과 필터를 설계할 때 '높은 주파수'가 $\pi$ 근처를, '낮은 주파수'가 0과 $2\pi$ 근처를 뜻하는 것도 이 때문이다.

## 컨볼루션과 곱셈

$e^{j\omega n}$을 LTI 시스템에 통과시키면 출력도 같은 복소지수이고 크기와 위상만 $H(e^{j\omega})$만큼 달라진다. 복소지수가 LTI 시스템의 **고유함수**라서 생기는 일이며, 이 성질 때문에 시간 영역에서 컨볼루션하던 것이 주파수 영역에서는 곱셈으로 바뀐다.

$$
y[n] = (x * h)[n] \quad\Longleftrightarrow\quad Y(e^{j\omega}) = X(e^{j\omega})\, H(e^{j\omega})
$$

필터가 어느 대역을 통과시키고 어느 대역을 막는지도 $|H(e^{j\omega})|$ 그래프 하나에서 읽어 낼 수 있다.

## 네 가지 푸리에 표현

시간 축이 연속인가 이산인가, 신호가 주기적인가 아닌가를 조합하면 푸리에 표현은 네 가지가 된다. 어느 것이든 한쪽 영역이 이산이면 반대쪽은 주기적이고, 한쪽이 주기적이면 반대쪽은 이산이다.

| | 시간 영역 | 주파수 영역 |
|---|---|---|
| 연속시간 푸리에 급수 (CTFS) | 연속, 주기적 | 이산, 비주기 |
| 연속시간 푸리에 변환 (CTFT) | 연속, 비주기 | 연속, 비주기 |
| 이산시간 푸리에 급수 (DTFS) | 이산, 주기적 | 이산, 주기적 |
| 이산시간 푸리에 변환 (DTFT) | 이산, 비주기 | 연속, 주기적 |

DTFT의 결과는 $\omega$의 연속 함수여서 컴퓨터에 그대로 넣을 수 없다. 대신 컴퓨터는 길이 $N$인 신호의 [[dft-fft|DFT]]를 계산하며, 그 값은 DTFT를 $\omega_k = 2\pi k / N$ 지점 $N$개에서 표본으로 뽑은 것과 같다. 이 DFT를 $N^2$번이 아니라 $N \log N$번 안팎의 연산으로 구하는 알고리즘을 **FFT**라 부른다. 결과는 DFT와 같고 계산만 빠르다.

## 자주 하는 오해

- **"$\omega$가 클수록 빠른 진동이다."** $\pi$까지만 맞는 말이다. $\pi$를 지나면 다시 느려지고 $2\pi$에 이르면 상수다.
- **"$-\pi$에서 $\pi$ 밖에도 다른 정보가 있다."** 없다. 그 바깥은 같은 한 주기의 반복이다.
- **"$\omega$의 단위는 Hz다."** 라디안/표본이다. $f_s$를 모르면 Hz로 바꿀 수 없어서 같은 $\omega = \pi/2$라도 $f_s$가 1 kHz면 250 Hz, 200 Hz면 50 Hz다.
- **"FFT와 DTFT는 같은 것이다."** DFT는 DTFT의 표본이고 FFT는 그 DFT를 빨리 계산하는 방법이다. 유한한 길이로 잘라서 계산하므로 해상도에 한계가 있고 누설(leakage)도 생긴다.

## 관련 개념

- [[sampling-aliasing|샘플링과 앨리어싱]]: 스펙트럼 복사와 $2\pi$ 주기성은 같은 현상
- [[dft-fft|DFT와 FFT]]: DTFT를 표본으로 뽑은 것, 컴퓨터가 실제로 계산하는 값
- [[z-transform|z 변환]]: 단위원 위의 값이 DTFT가 되는 더 넓은 변환
- [[matched-filter|정합 필터]]: 주파수 영역에서 보면 신호 스펙트럼의 켤레를 곱하는 필터

## 참고 자료

- MIT OCW, [6.003 Signals and Systems (Fall 2011)](https://ocw.mit.edu/courses/6-003-signals-and-systems-fall-2011/), Lecture 17 *Discrete-time frequency representations*, Lecture 18 *Discrete-time Fourier representations*, Lecture 19 *Relations among Fourier representations*
- A. V. Oppenheim, R. W. Schafer, *Discrete-Time Signal Processing*, 3rd ed., Ch. 2
