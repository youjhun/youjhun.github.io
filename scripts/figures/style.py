"""모든 그림이 같은 글꼴·색·여백을 쓰게 하는 공통 설정.

그림은 흰 배경 PNG로 저장한다. 사이트의 다크 모드에서도 카드처럼 읽히게 하려는 것이다.
한글 라벨은 사이트 본문과 같은 Pretendard를 쓴다. 없으면 나눔고딕, 그다음 DejaVu Sans로 넘어간다.
Pretendard OTF는 npm 패키지 `pretendard`의 dist/public/static에 있다.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "content" / "images"

# 사이트 테마(quartz.config.ts)의 secondary·tertiary와 맞춘 색
BLUE = "#284b63"
TEAL = "#5f8f84"
RED = "#c0392b"
ORANGE = "#d68a2e"
GRAY = "#9a9a9a"
LIGHT = "#e9eef2"


def setup():
    plt.rcParams.update(
        {
            "font.family": ["Pretendard", "NanumGothic", "DejaVu Sans"],
            "axes.unicode_minus": False,
            "mathtext.fontset": "dejavusans",
            "savefig.dpi": 160,
            "figure.facecolor": "white",
            "axes.facecolor": "white",
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 12.5,
            "axes.titleweight": "bold",
            "axes.labelsize": 11,
            "font.size": 10.5,
            "axes.grid": True,
            "grid.color": "#ececec",
            "grid.linewidth": 0.8,
            "legend.frameon": False,
        }
    )


def save(fig, article, name):
    out = OUT / article
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / name, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"wrote {out / name}")


def pi_ticks(ax, lo, hi, step=1):
    """x축 눈금을 π 단위로 단다 (lo, hi, step은 π의 배수)."""
    import numpy as np

    ks = np.arange(lo, hi + step / 2, step)

    def label(k):
        k = round(k, 3)
        if k == 0:
            return "0"
        if k == 1:
            return "π"
        if k == -1:
            return "−π"
        if float(k).is_integer():
            return f"{int(k)}π".replace("-", "−")
        return f"{k}π".replace("-", "−")

    ax.set_xticks(ks * np.pi)
    ax.set_xticklabels([label(k) for k in ks])
