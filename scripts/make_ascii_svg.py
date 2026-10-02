import cv2
import numpy as np

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)
CHAR_WIDTH = 7
CHAR_HEIGHT = 14
COLS = 95
ROWS = 50

def generate_ascii_svg(image_path="source-prepped.png", output_path="avi-ascii.svg"):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not load {image_path}. Run prep_photo.py first.")
        
    img_resized = cv2.resize(img, (COLS, ROWS))
    
    svg_width = COLS * CHAR_WIDTH
    svg_height = ROWS * CHAR_HEIGHT
    
    svg_lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="100%" height="100%">',
        '<style>',
        '  text { font-family: "Courier New", Courier, monospace; font-size: 12px; fill: #c9d1d9; }',
        '  .bg { fill: #0d1117; }',
        '  @keyframes wipe { to { transform: translateX(0); } }',
        '  .row-anim { animation: wipe 0.8s ease-out forwards; transform: translateX(-100%); }',
        '</style>',
        f'<rect width="{svg_width}" height="{svg_height}" class="bg" rx="6"/>',
        '<g transform="translate(10, 15)">'
    ]
    
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            val = img_resized[r, c]
            idx = int((val / 255.0) * (len(RAMP) - 1))
            char = RAMP[idx]
            if char == " ":
                char = "&nbsp;"
            elif char == "<": char = "&lt;"
            elif char == ">": char = "&gt;"
            elif char == "&": char = "&amp;"
            row_str += char
            
        delay = round(r * 0.02, 2)
        svg_lines.append(
            f'  <text x="0" y="{r * CHAR_HEIGHT}" class="row-anim" style="animation-delay: {delay}s;">{row_str}</text>'
        )
        
    svg_lines.append('</g>')
    svg_lines.append('</svg>')
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg_lines))
    print(f"Generated ASCII SVG at {output_path}")

if __name__ == "__main__":
    generate_ascii_svg()