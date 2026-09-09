#!/usr/bin/env python3
"""
pad_diagram.py - Aspect Ratio Auto-Padding Utility for Mermaid Diagrams

Part of jk-agy-mermaid plugin.
Inspects PNG diagram dimensions, evaluates the vertical aspect ratio (H / W),
and symmetrically pads margins with pure white (#FFFFFF) to guarantee that
H / W <= max_ratio (default: 1.15).

This ensures optimal fitting within Google Docs Pageless/Standard pages,
slides, and PDF deliverables without vertical overflow or horizontal distortion.
"""

import os
import sys
import argparse
from PIL import Image


def pad_diagram(
    input_path: str,
    output_path: str = None,
    max_ratio: float = 1.15,
    margin_ratio: float = 0.03,
    background_color: tuple = (255, 255, 255),
    quiet: bool = False
) -> str:
    """Pads a diagram image to satisfy H / W <= max_ratio with clean margins."""
    abs_input = os.path.abspath(input_path)
    if not os.path.exists(abs_input):
        raise FileNotFoundError(f"Input image not found: {abs_input}")

    if output_path is None:
        base, ext = os.path.splitext(abs_input)
        if base.endswith("_padded"):
            output_path = abs_input
        else:
            output_path = f"{base}_padded{ext}"
    else:
        output_path = os.path.abspath(output_path)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with Image.open(abs_input) as im:
        # Convert to RGB if RGBA/P to ensure pure white padding background
        if im.mode in ("RGBA", "LA", "P"):
            rgb_im = Image.new("RGB", im.size, background_color)
            rgb_im.paste(im, mask=im.split()[-1] if im.mode in ("RGBA", "LA") else None)
            im = rgb_im
        else:
            im = im.convert("RGB")

        w, h = im.size
        ratio = h / w

        target_w = int(h / max_ratio)
        if target_w > w:
            # Diagram is too tall (vertical tower). Pad width symmetrically.
            pad_x = (target_w - w) // 2
            padded = Image.new("RGB", (target_w, h), background_color)
            padded.paste(im, (pad_x, 0))
            if not quiet:
                print(f"[pad_diagram] {os.path.basename(abs_input)}: {w}x{h} (H/W = {ratio:.2f} > {max_ratio:.2f})")
                print(f"  -> Padded horizontally to: {target_w}x{h} (H/W = {h/target_w:.2f})")
        else:
            # Diagram aspect ratio is acceptable. Apply subtle breathing margin.
            m = max(1, int(w * margin_ratio))
            new_w = w + 2 * m
            new_h = h + 2 * m
            padded = Image.new("RGB", (new_w, new_h), background_color)
            padded.paste(im, (m, m))
            if not quiet:
                print(f"[pad_diagram] {os.path.basename(abs_input)}: {w}x{h} (H/W = {ratio:.2f} <= {max_ratio:.2f})")
                print(f"  -> Added {m}px breathing margin: {new_w}x{new_h} (H/W = {new_h/new_w:.2f})")

        padded.save(output_path, "PNG", quality=95)
        if not quiet:
            print(f"[pad_diagram] Saved calibrated asset: {output_path}")

    return output_path


def main():
    parser = argparse.ArgumentParser(
        description="Aspect ratio padding utility for Mermaid PNGs (H/W <= 1.15 calibration)"
    )
    parser.add_argument("input", help="Path to input PNG image or directory of images")
    parser.add_argument("-o", "--output", help="Path to output PNG image (optional)")
    parser.add_argument(
        "--max-ratio",
        type=float,
        default=1.15,
        help="Maximum allowable vertical ratio H / W (default: 1.15)"
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=0.03,
        help="Proportional breathing margin for already compliant images (default: 0.03)"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", help="Suppress diagnostic output"
    )

    args = parser.parse_args()

    if os.path.isdir(args.input):
        files = [
            os.path.join(args.input, f)
            for f in os.listdir(args.input)
            if f.lower().endswith(".png") and not f.endswith("_padded.png")
        ]
        if not files:
            print(f"No non-padded PNG files found in {args.input}")
            sys.exit(0)
        for f in sorted(files):
            pad_diagram(f, max_ratio=args.max_ratio, margin_ratio=args.margin, quiet=args.quiet)
    else:
        pad_diagram(
            args.input,
            output_path=args.output,
            max_ratio=args.max_ratio,
            margin_ratio=args.margin,
            quiet=args.quiet
        )


if __name__ == "__main__":
    main()
