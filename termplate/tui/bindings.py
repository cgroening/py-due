from pathlib import Path
from termz.tui.custom_bindings import CustomBindings

BINDINGS_FILE = Path(__file__).parent / 'bindings.yaml'
CUSTOM_BINDINGS = CustomBindings(str(BINDINGS_FILE))
