import json
import os

PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

def render_heatmap(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"{json_path} not found. Run fetch_contributions.py first.")
        
    with open(json_path, "r", encoding="utf-8") as f:
        days = json.load(f)
        
    total_contributions = sum(d["count"] for d in days)
    
    box_size = 11
    box_pad = 4
    start_x = 20
    start_y = 35
    
    svg_width = 860
    svg_height = 150
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">',
        '<style>',
        '  .bg { fill: #0d1117; }',
        '  .text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; fill: #8b949e; font-size: 11px; }',
        '  .title { font-weight: 600; fill: #c9d1d9; font-size: 13px; }',
        '  @keyframes slideIn {',
        '    0% { opacity: 0; transform: translateY(10px); }',
        '    100% { opacity: 1; transform: translateY(0); }',
        '  }',
        '  .heatmap-box { animation: slideIn 0.6s ease-out forwards; opacity: 0; }',
        '</style>',
        f'<rect width="{svg_width}" height="{svg_height}" class="bg" rx="6" stroke="#30363d" stroke-width="1"/>',
        f'<text x="{start_x}" y="22" class="text title">{total_contributions:,} contributions in the last year</text>'
    ]
    
    weeks = [days[i:i + 7] for i in range(0, len(days), 7)]
    
    for w_idx, week in enumerate(weeks):
        for d_idx, day in enumerate(week):
            x = start_x + w_idx * (box_size + box_pad)
            y = start_y + d_idx * (box_size + box_pad)
            level = min(day["level"], len(PALETTE) - 1)
            color = PALETTE[level]
            
            delay = round((w_idx + d_idx) * 0.008, 3)
            
            svg_lines.append(
                f'  <rect x="{x}" y="{y}" width="{box_size}" height="{box_size}" rx="2" fill="{color}" '
                f'class="heatmap-box" style="animation-delay: {delay}s;">'
                f'<title>{day["count"]} contributions on {day["date"]}</title></rect>'
            )
            
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated heatmap SVG at {output_path}")

if __name__ == "__main__":
    render_heatmap()