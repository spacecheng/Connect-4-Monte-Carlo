"""Generate presentation-quality charts for the Connect 4 MCTS project."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import numpy as np
import os

OUT = os.path.join(os.path.dirname(__file__), 'charts')
os.makedirs(OUT, exist_ok=True)

sns.set_theme(style="darkgrid", context="talk", palette="muted")
plt.rcParams.update({
    'figure.facecolor': '#1a1a2e',
    'axes.facecolor': '#16213e',
    'axes.edgecolor': '#e0e0e0',
    'axes.labelcolor': '#e0e0e0',
    'text.color': '#e0e0e0',
    'xtick.color': '#c0c0c0',
    'ytick.color': '#c0c0c0',
    'grid.color': '#2a2a4a',
    'grid.alpha': 0.5,
    'legend.facecolor': '#16213e',
    'legend.edgecolor': '#444',
    'font.family': 'sans-serif',
    'font.size': 13,
})

ACCENT = '#00d2ff'
GREEN = '#00e676'
RED = '#ff5252'
YELLOW = '#ffea00'
PURPLE = '#bb86fc'
GRAY = '#888888'


# ===== Chart 1: Win Rate Comparison Bar Chart =====
fig, ax = plt.subplots(figsize=(12, 6))

matchups = [
    'Random\nvs Random',
    'SmartRand\nvs Random',
    'MCTS(100)\nvs Random',
    'MCTS(250)\nvs Random',
    'MCTS(1000)\nvs Random',
    'MCTS(1000)\nvs SmartRand',
]
win_rates = [52, 96, 98, 100, 100, 100]
colors = [GRAY, YELLOW, '#64b5f6', ACCENT, GREEN, PURPLE]

bars = ax.bar(matchups, win_rates, color=colors, width=0.6, edgecolor='#ffffff22', linewidth=0.8)
for bar, val in zip(bars, win_rates):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{val}%', ha='center', va='bottom', fontweight='bold', fontsize=14, color='white')

ax.set_ylim(0, 115)
ax.set_ylabel('Win Rate (%)', fontsize=14)
ax.set_title('Bot Win Rates — 50 Games Each, Alternating First Player', fontsize=16, fontweight='bold', pad=15)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(100, decimals=0))
ax.axhline(y=50, color=GRAY, linestyle='--', alpha=0.4, label='Coin flip (50%)')
ax.legend(loc='upper left', fontsize=11)
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'win_rates_bar.png'), dpi=200, bbox_inches='tight')
plt.close()
print('1/5 win_rates_bar.png')


# ===== Chart 2: MCTS Win Rate vs Iterations (dual line) =====
fig, ax = plt.subplots(figsize=(10, 6))

iters = [50, 100, 250, 500, 1000, 2000]
wr_random = [94, 98, 100, 100, 100, 100]
wr_smart  = [None, 84, 100, 100, 100, None]

ax.plot(iters, wr_random, 'o-', color=GREEN, linewidth=2.5, markersize=9, label='vs Random', zorder=5)

smart_x = [100, 250, 500, 1000]
smart_y = [84, 100, 100, 100]
ax.plot(smart_x, smart_y, 's--', color=PURPLE, linewidth=2.5, markersize=9, label='vs SmartRandom', zorder=5)

ax.fill_between(iters, wr_random, alpha=0.08, color=GREEN)
ax.fill_between(smart_x, smart_y, alpha=0.08, color=PURPLE)

ax.set_xscale('log')
ax.set_xticks(iters)
ax.get_xaxis().set_major_formatter(mticker.ScalarFormatter())
ax.set_xlim(35, 2800)
ax.set_ylim(78, 103)
ax.set_xlabel('MCTS Iterations (log scale)', fontsize=14)
ax.set_ylabel('Win Rate (%)', fontsize=14)
ax.set_title('MCTS Win Rate vs. Iteration Budget', fontsize=16, fontweight='bold', pad=15)
ax.axhline(y=100, color='white', linestyle=':', alpha=0.2)

for x, y in zip(iters, wr_random):
    ax.annotate(f'{y}%', (x, y), textcoords='offset points', xytext=(0, 12),
                ha='center', fontsize=11, color=GREEN, fontweight='bold')
for x, y in zip(smart_x, smart_y):
    offset = (0, -18) if y == 100 else (0, 12)
    ax.annotate(f'{y}%', (x, y), textcoords='offset points', xytext=offset,
                ha='center', fontsize=11, color=PURPLE, fontweight='bold')

ax.legend(fontsize=12, loc='lower right')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'winrate_vs_iterations.png'), dpi=200, bbox_inches='tight')
plt.close()
print('2/5 winrate_vs_iterations.png')


# ===== Chart 3: Timing — Move Time vs Iterations =====
fig, ax = plt.subplots(figsize=(10, 6))

times_ms = [2.4, 4.6, 12.1, 23.1, 45.1, 91.1]

ax.plot(iters, times_ms, 'o-', color=ACCENT, linewidth=2.5, markersize=9, zorder=5)
ax.fill_between(iters, times_ms, alpha=0.1, color=ACCENT)

for x, y in zip(iters, times_ms):
    ax.annotate(f'{y}ms', (x, y), textcoords='offset points', xytext=(8, 8),
                ha='left', fontsize=11, color='white', fontweight='bold')

ax.axhspan(0, 100, alpha=0.04, color=GREEN)
ax.text(70, 90, 'Real-time zone (<100ms)', fontsize=10, color=GREEN, alpha=0.7, style='italic')
ax.axhline(y=100, color=GREEN, linestyle='--', alpha=0.3)

ax.set_xlabel('MCTS Iterations', fontsize=14)
ax.set_ylabel('Avg Time per Move (ms)', fontsize=14)
ax.set_title('MCTS Decision Speed vs. Iteration Count', fontsize=16, fontweight='bold', pad=15)
ax.set_xlim(-50, 2200)
ax.set_ylim(-5, 110)
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'timing_vs_iterations.png'), dpi=200, bbox_inches='tight')
plt.close()
print('3/5 timing_vs_iterations.png')


# ===== Chart 4: Board Size Scaling (dual-axis) =====
fig, ax1 = plt.subplots(figsize=(10, 6))

boards = ['7×6\nConnect-4', '9×7\nConnect-4', '10×8\nConnect-5', '12×10\nConnect-5']
board_times = [45.1, 58.0, 118.7, 144.8]
board_wr = [100, 100, 100, 100]
board_cells = [42, 63, 80, 120]

x = np.arange(len(boards))
bars = ax1.bar(x, board_times, 0.5, color=[ACCENT, '#4fc3f7', '#29b6f6', '#039be5'],
               edgecolor='#ffffff22', linewidth=0.8, zorder=3)
for bar, val, cells in zip(bars, board_times, board_cells):
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 3,
             f'{val}ms', ha='center', va='bottom', fontweight='bold', fontsize=13, color='white')
    ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height()/2,
             f'{cells} cells', ha='center', va='center', fontsize=10, color='#1a1a2e', fontweight='bold')

ax1.set_xticks(x)
ax1.set_xticklabels(boards)
ax1.set_ylabel('Avg Move Time (ms)', fontsize=14)
ax1.set_ylim(0, 185)
ax1.set_title('MCTS(1000) Scaling Across Board Sizes — 100% Win Rate on All',
              fontsize=15, fontweight='bold', pad=15)

ax1.axhline(y=100, color=RED, linestyle='--', alpha=0.4)
ax1.text(3.3, 103, '100ms threshold', fontsize=10, color=RED, alpha=0.6, style='italic')

ax2 = ax1.twinx()
ax2.plot(x, board_wr, 's-', color=GREEN, linewidth=2.5, markersize=12, zorder=5)
ax2.set_ylabel('Win Rate (%)', fontsize=14, color=GREEN)
ax2.set_ylim(85, 105)
ax2.tick_params(axis='y', labelcolor=GREEN)

plt.tight_layout()
fig.savefig(os.path.join(OUT, 'board_scaling.png'), dpi=200, bbox_inches='tight')
plt.close()
print('4/5 board_scaling.png')


# ===== Chart 5: MCTS vs SmartRandom stacked bar =====
fig, ax = plt.subplots(figsize=(10, 6))

labels = ['MCTS(100)', 'MCTS(250)', 'MCTS(500)', 'MCTS(1000)']
wins   = [42, 50, 50, 50]
losses = [6, 0, 0, 0]
draws  = [2, 0, 0, 0]
x = np.arange(len(labels))

ax.bar(x, wins,   0.5, label='Wins',   color=GREEN,  edgecolor='#ffffff22', zorder=3)
ax.bar(x, losses, 0.5, bottom=wins, label='Losses', color=RED, edgecolor='#ffffff22', zorder=3)
ax.bar(x, draws,  0.5, bottom=[w+l for w,l in zip(wins, losses)], label='Draws', color=GRAY, edgecolor='#ffffff22', zorder=3)

for i, (w, l, d) in enumerate(zip(wins, losses, draws)):
    if w > 0:
        ax.text(i, w/2, str(w), ha='center', va='center', fontweight='bold', fontsize=14, color='#1a1a2e')
    if l > 0:
        ax.text(i, w + l/2, str(l), ha='center', va='center', fontweight='bold', fontsize=12, color='white')
    if d > 0:
        ax.text(i, w + l + d/2, str(d), ha='center', va='center', fontweight='bold', fontsize=11, color='white')

ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.set_ylabel('Games (out of 50)', fontsize=14)
ax.set_title('MCTS vs. Random+WinCheck — Game Outcomes', fontsize=16, fontweight='bold', pad=15)
ax.set_ylim(0, 58)
ax.legend(fontsize=12, loc='upper right')
plt.tight_layout()
fig.savefig(os.path.join(OUT, 'mcts_vs_smartrand.png'), dpi=200, bbox_inches='tight')
plt.close()
print('5/5 mcts_vs_smartrand.png')

print('\nAll charts saved to ./charts/')
