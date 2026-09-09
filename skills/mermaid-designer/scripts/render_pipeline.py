#!/usr/bin/env python3
"""
render_pipeline.py - Unified Native Cloudtop Mermaid Rendering & Aspect Ratio Pipeline

Part of jk-agy-mermaid plugin.
Orchestrates:
1. Native Headless Chrome 3x HiDPI rendering via local Puppeteer & Iconify packs (render_native.js)
2. Aspect ratio evaluation and white canvas auto-padding (pad_diagram.py) to guarantee H / W <= 1.15.

Usage:
  python3 render_pipeline.py diagram.mmd
  python3 render_pipeline.py diagram.mmd -o custom_output.png
  python3 render_pipeline.py /path/to/diagrams/ --batch
"""

import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

# Local import from same scripts directory
SCRIPT_DIR = Path(__file__).resolve().parent
RENDER_NATIVE_JS = SCRIPT_DIR / "render_native.js"

try:
    from pad_diagram import pad_diagram
except ImportError:
    # Fallback to absolute import
    sys.path.insert(0, str(SCRIPT_DIR))
    from pad_diagram import pad_diagram


def render_and_pad(
    mmd_path: str,
    output_png: str = None,
    scale: int = 3,
    max_ratio: float = 1.15,
    margin: float = 0.03,
    skip_padding: bool = False,
    copy_to_brain: bool = False,
    brain_dir: str = None
) -> dict:
    """Executes the complete rendering and padding pipeline for a single .mmd file."""
    abs_mmd = os.path.abspath(mmd_path)
    if not os.path.exists(abs_mmd):
        raise FileNotFoundError(f"Input file not found: {abs_mmd}")

    if output_png is None:
        base, _ = os.path.splitext(abs_mmd)
        raw_png = f"{base}.png"
    else:
        raw_png = os.path.abspath(output_png)

    print(f"🎨 [1/2] Rendering native 3x HiDPI PNG: {os.path.basename(abs_mmd)} -> {os.path.basename(raw_png)}")
    cmd = [
        "node",
        str(RENDER_NATIVE_JS),
        abs_mmd,
        raw_png,
        "--scale",
        str(scale)
    ]

    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"❌ Render failed with exit code {res.returncode}:\n{res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)

    results = {"raw_png": raw_png}

    if not skip_padding:
        print(f"📐 [2/2] Calibrating aspect ratio and white padding (H/W <= {max_ratio:.2f})...")
        padded_png = pad_diagram(
            raw_png,
            max_ratio=max_ratio,
            margin_ratio=margin,
            quiet=False
        )
        results["padded_png"] = padded_png
        primary_asset = padded_png
    else:
        primary_asset = raw_png

    if copy_to_brain and brain_dir:
        os.makedirs(brain_dir, exist_ok=True)
        dest = os.path.join(brain_dir, os.path.basename(primary_asset))
        shutil.copy2(primary_asset, dest)
        results["brain_asset"] = dest
        print(f"🧠 Mirrored to conversation artifacts: {dest}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Unified Cloudtop Native Mermaid Rendering & Aspect Ratio Pipeline (jk-agy-mermaid)"
    )
    parser.add_argument("input", help="Path to .mmd file or directory containing .mmd files")
    parser.add_argument("-o", "--output", help="Explicit path for output PNG (single file mode only)")
    parser.add_argument("--scale", type=int, default=3, help="HiDPI device scale factor (default: 3)")
    parser.add_argument(
        "--max-ratio",
        type=float,
        default=1.15,
        help="Maximum allowable vertical ratio H / W before horizontal padding (default: 1.15)"
    )
    parser.add_argument(
        "--margin",
        type=float,
        default=0.03,
        help="Proportional breathing room margin (default: 0.03)"
    )
    parser.add_argument(
        "--no-pad",
        action="store_true",
        help="Skip aspect ratio padding, outputting only raw HiDPI PNG"
    )
    parser.add_argument(
        "--copy-to-brain",
        action="store_true",
        help="Copy resulting PNG into active Jetski conversation brain directory"
    )
    parser.add_argument(
        "--brain-dir",
        help="Path to active Jetski conversation brain directory (defaults to $APP_DATA_DIR/brain/$CONVERSATION_ID if set)"
    )

    args = parser.parse_args()

    # Determine brain directory if requested
    brain_dir = args.brain_dir
    if args.copy_to_brain and not brain_dir:
        conv_id = os.environ.get("CONVERSATION_ID")
        if conv_id:
            brain_dir = os.path.expanduser(f"~/.gemini/jetski/brain/{conv_id}")

    input_path = os.path.abspath(args.input)

    if os.path.isdir(input_path):
        mmd_files = sorted([
            os.path.join(input_path, f)
            for f in os.listdir(input_path)
            if f.lower().endswith(".mmd")
        ])
        if not mmd_files:
            print(f"No .mmd files found in directory: {input_path}")
            sys.exit(0)

        print(f"🚀 Batch processing {len(mmd_files)} diagrams in {input_path}...")
        for mmd in mmd_files:
            try:
                render_and_pad(
                    mmd,
                    scale=args.scale,
                    max_ratio=args.max_ratio,
                    margin=args.margin,
                    skip_padding=args.no_pad,
                    copy_to_brain=args.copy_to_brain,
                    brain_dir=brain_dir
                )
            except Exception as e:
                print(f"⚠️ Error rendering {os.path.basename(mmd)}: {e}", file=sys.stderr)
    else:
        render_and_pad(
            input_path,
            output_png=args.output,
            scale=args.scale,
            max_ratio=args.max_ratio,
            margin=args.margin,
            skip_padding=args.no_pad,
            copy_to_brain=args.copy_to_brain,
            brain_dir=brain_dir
        )


if __name__ == "__main__":
    main()
