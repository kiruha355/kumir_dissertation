from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "data" / "boar_matrix.txt"
KUMIR_PATH = ROOT / "kumir" / "boar_robot.kum"
SVG_PATH = ROOT / "preview" / "boar_pixel.svg"
PNG_PATH = ROOT / "preview" / "boar_pixel.png"
PIXEL_SIZE = 12
PAINTED = {"1", "2", "3", "4", "P"}
COLORS = {
    ".": "#f2eee8",
    "1": "#1c1714",
    "2": "#3d3128",
    "3": "#725c43",
    "4": "#a4875d",
    "E": "#f0ddaf",
    "P": "#100b09",
}


def read_matrix():
    rows = MATRIX_PATH.read_text(encoding="utf-8").splitlines()
    width = max(len(row) for row in rows)
    return [row.ljust(width, ".") for row in rows]


def write_svg(rows):
    width = len(rows[0])
    height = len(rows)
    canvas_width = width * PIXEL_SIZE
    canvas_height = height * PIXEL_SIZE
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {canvas_width} {canvas_height}" width="{canvas_width}" height="{canvas_height}">',
        f'<rect width="{canvas_width}" height="{canvas_height}" fill="{COLORS["."]}"/>',
    ]

    for y, row in enumerate(rows):
        for x, symbol in enumerate(row):
            if symbol == ".":
                continue
            color = COLORS.get(symbol, COLORS["1"])
            parts.append(
                f'<rect x="{x * PIXEL_SIZE}" y="{y * PIXEL_SIZE}" width="{PIXEL_SIZE}" height="{PIXEL_SIZE}" fill="{color}"/>'
            )

    parts.append("</svg>")
    SVG_PATH.write_text("\n".join(parts) + "\n", encoding="utf-8")


def write_png(rows):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        return

    width = len(rows[0])
    height = len(rows)
    image = Image.new("RGB", (width * PIXEL_SIZE, height * PIXEL_SIZE), COLORS["."])
    draw = ImageDraw.Draw(image)

    for y, row in enumerate(rows):
        for x, symbol in enumerate(row):
            if symbol == ".":
                continue
            color = COLORS.get(symbol, COLORS["1"])
            left = x * PIXEL_SIZE
            top = y * PIXEL_SIZE
            draw.rectangle(
                (left, top, left + PIXEL_SIZE - 1, top + PIXEL_SIZE - 1),
                fill=color,
            )

    image.save(PNG_PATH)


def move(lines, current_x, current_y, target_x, target_y):
    while current_x < target_x:
        lines.append("  вправо")
        current_x += 1
    while current_x > target_x:
        lines.append("  влево")
        current_x -= 1
    while current_y < target_y:
        lines.append("  вниз")
        current_y += 1
    while current_y > target_y:
        lines.append("  вверх")
        current_y -= 1
    return current_x, current_y


def write_kumir(rows):
    lines = ["использовать Робот", "", "алг основная", "нач"]
    current_x = 0
    current_y = 0

    for y, row in enumerate(rows):
        indexes = range(len(row)) if y % 2 == 0 else range(len(row) - 1, -1, -1)
        for x in indexes:
            if row[x] not in PAINTED:
                continue
            current_x, current_y = move(lines, current_x, current_y, x, y)
            lines.append("  закрасить")

    lines.append("кон")
    KUMIR_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    rows = read_matrix()
    write_svg(rows)
    write_png(rows)
    write_kumir(rows)


if __name__ == "__main__":
    main()
