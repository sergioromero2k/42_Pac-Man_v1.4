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
ENTRY_POINT = pac-man.py
CONFIG = config.json

GREEN        = \033[0;32m
RED          = \033[0;31m
YELLOW       = \033[0;33m
RESET        = \033[0m

.PHONY: all venv install run clean_venv clean fclean debug re lint

all: run

install:
	@echo "$(YELLOW)Creating virtual environment...$(RESET)"
	$(PYTHON) -m venv venv
	@echo "$(GREEN)Installing dependencies in venv...$(RESET)"
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install flake8 mypy
	./venv/bin/pip install ./mazegenerator-2.1.0-py3-none-any.whl

run:
	@echo "$(GREEN)Running $(NAME)...$(RESET)"
	$(PYTHON) $(ENTRY_POINT) $(CONFIG)

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
	$(PYTHON) -m pdb $(ENTRY_POINT)

re: fclean run

# --- Linting (Code Quality) ----

lint: install
	@echo "$(YELLOW)Running Flake8....$(RESET)"
	-$(PYTHON) -m flake8 . --exclude=venv,test_env,env,.venv
	@echo "$(YELLOW)Running Mypy...$(RESET)"
	-$(PYTHON) -m mypy .

lint-strict: install
	@echo "$(RED)Running Flake8 strict....$(RESET)"
	-$(PYTHON) -m flake8 . --exclude=venv,test_env,env,.venv
	@echo "$(RED)Running Mypy strict...$(RESET)"
	$(ENV)/bin/mypy . --strict
