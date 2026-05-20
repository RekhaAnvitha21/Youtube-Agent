from PIL import Image, ImageDraw, ImageFont
import os
from config.config import THUMBNAILS_DIR

def generate_thumbnail(topic, filename="thumbnail.png"):
    """Generate a YouTube thumbnail using Pillow"""
    
    os.makedirs(THUMBNAILS_DIR, exist_ok=True)
    
    # Create base image with gradient background
    width, height = 1280, 720
    img = Image.new('RGB', (width, height), color=(20, 20, 40))
    draw = ImageDraw.Draw(img)
    
    # Draw gradient background
    for i in range(height):
        ratio = i / height
        r = int(20 + (80 - 20) * ratio)
        g = int(20 + (40 - 20) * ratio)
        b = int(40 + (120 - 40) * ratio)
        draw.line([(0, i), (width, i)], fill=(r, g, b))
    
    # Draw accent rectangle on left
    draw.rectangle([0, 0, 12, height], fill=(255, 50, 50))
    
    # Draw decorative circles
    draw.ellipse([900, -100, 1400, 400], outline=(255, 50, 50), width=3)
    draw.ellipse([950, 50, 1350, 450], outline=(255, 100, 50), width=2)
    
    # Wrap and draw title text
    words = topic.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        if len(' '.join(current_line)) > 25:
            lines.append(' '.join(current_line[:-1]))
            current_line = [word]
    lines.append(' '.join(current_line))
    
    # Draw each line of title
    y_start = 200
    for i, line in enumerate(lines[:4]):
        # Load a bigger font
        try:
            font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 72)
            small_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 36)
        except:
            font = ImageFont.load_default()
            small_font = font
        
        # Shadow effect
        draw.text((62, y_start + i * 90 + 4), line,
                 fill=(0, 0, 0), font=font)
        # Main text
        draw.text((60, y_start + i * 90), line,
                 fill=(255, 255, 255), font=font)
    
    # Draw bottom label
    draw.rectangle([0, 620, width, height], fill=(255, 50, 50))
    try:
        small_font = ImageFont.truetype("C:\\Windows\\Fonts\\arialbd.ttf", 36)
    except:
        small_font = ImageFont.load_default()
    draw.text((60, 635), "WATCH TILL THE END",
             fill=(255, 255, 255), font=small_font)
    
    # Save thumbnail
    output_path = os.path.join(THUMBNAILS_DIR, filename)
    img.save(output_path)
    print(f"Thumbnail saved to: {output_path}")
    return output_path

if __name__ == "__main__":
    topic = "I spent my whole career building passive income. Here's what I got wrong"
    print("Generating thumbnail...")
    path = generate_thumbnail(topic)
    print("Done!")