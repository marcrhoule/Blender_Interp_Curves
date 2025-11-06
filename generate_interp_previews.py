"""
Run this script to generate PNG preview images for all interpolation functions.
This creates a folder with all the preview images that the Blender addon will use.
"""

import math
import os
from PIL import Image, ImageDraw

# Import functions from the shared library
try:
    from interpolation_functions import INTERPOLATION_FUNCTIONS
except ImportError:
    print("Error: Could not find interpolation_functions.py")
    print("Make sure this script is in the same folder as interpolation_functions.py")
    exit(1)

def generate_preview(func, name, width=200, height=100, samples=200):
    """Generate a preview image for an interpolation function"""
    
    # Create image with dark background
    img = Image.new('RGB', (width, height), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    
    # Draw grid
    grid_color = (50, 50, 50)
    for i in range(0, width, width // 4):
        draw.line([(i, 0), (i, height)], fill=grid_color, width=1)
    for i in range(0, height, height // 4):
        draw.line([(0, i), (width, i)], fill=grid_color, width=1)
    
    # Calculate points
    points = []
    values = []
    
    for i in range(samples):
        t = i / (samples - 1)
        try:
            value = func(t)
            values.append(value)
        except:
            values.append(t)  # Fallback to linear
    
    # Normalize values to fit in image
    min_val = min(values)
    max_val = max(values)
    value_range = max_val - min_val
    
    if value_range == 0:
        value_range = 1
    
    # Create coordinate points
    for i, value in enumerate(values):
        x = int((i / (samples - 1)) * (width - 1))
        # Flip y coordinate (image coords are top-down)
        normalized = (value - min_val) / value_range
        y = int((1 - normalized) * (height - 1))
        points.append((x, y))
    
    # Draw the curve
    if len(points) > 1:
        draw.line(points, fill=(100, 200, 255), width=2)
    
    # Draw start and end points
    if points:
        start_x, start_y = points[0]
        end_x, end_y = points[-1]
        draw.ellipse([start_x-3, start_y-3, start_x+3, start_y+3], fill=(0, 255, 100))
        draw.ellipse([end_x-3, end_y-3, end_x+3, end_y+3], fill=(255, 100, 100))
    
    return img

def generate_all_previews(output_dir="interp_previews"):
    """Generate preview images for all interpolation functions"""
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Generating {len(INTERPOLATION_FUNCTIONS)} preview images...")
    
    for name, func in INTERPOLATION_FUNCTIONS.items():
        # Create safe filename
        safe_name = name.replace(" ", "_").replace("+", "plus").replace("/", "_")
        filename = f"{safe_name}.png"
        filepath = os.path.join(output_dir, filename)
        
        try:
            img = generate_preview(func, name)
            img.save(filepath)
            print(f"✓ Generated: {filename}")
        except Exception as e:
            print(f"✗ Failed to generate {name}: {e}")
    
    print(f"\nDone! All previews saved to: {output_dir}/")
    print(f"Copy this folder to your Blender addon directory.")

if __name__ == "__main__":
    generate_all_previews()