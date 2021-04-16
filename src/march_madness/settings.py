import os

from pathlib import Path


PROJ_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = Path(Path(PROJ_DIR).parent).parent
DATA_DIR = os.path.join(ROOT_DIR, "data")
BRACKET_DIR = os.path.join(DATA_DIR, "brackets")
CONFERENCE_WITH_TEAM_DIR = os.path.join(DATA_DIR, "conferences")
CONFERENCE_OVERALL_DIR = os.path.join(DATA_DIR, "overall")
INDEX_DIR = os.path.join(DATA_DIR, "indexes")

TEAM_YEARS = list(range(2000, 2022))
ACTUAL_EXCLUDE_YEARS = [2020, 2021]

