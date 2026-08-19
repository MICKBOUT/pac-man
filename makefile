VENV        = .venv

SRC_DIR			= src
MAIN        = $(SRC_DIR)/pac-man.py

LOCAL_DEPS  = lib/mazegenerator-2.1.0-py3-none-any.whl
DIST_DIR    = dist/linux
PACKAGE_DIR = $(DIST_DIR)/pac-man
PACKAGE_ZIP = $(DIST_DIR)/pac-man-linux.zip

FLAKE = flake8
MYPY  = mypy

MYPY_FLAGS = \
	--warn-return-any           \
	--warn-unused-ignores       \
	--ignore-missing-imports    \
	--disallow-untyped-defs     \
	--check-untyped-defs

install:
	uv sync

run:
	uv run $(MAIN) config.json

lint: install
	uv run $(FLAKE) . --exclude $(VENV)
	uv run $(MYPY) . $(MYPY_FLAGS)

lint-strict: install
	uv run $(FLAKE) . --exclude $(VENV)
	uv run $(MYPY) . --strict

debug: install
	uv run -m pdb $(MAIN) config.json

package:
	rm -rf build/pyinstaller $(PACKAGE_DIR) $(PACKAGE_ZIP)
	uv run pyinstaller --noconfirm --clean --workpath build/pyinstaller --distpath $(DIST_DIR) pac-man.spec
	cp config.json $(PACKAGE_DIR)/config.json
	printf '[]\n' > $(PACKAGE_DIR)/scores.json
	cp README.md $(PACKAGE_DIR)/README.txt
	cd $(DIST_DIR) && zip -qr pac-man-linux.zip pac-man


clean:
	uv clean
	rm -rf $(VENV)
	rm -rf build/pyinstaller
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

clean-package:
	rm -rf build/pyinstaller $(PACKAGE_DIR)
	rm -f $(PACKAGE_ZIP)

.PHONY: install run debug package test lint lint-strict profiler clean clean-package
