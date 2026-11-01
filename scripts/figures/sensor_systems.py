"""Illustrative sensor budgets and phase detection; not measured device data."""
import numpy as np
import matplotlib.pyplot as plt
from style import BLUE, TEAL, GRAY, setup, save

setup()

# Sequential stages after the last sample; start-up acquisition is separate.
fig, axes = plt.subplots(1, 2, figsize=(10, 3.5))
ax = axes[0]
labels = ['Sensor + AFE', 'CPU (average)', 'Radio (average)']
radio = 0.112 * 30 + 0.888 * 0.03
ax.bar(labels, [5, 2, radio], color=[BLUE, TEAL, GRAY])
ax.set_ylabel('Average power (mW)')
ax.set_title('Load power budget')
for i, value in enumerate([5, 2, radio]):
    ax.text(i, value + 0.1, f'{value:.2f}', ha='center')
ax.set_ylim(0, 6)
ax = axes[1]
left = 0
for duration, label, color in zip([5, 12, 8], ['Preprocess', 'Inference', 'Output'], [BLUE, TEAL, GRAY]):
    ax.barh([0], [duration], left=left, label=label, color=color)
    left += duration
ax.axvline(100, color=BLUE, linestyle='--', label='Next update')
ax.set_xlim(0, 110)
ax.set_yticks([])
ax.set_xlabel('Time after the last sample (ms)')
ax.set_title('Processing time and update interval')
ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.22), ncol=2, fontsize=9)
fig.tight_layout()
save(fig, 'system-budgets-latency-power', 'budgets.png')

phase = np.linspace(0, 2*np.pi, 361)
fig, ax = plt.subplots(figsize=(7, 3.4))
ax.plot(np.degrees(phase), np.cos(phase), label='I correlation / energy', color=BLUE)
ax.plot(np.degrees(phase), np.ones_like(phase), label='I/Q magnitude / energy', color=TEAL, linestyle='--')
ax.set_xlabel('Constant received phase (degrees)')
ax.set_ylabel('Normalized score')
ax.set_xticks([0, 90, 180, 270, 360])
ax.set_ylim(-1.2, 1.2)
ax.legend(loc='lower right')
fig.tight_layout()
save(fig, 'matched-filter', 'iq-phase.png')
