############################################################
# ██████╗  █████╗  ██████╗    ███╗   ███╗ █████╗ ███╗   ██╗
# ██╔══██╗██╔══██╗██╔════╝    ████╗ ████║██╔══██╗████╗  ██║
# ██████╔╝███████║██║         ██╔████╔██║███████║██╔██╗ ██║
# ██╔═══╝ ██╔══██║██║         ██║╚██╔╝██║██╔══██║██║╚██╗██║
# ██║     ██║  ██║╚██████╗    ██║ ╚═╝ ██║██║  ██║██║ ╚████║
# ╚═╝     ╚═╝  ╚═╝ ╚═════╝    ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝
############################################################

NAME = pac_man
PYTHON = python3
VENV_PYTHON = ./venv/bin/python

ENTRY_POINT = pac-man.py
CONFIG = config.json

GREEN        = \033[0;32m
RED          = \033[0;31m
YELLOW       = \033[0;33m
RESET        = \033[0m

.PHONY: all install run clean_venv clean fclean debug re lint lint-strict

all: run

install:
	@echo "$(YELLOW)Creating virtual environment...$(RESET)"
	$(PYTHON) -m venv venv
	@echo "$(GREEN)Installing dependencies in venv...$(RESET)"
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install flake8 mypy
	./venv/bin/pip install ./mazegenerator-2.1.0-py3-none-any.whl
	./venv/bin/pip install arcade==3.3.3

run:
	@echo "$(GREEN)Running $(NAME)...$(RESET)"
	$(VENV_PYTHON) $(ENTRY_POINT) $(CONFIG)

clean_venv:
	@echo "$(RED)Removing virtual environment...$(RESET)"
	rm -rf venv

clean:
	@echo "$(RED)Cleaning caches and temporary files...$(RESET)"
	rm -rf __pycache__
	rm -rf .mypy_cache
	rm -rf .pytest_cache
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name "__pycache__" -exec rm -rf {} +

fclean: clean clean_venv

debug:
	@echo "$(YELLOW)Running in debug mode...$(RESET)"
	$(VENV_PYTHON) -m pdb $(ENTRY_POINT) $(CONFIG)

re: fclean install run

# --- Linting (Code Quality) ----

lint:
	@echo "$(YELLOW)Running Flake8....$(RESET)"
	-$(VENV_PYTHON) -m flake8 . --exclude=venv,test_env,env,.venv
	@echo "$(YELLOW)Running Mypy...$(RESET)"
	-$(VENV_PYTHON) -m mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	@echo "$(RED)Running Flake8 strict....$(RESET)"
	-$(VENV_PYTHON) -m flake8 . --exclude=venv,test_env,env,.venv
	@echo "$(RED)Running Mypy strict...$(RESET)"
	-$(VENV_PYTHON) -m mypy . --strict
