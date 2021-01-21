from pathlib import Path

from umudugudu import data, plot


def get_data():
    df = data.get_villages()
    return df.query("Province == 'Kigali Town/Umujyi wa Kigali'")


def main(opacity: float = 0.25, line_width: float = 1.5, transparent: bool = False):
    df_kigali = get_data()
    fig = plot.administrative_divisions(
        df_kigali,
        opacity=opacity,
        line_width=line_width,
        transparent=transparent,
    )
    export_folder = Path("html")
    export_folder.mkdir(exist_ok=True)
    (export_folder / f"index.html").write_text(fig.to_html())


if __name__ == "__main__":
    import typer

    typer.run(main)
