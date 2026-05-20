from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path("/home/uwase/Downloads/plant/hero")
OUT = ROOT / "outputs"
RESAMPLE = getattr(Image, "Resampling", Image).LANCZOS

reference = Image.open(ROOT / "reference" / "hero_reference.png").convert("RGB").resize((1600, 900), RESAMPLE)
generated = Image.open(OUT / "hero_generated.png").convert("RGB")

comparison = Image.new("RGB", (1700, 2080), (248, 245, 241))
draw = ImageDraw.Draw(comparison)
draw.text((40, 26), "reference hero", fill=(30, 30, 30))
draw.text((870, 26), "generated hero", fill=(30, 30, 30))
comparison.paste(reference.resize((800, 450), RESAMPLE), (40, 55))
comparison.paste(generated.resize((800, 450), RESAMPLE), (870, 55))

regions = [
    ("left typography/text area", (0, 110, 640, 660)),
    ("terracotta wall/blob", (610, 0, 1390, 735)),
    ("vase/pot and base composition", (720, 150, 1460, 790)),
    ("bottom terracotta path", (0, 610, 1600, 900)),
    ("overall spacing and balance", (0, 0, 1600, 900)),
]

y = 545
for label, box in regions:
    draw.text((40, y), f"{label}: reference", fill=(30, 30, 30))
    draw.text((870, y), f"{label}: generated", fill=(30, 30, 30))
    ref_crop = reference.crop(box).resize((760, 260), RESAMPLE)
    gen_crop = generated.crop(box).resize((760, 260), RESAMPLE)
    comparison.paste(ref_crop, (40, y + 28))
    comparison.paste(gen_crop, (870, y + 28))
    y += 300

comparison.save(OUT / "hero_comparison.png")
print(f"Wrote {OUT / 'hero_comparison.png'}")
