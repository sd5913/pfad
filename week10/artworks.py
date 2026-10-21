"""A tiny, local class-and-JSON example. Run from the pfad repository root."""

import argparse
import json
from pathlib import Path


class Artwork:
    def __init__(self, id, title, views, exhibition_id):
        self.id = id
        self.title = title
        self.views = views
        self.exhibition_id = exhibition_id

    def view(self):
        self.views += 1


def record_for(artwork):
    return {
        "id": artwork.id,
        "title": artwork.title,
        "views": artwork.views,
        "exhibition_id": artwork.exhibition_id,
    }


def save(path, broken_link=False):
    amber = Artwork("a1", "Amber", 2, "e1")
    blue = Artwork("a2", "Blue", 7, "e99" if broken_link else "e1")
    amber.view()
    print(f"After amber.view(): a1={amber.views}, a2={blue.views}")

    data = {
        "exhibitions": [{"id": "e1", "name": "Night"}],
        "artworks": [record_for(amber), record_for(blue)],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation avoids silently replacing someone's earlier work.
    with path.open("x", encoding="utf-8") as output:
        json.dump(data, output, indent=2)
        output.write("\n")
    print(f"Saved {path}")


def load(path):
    with path.open(encoding="utf-8") as source:
        data = json.load(source)

    exhibition_ids = {record["id"] for record in data["exhibitions"]}
    artworks = [
        Artwork(record["id"], record["title"], record["views"], record["exhibition_id"])
        for record in data["artworks"]
    ]
    for artwork in artworks:
        if artwork.exhibition_id not in exhibition_ids:
            raise ValueError(
                f"Unresolved exhibition_id {artwork.exhibition_id} for artwork {artwork.id}"
            )
        print(f"{artwork.id}: {artwork.title}, views={artwork.views}, exhibition={artwork.exhibition_id}")

    # This is a new in-memory object. The JSON file still has the saved count.
    artworks[0].view()
    print(f"After reload + view(): {artworks[0].id}={artworks[0].views} (not saved)")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("save", "load"))
    parser.add_argument("--file", type=Path, required=True, help="explicit local JSON path")
    parser.add_argument("--broken-link", action="store_true", help="save a deliberately broken e99 link")
    args = parser.parse_args()
    if args.broken_link and args.action != "save":
        parser.error("--broken-link is only for save")

    try:
        if args.action == "save":
            save(args.file, broken_link=args.broken_link)
        else:
            load(args.file)
    except (FileNotFoundError, FileExistsError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        parser.exit(1, f"Cannot {args.action}: {error}\n")


if __name__ == "__main__":
    main()
