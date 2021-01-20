from pathlib import Path

from umudugudu import data, plot


def get_data():
    df = data.get_villages()
    return df.query("Province == 'Kigali Town/Umujyi wa Kigali'")


def main():
    df_kigali = get_data()
    fig = plot.administrative_divisions(df_kigali)
    export_folder = Path("html")
    export_folder.mkdir(exist_ok=True)
    (export_folder / "index.html").write_text(fig.to_html())


if __name__ == "__main__":
    main()
