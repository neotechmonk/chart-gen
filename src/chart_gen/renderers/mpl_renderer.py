"""Matplotlib chart renderer."""

from datetime import datetime, timezone

import matplotlib.pyplot as plt
import numpy as np


class MplRenderer:
    """Full-renderer using matplotlib."""

    def __init__(self):
        self.theme = {
            "bg": "#0a0e14",
            "up": "#88d8b0",
            "down": "#ff6b6b",
            "grid": "#ffffff",
            "text": "#999999",
            "ribbon": "#a2d2ff",
        }
        plt.style.use("dark_background")

    def render(
        self,
        symbol: str,
        interval: str,
        df,
        scene_graph,
        bar_count: int,
        save_path: str | None = None,
    ) -> None:
        fig, ax_main = plt.subplots(figsize=(16, 9))
        fig.patch.set_facecolor(self.theme["bg"])
        ax_main.set_facecolor(self.theme["bg"])

        plt.subplots_adjust(left=0.05, right=0.95, top=0.88, bottom=0.1)

        self._draw_hud(fig, symbol, interval, df, bar_count)
        self._draw_candles(ax_main, df)

        for el in scene_graph.get_render_list():
            clip = {"clip_on": True, "zorder": 10}
            if el["type"] == "line":
                ax_main.plot(
                    el["x"],
                    el["y"],
                    color=el["color"],
                    ls=el.get("style", "-"),
                    lw=el.get("width", 2),
                    **clip,
                )
            elif el["type"] == "zone":
                ax_main.fill_between(
                    el["x"],
                    el["y1"],
                    el["y2"],
                    color=el["color"],
                    alpha=el.get("alpha", 0.2),
                    **clip,
                )
            elif el["type"] == "text":
                ax_main.text(
                    el["x"],
                    el["y"],
                    el["content"],
                    color=el["color"],
                    fontsize=8,
                    fontweight="bold",
                    ha="center",
                    **clip,
                )

        self._setup_axes(ax_main, df, bar_count)
        if save_path:
            fig.savefig(save_path, dpi=100, bbox_inches="tight")
            plt.close(fig)
        else:
            plt.show()

    def _draw_hud(self, fig, symbol: str, interval: str, df, bar_count: int) -> None:
        col = "Datetime" if "Datetime" in df.columns else "Date"
        r_start = df[col].iloc[0].strftime("%Y-%m-%d %H:%M")
        r_end = df[col].iloc[-1].strftime("%Y-%m-%d %H:%M")

        fig.text(0.05, 0.96, symbol, fontsize=14, fontweight="bold", color="gold")
        fig.text(0.05 + (len(symbol) * 0.012), 0.96, f" ({interval})", color=self.theme["text"], family="monospace")
        fig.text(0.05, 0.94, f"{r_start} — {r_end}", fontsize=7, color=self.theme["text"], family="monospace")
        fig.text(
            0.95,
            0.96,
            f"RENDERED: {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}",
            fontsize=7,
            color=self.theme["text"],
            ha="right",
        )

        fig.add_artist(
            plt.Line2D([0.05, 0.95], [0.93, 0.93], transform=fig.transFigure, color="white", alpha=0.08)
        )

    def _draw_candles(self, ax, df) -> None:
        for i, row in df.iterrows():
            color = self.theme["up"] if row["Close"] >= row["Open"] else self.theme["down"]
            ax.vlines(i, row["Low"], row["High"], color=color, lw=1.2, alpha=0.7, clip_on=True)
            ax.hlines(row["Open"], i - 0.3, i, color=color, lw=1.2, alpha=0.7, clip_on=True)
            ax.hlines(row["Close"], i, i + 0.3, color=color, lw=1.2, alpha=0.7, clip_on=True)

    def _setup_axes(self, ax, df, bar_count: int) -> None:
        ax_top = ax.twiny()
        ax.set_xlim(0, len(df) + 5)
        ax_top.set_xlim(ax.get_xlim())

        start_idx = len(df) - bar_count
        ticks = [t for t in range(0, len(df), max(1, bar_count // 10)) if t != start_idx]
        ax_top.set_xticks(ticks)
        ax_top.tick_params(axis="x", colors=f"{self.theme['ribbon']}80", labelsize=8, pad=8)
        ax_top.set_xticklabels([str(len(df) - t) for t in ticks], family="monospace")

        ax_top.text(
            start_idx,
            1.028,
            f" {bar_count} ",
            transform=ax_top.get_xaxis_transform(),
            color="white",
            fontweight="bold",
            fontsize=8,
            family="monospace",
            bbox=dict(
                facecolor="#1a222d",
                edgecolor=self.theme["ribbon"],
                boxstyle="round,pad=0.2",
                alpha=0.9,
            ),
            ha="center",
            va="center",
        )

        tick_indices = np.linspace(0, len(df) - 1, 8, dtype=int)
        col = "Datetime" if "Datetime" in df.columns else "Date"
        ax.set_xticks(tick_indices)
        ax.set_xticklabels(
            [df[col].iloc[i].strftime("%b %d %H:%M") for i in tick_indices],
            color="#444444",
            fontsize=8,
        )

        ax_right = ax.twinx()
        p_min, p_max = df["Low"].min() * 0.998, df["High"].max() * 1.002
        ax.set_ylim(p_min, p_max)
        ax_right.set_ylim(p_min, p_max)
        for a in [ax, ax_right]:
            a.spines[["top", "right", "left"]].set_visible(False)
            a.tick_params(axis="y", colors="#444444", labelsize=8)
