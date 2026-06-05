"""Run once to initialize database and create initial alembic revision if needed."""
from pathlib import Path
import subprocess
import sys


def main():
    here = Path(__file__).parent.parent
    print("Initializing DB (ensure DATABASE_URL is set in environment)...")
    # Create alembic env if not exists
    alembic_dir = here / "backend" / "alembic"
    if not alembic_dir.exists():
        print("No alembic directory found; create migrations with 'alembic init' manually")
        return
    # Run alembic upgrade head
    subprocess.check_call([sys.executable, "-m", "alembic", "upgrade", "head"], cwd=here / "backend")


if __name__ == "__main__":
    main()
