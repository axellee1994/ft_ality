.PHONY: build run test clean

PYTHON := python3
GRAMMAR := grammars/mk9.gmr

build: ft_ality
	$(PYTHON) -m py_compile main.py

ft_ality:
	@echo '#!/bin/bash' > ft_ality
	@echo 'exec $(PYTHON) $$(dirname $$0)/main.py "$$@"' >> ft_ality
	@chmod +x ft_ality

run: ft_ality
	./ft_ality $(GRAMMAR)

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	rm -f ft_ality
