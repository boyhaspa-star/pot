from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFilter, ImageFont


ROOT = Path("/home/uwase/Downloads/plant/hero")
OUT = ROOT / "outputs"
W, H = 1600, 900
RESAMPLE = getattr(Image, "Resampling", Image).LANCZOS


def font(size, serif=False):
    candidates = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf" if serif else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSerif-Regular.ttf" if serif else "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_blob(draw):
    points = []
    cx, cy = 1040, 345
    rx, ry = 260, 360
    for i in range(160):
        t = math.tau * i / 160
        wobble = 1 + 0.13 * math.sin(t * 2.1 - 0.7) + 0.08 * math.sin(t * 4.0 + 1.4)
        x = cx + math.cos(t) * rx * wobble + 24 * math.sin(t * 1.2)
        y = cy + math.sin(t) * ry * wobble
        points.append((x, y))
    draw.polygon(points, fill=(184, 94, 55))


def draw_path(draw):
    points = [(0, H)]
    for x in range(0, W + 1, 18):
        y = 710 - 92 * math.sin((x / W) * math.pi * 0.88 + 0.25) + 28 * math.sin((x / W) * math.tau * 1.35)
        points.append((x, y))
    points.append((W, H))
    draw.polygon(points, fill=(199, 103, 57))


def paste_contain(base, overlay, box):
    x, y, w, h = box
    image = overlay.copy()
    ratio = min(w / image.width, h / image.height)
    new_size = (round(image.width * ratio), round(image.height * ratio))
    image = image.resize(new_size, RESAMPLE)
    x += (w - image.width) // 2
    y += (h - image.height) // 2
    if image.mode == "RGBA":
        base.alpha_composite(image, (x, y))
    else:
        base.paste(image, (x, y))


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    hero = Image.new("RGBA", (W, H), (246, 237, 224, 255))
    draw = ImageDraw.Draw(hero)

    for radius, alpha in [(540, 44), (280, 30)]:
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)
        gdraw.ellipse((940 - radius, 125 - radius, 940 + radius, 125 + radius), fill=(255, 248, 235, alpha))
        hero.alpha_composite(glow.filter(ImageFilter.GaussianBlur(80)))

    draw_blob(draw)
    draw_path(draw)

    nav_font = font(15)
    logo_font = font(15, serif=True)
    draw.text((78, 48), "AUREN", fill=(42, 30, 24), font=logo_font)
    nav_x = 1048
    for item in ["Work", "About", "Journal", "Contact"]:
        draw.text((nav_x, 48), item, fill=(45, 31, 25), font=nav_font)
        nav_x += 92
    draw.line((1498, 51, 1518, 51), fill=(45, 31, 25), width=2)
    draw.line((1498, 58, 1518, 58), fill=(45, 31, 25), width=2)

    side_font = font(14)
    side = Image.new("RGBA", (360, 26), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(side)
    sdraw.text((0, 3), "SOFT STRATEGY / VISUAL SYSTEMS", fill=(64, 45, 34, 150), font=side_font)
    hero.alpha_composite(side.rotate(90, expand=True), (70, 265))

    serif = font(66, serif=True)
    body_font = font(20)
    cta_font = font(16)
    x = 245
    y = 260
    for line in ["I design", "brands with", "soul."]:
        draw.text((x, y), line, fill=(30, 22, 18), font=serif)
        y += 70
    draw.text(
        (x, y + 12),
        "Brand & Web Designer crafting\nthoughtful identities and digital\nexperiences.",
        fill=(50, 35, 27),
        font=body_font,
        spacing=8,
    )
    cta_y = y + 132
    draw.text((x, cta_y), "View Selected Work  →", fill=(31, 22, 17), font=cta_font)
    draw.line((x, cta_y + 27, x + 160, cta_y + 27), fill=(31, 22, 17), width=1)

    cutout = Image.open(OUT / "hero_object_cutout.png").convert("RGBA")
    paste_contain(hero, cutout, (830, 100, 500, 650))

    hero.convert("RGB").save(OUT / "hero_generated.png", quality=95)
    print(f"Wrote {OUT / 'hero_generated.png'}")


if __name__ == "__main__":
    main()
