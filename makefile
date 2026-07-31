VENV        = .venv

MAIN        = pac-man.py

LOCAL_DEPS  = lib/mazegenerator-2.1.0-py3-none-any.whl

FLAKE = flake8
MYPY  = mypy

MYPY_FLAGS = \
	--warn-return-any           \
	--warn-unused-ignores       \
	--ignore-missing-imports    \
	--disallow-untyped-defs     \
	--check-untyped-defs


run:
	uv run src/$(MAIN)

lint: install
	uv run $(FLAKE) . --exclude $(VENV)
	uv run $(MYPY) $(MYPY_FLAGS) .

lint-strict: install
	uv run $(FLAKE) . --exclude $(VENV)
	uv run $(MYPY) --strict .

clean:
	uv clean
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +

.PHONY: install run debug test lint lint-strict profiler clean