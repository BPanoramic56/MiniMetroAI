from tracker import Tracker
import webbrowser
from pathlib import Path
import time
import webview


HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.min.js"></script>
  <script>
    mermaid.initialize({ startOnLoad: true, theme: "default" });
  </script>
</head>
<body>
<div class="mermaid">
{diagram}
</div>
</body>
</html>
"""

class Grapher:
    
	def __init__(self, tracker: Tracker):
		self.tracker = tracker

	def tracker_to_mermaid(self) -> str:
		lines = ["graph TD"]

		# ---- Style definitions ----
		lines.append("classDef station fill:#E3F2FD,stroke:#1565C0,stroke-width:2px;")
		lines.append("classDef line fill:#F3E5F5,stroke:#6A1B9A,stroke-width:2px;")
		lines.append("classDef service fill:#E8F5E9,stroke:#2E7D32;")

		# ---- Service nodes ----
		service_nodes = set()
		for services in (
			list(self.tracker.station_service_dict.values())
			+ list(self.tracker.line_service_dict.values())
		):
			service_nodes |= services

		for service in service_nodes:
			lines.append(f"SERVICE_{service.name}[{service.name}]")
			lines.append(f"class SERVICE_{service.name} service")

		# ---- Station nodes ----
		for station_id, services in self.tracker.station_service_dict.items():
			sid = f"ST_{station_id.hex[:6]}"
			lines.append(f"{sid}[Station {station_id.hex[:4]}]")
			lines.append(f"class {sid} station")

			for service in services:
				lines.append(f"{sid} --> SERVICE_{service.name}")

		# ---- Line nodes ----
		for line_id, services in self.tracker.line_service_dict.items():
			lid = f"LN_{line_id.hex[:6]}"
			lines.append(f"{lid}[Line {line_id.hex[:4]}]")
			lines.append(f"class {lid} line")

			for service in services:
				lines.append(f"{lid} --> SERVICE_{service.name}")

		return "\n".join(lines)
	def show_mermaid_app(mermaid_code: str):
		html = HTML_TEMPLATE.format(diagram=mermaid_code)
		webview.create_window("Metro Service Map", html=html)
		webview.start()
