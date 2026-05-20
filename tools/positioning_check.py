#!/usr/bin/env python3
"""Capture and compare hero 3D object positioning against the reference."""

from __future__ import annotations

import argparse
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ROOT / "outputs"
REFERENCE = ROOT / "hero.png"
URL = "http://localhost:5173/#work"

VIEWPORT = (1840, 966)
SCREENSHOT = OUTPUTS / "hero_generated.png"
COMPARISON = OUTPUTS / "hero_positioning_comparison.png"
STANDARD_COMPARISON = OUTPUTS / "hero_comparison.png"
REPORT = OUTPUTS / "hero_positioning_report.md"

# Boxes measured on hero/hero.png, then scaled to the live screenshot size.
REFERENCE_BOXES = {
    "full 3D target": (218, 43, 364, 213),
    "plant target": (242, 48, 330, 145),
    "vase target": (238, 104, 314, 181),
    "base target": (218, 168, 364, 213),
}

RESAMPLE = getattr(getattr(Image, "Resampling", Image), "LANCZOS", Image.LANCZOS)


@dataclass(frozen=True)
class Box:
    left: int
    top: int
    right: int
    bottom: int

    @property
    def width(self) -> int:
        return self.right - self.left

    @property
    def height(self) -> int:
        return self.bottom - self.top

    @property
    def center(self) -> tuple[float, float]:
        return ((self.left + self.right) / 2, (self.top + self.bottom) / 2)

    def as_tuple(self) -> tuple[int, int, int, int]:
        return (self.left, self.top, self.right, self.bottom)


def find_font(size: int = 24) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for candidate in (
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
    ):
        path = Path(candidate)
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def capture_page(path: Path, viewport: tuple[int, int]) -> None:
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        raise RuntimeError("Could not find google-chrome/chromium for screenshot capture.")

    width, height = viewport
    command = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--enable-unsafe-swiftshader",
        f"--window-size={width},{height}",
        "--virtual-time-budget=10000",
        "--run-all-compositor-stages-before-draw",
        f"--screenshot={path}",
        URL,
    ]
    subprocess.run(command, cwd=ROOT, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def scale_box(box: tuple[int, int, int, int], source: tuple[int, int], target: tuple[int, int]) -> Box:
    sx = target[0] / source[0]
    sy = target[1] / source[1]
    left, top, right, bottom = box
    return Box(round(left * sx), round(top * sy), round(right * sx), round(bottom * sy))


def detect_current_object(image: Image.Image) -> Box | None:
    """Find dark/textured 3D pixels in the right hero area.

    The terracotta wall/path are broad, flat orange shapes. The 3D object is
    darker, textured, and contains brown plant lines, so this mask avoids the
    flat background shapes while still catching the vase, stem, base, and shadow.
    """

    width, height = image.size
    pixels = image.load()
    xs: list[int] = []
    ys: list[int] = []

    for y in range(round(height * 0.12), round(height * 0.86), 2):
        for x in range(round(width * 0.50), round(width * 0.88), 2):
            r, g, b = pixels[x, y]
            red_flat_bg = r > 178 and 70 <= g <= 135 and 35 <= b <= 95 and (r - g) > 55
            cream_bg = r > 218 and g > 205 and b > 188
            likely_3d = (
                not red_flat_bg
                and not cream_bg
                and (
                    (r < 170 and g < 125 and b < 100)
                    or (r < 120 and g < 105 and b < 90)
                    or ((max(r, g, b) - min(r, g, b)) > 55 and r < 210)
                )
            )
            if likely_3d:
                xs.append(x)
                ys.append(y)

    if len(xs) < 60:
        return None

    pad = 10
    return Box(max(0, min(xs) - pad), max(0, min(ys) - pad), min(width, max(xs) + pad), min(height, max(ys) + pad))


def detect_current_base(image: Image.Image, base_target: Box) -> Box | None:
    """Detect the broad dark base/slab line inside the reference base band."""

    pixels = image.load()
    row_hits: list[tuple[int, list[int]]] = []

    left = max(0, base_target.left - 60)
    right = min(image.width, base_target.right + 40)
    top = max(0, base_target.top - 35)
    bottom = min(image.height, base_target.bottom)

    for y in range(top, bottom):
        xs: list[int] = []
        for x in range(left, right):
            r, g, b = pixels[x, y]
            dark_brown = r < 150 and g < 95 and b < 70 and (r - b) > 25
            if dark_brown:
                xs.append(x)
        if xs:
            row_hits.append((y, xs))

    if not row_hits:
        return None

    max_count = max(len(xs) for _, xs in row_hits)
    strong_rows = [(y, xs) for y, xs in row_hits if len(xs) >= max(24, max_count * 0.58)]
    if not strong_rows:
        return None

    xs = [x for _, row in strong_rows for x in row]
    ys = [y for y, _ in strong_rows]
    return Box(min(xs), min(ys), max(xs), max(ys))


def draw_labeled_box(draw: ImageDraw.ImageDraw, box: Box, label: str, color: tuple[int, int, int], font) -> None:
    draw.rectangle(box.as_tuple(), outline=color, width=4)
    if hasattr(draw, "textbbox"):
        text_box = draw.textbbox((0, 0), label, font=font)
        text_w = text_box[2] - text_box[0]
        text_h = text_box[3] - text_box[1]
    else:
        text_w, text_h = draw.textsize(label, font=font)
    label_w = text_w + 16
    label_h = text_h + 12
    y = max(0, box.top - label_h - 3)
    draw.rectangle((box.left, y, box.left + label_w, y + label_h), fill=(248, 239, 229))
    draw.text((box.left + 8, y + 5), label, fill=color, font=font)


def make_comparison(reference: Image.Image, current: Image.Image, current_box: Box | None) -> tuple[Path, str]:
    width, height = current.size
    ref_resized = reference.resize((width, height), RESAMPLE)
    font = find_font(24)
    title_font = find_font(34)

    target_boxes = {
        name: scale_box(box, reference.size, current.size) for name, box in REFERENCE_BOXES.items()
    }
    target = target_boxes["full 3D target"]
    base_target = target_boxes["base target"]
    current_base_box = detect_current_base(current, base_target)

    ref_marked = ref_resized.copy()
    cur_marked = current.copy()
    ref_draw = ImageDraw.Draw(ref_marked)
    cur_draw = ImageDraw.Draw(cur_marked)

    colors = {
        "full 3D target": (29, 96, 151),
        "plant target": (84, 117, 37),
        "vase target": (151, 84, 23),
        "base target": (132, 66, 137),
    }

    for name, box in target_boxes.items():
        draw_labeled_box(ref_draw, box, f"reference {name}", colors[name], font)
        draw_labeled_box(cur_draw, box, f"target {name}", colors[name], font)

    if current_box:
        draw_labeled_box(cur_draw, current_box, "detected current 3D", (214, 171, 0), font)
    if current_base_box:
        draw_labeled_box(cur_draw, current_base_box, "detected current base", (0, 120, 130), font)

    gap = 28
    header = 64
    crop_h = 300
    sheet = Image.new("RGB", (width * 2 + gap, header + height + crop_h + 80), (248, 239, 229))
    sheet_draw = ImageDraw.Draw(sheet)
    sheet_draw.text((24, 18), "reference hero", fill=(30, 24, 19), font=title_font)
    sheet_draw.text((width + gap + 24, 18), "current generated hero", fill=(30, 24, 19), font=title_font)
    sheet.paste(ref_marked, (0, header))
    sheet.paste(cur_marked, (width + gap, header))

    crop_top = header + height + 34
    sheet_draw.text((24, crop_top - 28), "target object crop: reference", fill=(30, 24, 19), font=font)
    sheet_draw.text((width + gap + 24, crop_top - 28), "target object crop: current", fill=(30, 24, 19), font=font)
    ref_crop = ref_resized.crop(target.as_tuple()).resize((round(width * 0.42), crop_h), RESAMPLE)
    cur_crop = current.crop(target.as_tuple()).resize((round(width * 0.42), crop_h), RESAMPLE)
    sheet.paste(ref_crop, (24, crop_top))
    sheet.paste(cur_crop, (width + gap + 24, crop_top))

    sheet.save(COMPARISON)
    sheet.save(STANDARD_COMPARISON)

    if current_box:
        target_center = target.center
        current_center = current_box.center
        dx = round(current_center[0] - target_center[0])
        dy = round(current_center[1] - target_center[1])
        size_ratio = round((current_box.width * current_box.height) / max(1, target.width * target.height), 2)
        report = (
            f"Detected current 3D box: {current_box.as_tuple()}\n"
            f"Reference full 3D target box: {target.as_tuple()}\n"
            f"Center offset from target: x {dx}px, y {dy}px\n"
            f"Detected/target area ratio: {size_ratio}\n"
        )
    else:
        report = (
            "No current 3D object was detected in the right-side hero region.\n"
            f"Reference full 3D target box: {target.as_tuple()}\n"
        )

    if current_base_box:
        base_center = base_target.center
        current_base_center = current_base_box.center
        base_dx = round(current_base_center[0] - base_center[0])
        base_dy = round(current_base_center[1] - base_center[1])
        inside = (
            current_base_box.left >= base_target.left
            and current_base_box.right <= base_target.right
            and current_base_box.top >= base_target.top
            and current_base_box.bottom <= base_target.bottom
        )
        report += (
            f"Detected current base box: {current_base_box.as_tuple()}\n"
            f"Reference base target box: {base_target.as_tuple()}\n"
            f"Base center offset from target: x {base_dx}px, y {base_dy}px\n"
            f"Base box inside target: {inside}\n"
        )
    else:
        report += f"Detected current base box: none\nReference base target box: {base_target.as_tuple()}\n"

    return COMPARISON, report


def write_report(comparison_report: str) -> None:
    REPORT.write_text(
        "# Hero Positioning Check\n\n"
        f"- Reference image: `{REFERENCE.relative_to(ROOT)}`\n"
        f"- Current screenshot: `{SCREENSHOT.relative_to(ROOT)}`\n"
        f"- Positioning comparison image: `{COMPARISON.relative_to(ROOT)}`\n"
        f"- Standard comparison image: `{STANDARD_COMPARISON.relative_to(ROOT)}`\n"
        f"- Viewport: `{VIEWPORT[0]}x{VIEWPORT[1]}`\n\n"
        "## Measurement\n\n"
        f"```text\n{comparison_report}```\n\n"
        "## How To Read The Comparison\n\n"
        "- Blue is the full 3D composition target from the reference.\n"
        "- Green is the plant target.\n"
        "- Brown is the vase target.\n"
        "- Purple is the base target.\n"
        "- Yellow is the detected current 3D object position.\n\n"
        "- Teal is the detected current base/slab position.\n\n"
        "## Decision Rule\n\n"
        "For the path-placement pass, use the teal base/slab detection as the decisive check: it should sit inside the "
        "purple reference base band and visually touch the lower terracotta path. The yellow full-object box is only a "
        "coarse guide because the current copied plant model is taller and denser than the reference plant.\n",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-capture", action="store_true", help="Use the existing hero_generated.png screenshot.")
    args = parser.parse_args()

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    if not args.no_capture:
        capture_page(SCREENSHOT, VIEWPORT)

    reference = Image.open(REFERENCE).convert("RGB")
    current = Image.open(SCREENSHOT).convert("RGB")
    current_box = detect_current_object(current)
    _, comparison_report = make_comparison(reference, current, current_box)
    write_report(comparison_report)
    print(comparison_report)
    print(f"Saved {COMPARISON.relative_to(ROOT)}")
    print(f"Saved {STANDARD_COMPARISON.relative_to(ROOT)}")
    print(f"Saved {REPORT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
