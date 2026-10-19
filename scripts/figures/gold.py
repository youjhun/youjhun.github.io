"""길이 31(n = 5) Gold code를 만든다. 정합 필터·논문 그림이 같이 쓴다.

선호 쌍(preferred pair)인 최대 길이 수열(m-sequence) U, V를 LFSR로 만든다.
U와 V를 k = 0..30칸 돌려 XOR한 31개에 U, V 자신을 더한 33개가 한 Gold code 묶음이다.
묶음 안 어느 두 부호의 주기 상호상관도 {-1, -t(n), t(n)-2} 세 값만 갖는다. n = 5이면 t = 9.
"""

import numpy as np

N_BITS = 5
LENGTH = 2**N_BITS - 1  # 31


def m_sequence(taps, n=N_BITS):
    """피보나치 LFSR. taps는 귀환에 쓰는 단(1부터 셈)."""
    state = [1] * n
    out = []
    for _ in range(2**n - 1):
        out.append(state[-1])
        fb = 0
        for t in taps:
            fb ^= state[t - 1]
        state = [fb] + state[:-1]
    return np.array(out)


# x^5 + x^2 + 1 과 x^5 + x^4 + x^3 + x^2 + 1 (n = 5의 선호 쌍)
U = m_sequence([5, 2])
V = m_sequence([5, 4, 3, 2])


def gold(k):
    """k번째 Gold code를 ±1 칩으로 돌려준다."""
    bits = U ^ np.roll(V, k)
    return 1 - 2 * bits


def periodic_xcorr(a, b):
    return np.array([np.dot(a, np.roll(b, s)) for s in range(len(a))])


if __name__ == "__main__":
    a, b = gold(3), gold(11)
    print("auto:", sorted(set(periodic_xcorr(a, a)[1:].tolist())))
    print("cross:", sorted(set(periodic_xcorr(a, b).tolist())))
