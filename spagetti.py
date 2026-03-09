### dont delete.. steal the shapes


import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import uuid
from datetime import datetime, timezone
from abc import ABC, abstractmethod

# --- 1. DATA PROVIDER ---
class BaseProvider(ABC):
    @abstractmethod
    def get_data(self, symbol, interval, count): pass

class YFinanceProvider(BaseProvider):
    def get_data(self, symbol, interval, count):
        # Fetch slightly more to account for buffer and technical lookback
        buffer = int(count * 0.15)
        df = yf.Ticker(symbol).history(period="1mo", interval=interval)
        return df.tail(count + buffer).copy().reset_index()

# --- 2. THE STATEFUL SCENE GRAPH ---
class SceneGraph:
    def __init__(self):
        # Registry stores: { uuid: {"data": {}, "created_at": dt, "updated_at": dt} }
        self._registry = {}

    def add(self, shape_data):
        """Creates a unique shape handle and returns a permanent UUID."""
        obj_id = str(uuid.uuid4())
        now = datetime.now()
        self._registry[obj_id] = {
            "id": obj_id,
            "data": shape_data,
            "created_at": now,
            "updated_at": now
        }
        return obj_id

    def update(self, obj_id, new_data):
        """Updates an existing shape's properties via its UUID."""
        if obj_id in self._registry:
            self._registry[obj_id]["data"].update(new_data)
            self._registry[obj_id]["updated_at"] = datetime.now()
        else:
            print(f"Warning: Attempted to update non-existent UUID {obj_id}")

    def get_render_list(self):
        """Flushes all current shape data to the renderer."""
        return [item["data"] for item in self._registry.values()]

# --- 3. SHAPE PROVIDERS (The 'ShapeThiongs') ---
class BaseShapeProvider(ABC):
    def __init__(self, scene_graph):
        self.scene = scene_graph
        self.handle = None # Persistent UUID handle

    @abstractmethod
    def sync(self, df): pass

class PivotLegShape(BaseShapeProvider):
    """Example: A diagonal line that 'stretches' as new data arrives."""
    def sync(self, df):
        last_idx = len(df) - 1
        curr_price = df['Close'].iloc[-1]
        start_price = df['High'].iloc[max(0, last_idx-60)]

        shape_props = {
            "type": "line",
            "x": [last_idx - 60, last_idx],
            "y": [start_price, curr_price],
            "color": "orange", "style": "--", "width": 2
        }

        if not self.handle:
            self.handle = self.scene.add(shape_props)
        else:
            self.scene.update(self.handle, shape_props)

class RejectionZoneShape(BaseShapeProvider):
    """Example: A static zone that is added once and persists."""
    def sync(self, df):
        if not self.handle:
            last_idx = len(df) - 1
            self.handle = self.scene.add({
                "type": "zone",
                "x": [last_idx - 30, last_idx],
                "y1": 400, "y2": 405,
                "color": "#88d8b0", "alpha": 0.15
            })

# --- 4. THE FULL-RENDERER (Matplotlib Implementation) ---
class MplRenderer:
    def __init__(self):
        self.theme = {
            'bg': '#0a0e14', 'up': '#88d8b0', 'down': '#ff6b6b',
            'grid': '#ffffff', 'text': '#999999', 'ribbon': '#a2d2ff'
        }
        plt.style.use('dark_background')

    def render(self, symbol, interval, df, scene_graph, bar_count):
        fig, ax_main = plt.subplots(figsize=(16, 9))
        fig.patch.set_facecolor(self.theme['bg'])
        ax_main.set_facecolor(self.theme['bg'])

        # Tight layout for the HUD
        plt.subplots_adjust(left=0.05, right=0.95, top=0.88, bottom=0.1)

        self._draw_hud(fig, symbol, interval, df, bar_count)
        self._draw_candles(ax_main, df)

        # RENDER SCENE GRAPH (Flushing the UUID-based registry)
        for el in scene_graph.get_render_list():
            clip = {'clip_on': True, 'zorder': 10}
            if el['type'] == 'line':
                ax_main.plot(el['x'], el['y'], color=el['color'], ls=el.get('style', '-'), lw=el.get('width', 2), **clip)
            elif el['type'] == 'zone':
                ax_main.fill_between(el['x'], el['y1'], el['y2'], color=el['color'], alpha=el.get('alpha', 0.2), **clip)
            elif el['type'] == 'text':
                ax_main.text(el['x'], el['y'], el['content'], color=el['color'], fontsize=8, fontweight='bold', ha='center', **clip)

        self._setup_axes(ax_main, df, bar_count)
        plt.show()

    def _draw_hud(self, fig, symbol, interval, df, bar_count):
        col = 'Datetime' if 'Datetime' in df.columns else 'Date'
        r_start, r_end = df[col].iloc[0].strftime('%Y-%m-%d %H:%M'), df[col].iloc[-1].strftime('%Y-%m-%d %H:%M')

        fig.text(0.05, 0.96, symbol, fontsize=14, fontweight='bold', color='gold')
        fig.text(0.05 + (len(symbol)*0.012), 0.96, f" ({interval})", color=self.theme['text'], family='monospace')
        fig.text(0.05, 0.94, f"{r_start} — {r_end}", fontsize=7, color=self.theme['text'], family='monospace')
        fig.text(0.95, 0.96, f"RENDERED: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}", fontsize=7, color=self.theme['text'], ha='right')

        fig.add_artist(plt.Line2D([0.05, 0.95], [0.93, 0.93], transform=fig.transFigure, color='white', alpha=0.08))

    def _draw_candles(self, ax, df):
        for i, row in df.iterrows():
            color = self.theme['up'] if row["Close"] >= row["Open"] else self.theme['down']
            ax.vlines(i, row["Low"], row["High"], color=color, lw=1.2, alpha=0.7, clip_on=True)
            ax.hlines(row["Open"], i - 0.3, i, color=color, lw=1.2, alpha=0.7, clip_on=True)
            ax.hlines(row["Close"], i, i + 0.3, color=color, lw=1.2, alpha=0.7, clip_on=True)

    def _setup_axes(self, ax, df, bar_count):
        # Top Bar Count Ribbon
        ax_top = ax.twiny()
        ax.set_xlim(0, len(df) + 5)
        ax_top.set_xlim(ax.get_xlim())

        start_idx = len(df) - bar_count
        ticks = [t for t in range(0, len(df), max(1, bar_count//10)) if t != start_idx]
        ax_top.set_xticks(ticks)
        ax_top.tick_params(axis='x', colors=f"{self.theme['ribbon']}80", labelsize=8, pad=8)
        ax_top.set_xticklabels([str(len(df) - t) for t in ticks], family='monospace')

        ax_top.text(start_idx, 1.028, f" {bar_count} ", transform=ax_top.get_xaxis_transform(),
                    color='white', fontweight='bold', fontsize=8, family='monospace',
                    bbox=dict(facecolor='#1a222d', edgecolor=self.theme['ribbon'], boxstyle='round,pad=0.2', alpha=0.9),
                    ha='center', va='center')

        # Time Ribbon
        tick_indices = np.linspace(0, len(df)-1, 8, dtype=int)
        col = 'Datetime' if 'Datetime' in df.columns else 'Date'
        ax.set_xticks(tick_indices)
        ax.set_xticklabels([df[col].iloc[i].strftime('%b %d %H:%M') for i in tick_indices], color='#444444', fontsize=8)

        # Scaling
        ax_right = ax.twinx()
        p_min, p_max = df['Low'].min() * 0.998, df['High'].max() * 1.002
        ax.set_ylim(p_min, p_max)
        ax_right.set_ylim(p_min, p_max)
        for a in [ax, ax_right]:
            a.spines[['top', 'right', 'left']].set_visible(False)
            a.tick_params(axis='y', colors='#444444', labelsize=8)

# --- 5. ORCHESTRATOR ---
def run_engine():
    symbol, interval, bar_count = "MSFT", "1h", 100

    # Initialize Core
    provider = YFinanceProvider()
    scene = SceneGraph()
    renderer = MplRenderer()

    # Register ShapeProviders
    shapes = [PivotLegShape(scene), RejectionZoneShape(scene)]

    # Execution
    data = provider.get_data(symbol, interval, bar_count)

    for s in shapes:
        s.sync(data) # This handles the ADD or UPDATE logic internally via UUID

    renderer.render(symbol, interval, data, scene, bar_count)

if __name__ == "__main__":
    run_engine()