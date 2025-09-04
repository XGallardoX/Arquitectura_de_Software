import argparse
import subprocess
import sys
from pathlib import Path

from backend.datapp.dashboard import run_dashboard


def run_django() -> None:
    """Run the Django development server."""
    manage_py = Path(__file__).resolve().parent / "backend" / "webapp" / "manage.py"
    subprocess.run([sys.executable, str(manage_py), "runserver"], check=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="CLI para levantar el dashboard de Streamlit o el servidor Django",
    )
    parser.add_argument(
        "--app",
        choices=["dashboard", "server"],
        default="dashboard",
        help=(
            "Elige 'dashboard' para Streamlit (por defecto) "
            "o 'server' para Django"
        ),
    )
    args = parser.parse_args()

    if args.app == "dashboard":
        run_dashboard()
    else:
        run_django()


if __name__ == "__main__":
    main()
