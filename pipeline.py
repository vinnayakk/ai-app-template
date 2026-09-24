import csv
import json
import sys

from dotenv import load_dotenv

from generate_copy import generate_copy
from generate_ad_image_brand import generate_image

load_dotenv()


def run_pipeline(brief_path: str, count: int = 5):
    with open(brief_path) as f:
        brief = json.load(f)

    variants = generate_copy(brief, count=count)

    rows = []
    for variant in variants:
        print(f"Generating image for variant {variant.variant_number}...")
        image_path = generate_image(brief, variant.model_dump())
        row = variant.model_dump()
        row["image_path"] = image_path
        rows.append(row)

    safe_name = brief["brand"]["name"].lower().replace(" ", "_")
    output_csv = f"{safe_name}_pipeline_results.csv"

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(
            f, fieldnames=["variant_number", "headline", "body", "cta", "image_path"]
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Done. Wrote {len(rows)} rows to {output_csv}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python pipeline.py <brief.json>")
        sys.exit(1)

    run_pipeline(sys.argv[1])