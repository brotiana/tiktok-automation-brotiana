from rich.live import Live
from rich.layout import Layout
from rich.panel import Panel
from rich.console import Console
import time

console = Console()
logs = []

layout = Layout()
layout.split_column(
    Layout(name="logs"),
    Layout(name="bar", size=3),
)

with Live(layout, refresh_per_second=4):
    i = 0
    while True:
        logs.append(f"Log line {i}")
        layout["logs"].update(Panel("\n".join(logs[-20:]), title="Logs"))
        layout["bar"].update(Panel(f"STATUS: OK | Lines: {i} | {time.strftime('%H:%M:%S')}"))
        i += 1
        time.sleep(0.3)