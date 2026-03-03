#!/usr/bin/env python3
"""Simple local TUI for adding/removing tags on Zola blog posts."""

from __future__ import annotations

import curses
import re
import tomllib
from dataclasses import dataclass
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
CONTENT_DIR = ROOT_DIR / "content"


@dataclass
class Post:
    path: Path
    title: str
    date: str
    tags: list[str]


def parse_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("+++\n"):
        raise ValueError("missing TOML frontmatter opening delimiter")

    close = text.find("\n+++\n", 4)
    delimiter_len = 5

    if close == -1:
        close = text.find("\n+++", 4)
        delimiter_len = 4

    if close == -1:
        raise ValueError("missing TOML frontmatter closing delimiter")

    frontmatter = text[4:close]
    body = text[close + delimiter_len :]
    return frontmatter, body


def format_tags_line(tags: list[str]) -> str:
    escaped = [tag.replace("\\", "\\\\").replace('"', '\\"') for tag in tags]
    values = ", ".join(f'"{tag}"' for tag in escaped)
    return f"tags = [{values}]"


def update_frontmatter_tags(frontmatter: str, tags: list[str]) -> str:
    lines = frontmatter.splitlines()
    tags_line = format_tags_line(tags)

    section_start = None
    for idx, line in enumerate(lines):
        if line.strip() == "[taxonomies]":
            section_start = idx
            break

    if section_start is None:
        if lines and lines[-1].strip():
            lines.append("")
        lines.extend(["[taxonomies]", tags_line])
        return "\n".join(lines).rstrip() + "\n"

    section_end = len(lines)
    for idx in range(section_start + 1, len(lines)):
        stripped = lines[idx].strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            section_end = idx
            break

    tag_line_idx = None
    for idx in range(section_start + 1, section_end):
        if re.match(r"^\s*tags\s*=", lines[idx]):
            tag_line_idx = idx
            break

    if tag_line_idx is not None:
        lines[tag_line_idx] = tags_line
    else:
        lines.insert(section_start + 1, tags_line)

    return "\n".join(lines).rstrip() + "\n"


def read_post(path: Path) -> Post | None:
    text = path.read_text(encoding="utf-8")
    frontmatter, _ = parse_frontmatter(text)
    data = tomllib.loads(frontmatter)

    date_value = data.get("date")
    if date_value is None:
        return None

    title = str(data.get("title") or path.parent.name)
    date_text = date_value.isoformat() if hasattr(date_value, "isoformat") else str(date_value)

    tags: list[str] = []
    taxonomies = data.get("taxonomies")
    if isinstance(taxonomies, dict):
        raw_tags = taxonomies.get("tags", [])
        if isinstance(raw_tags, list):
            tags = [str(tag) for tag in raw_tags]

    return Post(path=path, title=title, date=date_text, tags=sorted(set(tags), key=str.casefold))


def load_posts(content_dir: Path) -> tuple[list[Post], int]:
    posts: list[Post] = []
    skipped = 0

    for path in sorted(content_dir.rglob("index.md")):
        rel = path.relative_to(content_dir)
        if rel.parts and rel.parts[0] == "pages":
            continue
        try:
            post = read_post(path)
            if post is None:
                continue
            posts.append(post)
        except Exception:
            skipped += 1

    posts.sort(key=lambda p: (p.date, p.title), reverse=True)
    return posts, skipped


def write_post_tags(post: Post) -> None:
    text = post.path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    updated = update_frontmatter_tags(frontmatter, post.tags)
    new_text = "+++\n" + updated + "+++\n" + body
    post.path.write_text(new_text, encoding="utf-8")


def all_tags(posts: list[Post]) -> list[tuple[str, int]]:
    counts: dict[str, int] = {}
    for post in posts:
        for tag in post.tags:
            counts[tag] = counts.get(tag, 0) + 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0].casefold()))


def truncate(text: str, width: int) -> str:
    if width <= 0:
        return ""
    if len(text) <= width:
        return text
    if width == 1:
        return "…"
    return text[: width - 1] + "…"


def read_key(stdscr: curses.window):
    key = stdscr.get_wch()
    if key != "\x1b":
        return key

    # Some terminals emit arrows as ESC [ A / ESC [ B even with keypad mode.
    stdscr.nodelay(True)
    try:
        next1 = stdscr.get_wch()
        next2 = stdscr.get_wch()
    except curses.error:
        return "\x1b"
    finally:
        stdscr.nodelay(False)

    if next1 == "[" and next2 == "A":
        return curses.KEY_UP
    if next1 == "[" and next2 == "B":
        return curses.KEY_DOWN
    return "\x1b"


def prompt_text(stdscr: curses.window, label: str) -> str | None:
    h, w = stdscr.getmaxyx()
    chars: list[str] = []

    curses.noecho()
    try:
        curses.curs_set(1)
    except curses.error:
        pass

    while True:
        current = "".join(chars)
        stdscr.move(h - 1, 0)
        stdscr.clrtoeol()
        stdscr.addnstr(h - 1, 0, f"{label}{current}", max(1, w - 1))
        cursor_x = min(len(label) + len(current), max(0, w - 1))
        stdscr.move(h - 1, cursor_x)
        stdscr.refresh()

        key = read_key(stdscr)
        if key == "\x1b":
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return None
        if key in ("\n", "\r", curses.KEY_ENTER):
            try:
                curses.curs_set(0)
            except curses.error:
                pass
            return "".join(chars).strip()
        if key in (curses.KEY_BACKSPACE, "\b", "\x7f"):
            if chars:
                chars.pop()
            continue
        if isinstance(key, str) and key.isprintable():
            chars.append(key)


def pick_option(stdscr: curses.window, title: str, options: list[str]) -> int | None:
    if not options:
        return None

    selected = 0
    offset = 0

    while True:
        h, w = stdscr.getmaxyx()
        top = 2
        max_rows = max(1, h - 7)

        if selected < offset:
            offset = selected
        if selected >= offset + max_rows:
            offset = selected - max_rows + 1

        for y in range(top, h - 1):
            stdscr.move(y, 0)
            stdscr.clrtoeol()

        stdscr.addnstr(top, 0, truncate(title, w - 1), max(1, w - 1), curses.A_BOLD)
        stdscr.addnstr(top + 1, 0, "Enter select | Esc cancel | j/k move", max(1, w - 1), curses.A_DIM)

        for row in range(max_rows):
            idx = offset + row
            if idx >= len(options):
                break
            y = top + 2 + row
            attr = curses.A_REVERSE if idx == selected else curses.A_NORMAL
            line = f"{idx + 1}. {options[idx]}"
            stdscr.addnstr(y, 0, truncate(line, w - 1), max(1, w - 1), attr)

        stdscr.refresh()
        key = read_key(stdscr)

        if key == "\x1b":
            return None
        if key in ("\n", "\r", curses.KEY_ENTER):
            return selected
        if key in (curses.KEY_UP, "k"):
            selected = max(0, selected - 1)
            continue
        if key in (curses.KEY_DOWN, "j"):
            selected = min(len(options) - 1, selected + 1)
            continue


def draw(
    stdscr: curses.window,
    posts: list[Post],
    selected: int,
    status: str,
    skipped: int,
) -> None:
    stdscr.erase()
    h, w = stdscr.getmaxyx()

    header = f"Tag Manager | posts: {len(posts)}"
    if skipped:
        header += f" | skipped: {skipped}"
    stdscr.addnstr(0, 0, header, max(1, w - 1), curses.A_BOLD)

    if not posts:
        stdscr.addnstr(2, 0, "No posts found in content/", max(1, w - 1))
        stdscr.addnstr(h - 2, 0, "q quit", max(1, w - 1))
        stdscr.refresh()
        return

    list_top = 2
    list_height = max(1, h - 5)
    left_width = max(30, min(w - 20, int(w * 0.66)))
    right_x = min(w - 1, left_width + 2)

    start = max(0, selected - list_height + 1)
    if selected < start:
        start = selected

    stdscr.addnstr(1, 0, "Posts", max(1, left_width), curses.A_UNDERLINE)
    stdscr.addnstr(1, right_x, "Tags", max(1, w - right_x - 1), curses.A_UNDERLINE)

    for row in range(list_height):
        idx = start + row
        if idx >= len(posts):
            break

        y = list_top + row
        post = posts[idx]
        tag_text = ", ".join(post.tags) if post.tags else "-"
        line = f"{post.date} | {post.title} | {tag_text}"
        attr = curses.A_REVERSE if idx == selected else curses.A_NORMAL
        stdscr.addnstr(y, 0, truncate(line, left_width), max(1, left_width), attr)

    tag_items = all_tags(posts)
    for row in range(list_height):
        if row >= len(tag_items):
            break
        y = list_top + row
        tag, count = tag_items[row]
        stdscr.addnstr(y, right_x, truncate(f"{tag} ({count})", w - right_x - 1), max(1, w - right_x - 1))

    help_text = "j/k or arrows move | a pick/add tag | r pick tag to remove | q quit"
    stdscr.addnstr(h - 2, 0, truncate(help_text, w - 1), max(1, w - 1), curses.A_DIM)
    stdscr.addnstr(h - 1, 0, truncate(status, w - 1), max(1, w - 1))
    stdscr.refresh()


def run(stdscr: curses.window) -> None:
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    try:
        curses.curs_set(0)
    except curses.error:
        pass

    posts, skipped = load_posts(CONTENT_DIR)
    selected = 0
    status = "Ready"

    while True:
        draw(stdscr, posts, selected, status, skipped)
        key = read_key(stdscr)

        if key in ("q", "Q"):
            return

        if not posts:
            continue

        if key in (curses.KEY_UP, "k"):
            selected = max(0, selected - 1)
            continue

        if key in (curses.KEY_DOWN, "j"):
            selected = min(len(posts) - 1, selected + 1)
            continue

        post = posts[selected]

        if key in ("a", "A"):
            existing_tags = [tag for tag, _ in all_tags(posts) if tag not in post.tags]
            add_options = ["Add new tag..."] + existing_tags
            picked_idx = pick_option(stdscr, "Pick tag to add (Esc cancel):", add_options)
            if picked_idx is None:
                status = "Add cancelled"
                continue
            if picked_idx == 0:
                tag = prompt_text(stdscr, "Add new tag (Esc cancel): ")
                if tag is None:
                    status = "Add cancelled"
                    continue
            else:
                tag = add_options[picked_idx]
            if not tag:
                status = "Tag cannot be empty"
                continue
            if tag in post.tags:
                status = f"Tag already present: {tag}"
                continue
            post.tags = sorted(set(post.tags + [tag]), key=str.casefold)
            write_post_tags(post)
            status = f"Added '{tag}' to: {post.title}"
            continue

        if key in ("r", "R"):
            if not post.tags:
                status = "Post has no tags"
                continue
            picked_idx = pick_option(stdscr, "Pick tag to remove (Esc cancel):", post.tags)
            if picked_idx is None:
                status = "Remove cancelled"
                continue
            tag = post.tags[picked_idx]
            post.tags = [t for t in post.tags if t != tag]
            write_post_tags(post)
            status = f"Removed '{tag}' from: {post.title}"
            continue

        status = "Unknown key"


def main() -> None:
    if not CONTENT_DIR.exists():
        raise SystemExit(f"content directory not found: {CONTENT_DIR}")
    curses.wrapper(run)


if __name__ == "__main__":
    main()
