# LaTeX Workspace Makefile
# Simplified unified Makefile for LaTeX projects

# Try to use system latexmk first, fallback to virtual env if available
LATEXMK := $(shell command -v latexmk 2>/dev/null || echo ".venv/bin/latexmk")

# Default target
.PHONY: help
help:
	@echo "LaTeX Workspace Commands"
	@echo "======================="
	@echo "compile      - Compile main LaTeX document"
	@echo "cv           - Compile CV template (generates Helio_Fernandes_CV_2025.pdf)"
	@echo "watch        - Watch for changes and auto-compile main document"
	@echo "clean        - Clean auxiliary LaTeX files"
	@echo "install      - Install system LaTeX packages (requires sudo)"
	@echo "check        - Check LaTeX installation"

# Compile main document
.PHONY: compile
compile:
	@if [ -f "main.tex" ]; then \
		$(LATEXMK) -pdf main.tex; \
	else \
		echo "No main.tex found. Use 'make cv' for CV template or specify a LaTeX file"; \
	fi

# Compile CV template
.PHONY: cv
cv:
	@if [ -f "helio_fernandes_pt.tex" ]; then \
		$(LATEXMK) -pdf helio_fernandes_pt.tex; \
	elif [ -f "templates/cv/helio_fernandes_pt.tex" ]; then \
		cd templates/cv && $(LATEXMK) -pdf helio_fernandes_pt.tex; \
	else \
		echo "No helio_fernandes_pt.tex found in current directory or templates/cv/"; \
	fi

# Watch for changes and auto-compile
.PHONY: watch
watch:
	@if [ -f "main.tex" ]; then \
		$(LATEXMK) -pdf -pvc main.tex; \
	else \
		echo "No main.tex found. Please specify a LaTeX file"; \
	fi

# Clean auxiliary files
.PHONY: clean
clean:
	@echo "Cleaning auxiliary LaTeX files..."
	@find . -name "*.aux" -delete 2>/dev/null || true
	@find . -name "*.log" -delete 2>/dev/null || true
	@find . -name "*.bbl" -delete 2>/dev/null || true
	@find . -name "*.blg" -delete 2>/dev/null || true
	@find . -name "*.toc" -delete 2>/dev/null || true
	@find . -name "*.out" -delete 2>/dev/null || true
	@find . -name "*.fdb_latexmk" -delete 2>/dev/null || true
	@find . -name "*.fls" -delete 2>/dev/null || true
	@find . -name "*.synctex.gz" -delete 2>/dev/null || true
	@find . -name "helio_fernandes_*.pdf" -delete 2>/dev/null || true
	@echo "Auxiliary files cleaned"

# Install system LaTeX packages
.PHONY: install
install:
	@echo "Installing system LaTeX packages..."
	@if command -v apt-get >/dev/null 2>&1; then \
		sudo apt-get update && sudo apt-get install -y \
			texlive-latex-base \
			texlive-latex-recommended \
			texlive-latex-extra \
			texlive-fonts-recommended \
			texlive-fonts-extra \
			texlive-bibtex-extra \
			latexmk; \
	elif command -v pacman >/dev/null 2>&1; then \
		sudo pacman -S texlive-core texlive-latexextra texlive-bibtexextra; \
	else \
		echo "Please install LaTeX manually for your system"; \
	fi

# Check LaTeX installation
.PHONY: check
check:
	@echo "Checking LaTeX installation..."
	@if command -v latexmk >/dev/null 2>&1; then \
		echo "✓ latexmk available"; \
		latexmk --version | head -1; \
	else \
		echo "✗ latexmk not found"; \
		echo ""; \
		echo "Install instructions:"; \
		if command -v pacman >/dev/null 2>&1; then \
			echo "  Arch Linux: sudo pacman -S texlive-core texlive-latexextra texlive-binextra"; \
			echo "  Wiki: https://wiki.archlinux.org/title/TeX_Live"; \
		elif command -v apt-get >/dev/null 2>&1; then \
			echo "  Debian/Ubuntu: sudo apt-get install texlive-latex-base texlive-latex-extra latexmk"; \
			echo "  Docs: https://www.tug.org/texlive/"; \
		elif command -v dnf >/dev/null 2>&1; then \
			echo "  Fedora: sudo dnf install texlive-scheme-medium latexmk"; \
			echo "  Docs: https://www.tug.org/texlive/"; \
		else \
			echo "  Visit: https://www.tug.org/texlive/"; \
		fi; \
	fi
	@if command -v pdflatex >/dev/null 2>&1; then \
		echo "✓ pdflatex available"; \
	else \
		echo "✗ pdflatex not found"; \
		echo ""; \
		echo "Install instructions:"; \
		if command -v pacman >/dev/null 2>&1; then \
			echo "  Arch Linux: sudo pacman -S texlive-core texlive-latexextra"; \
			echo "  Wiki: https://wiki.archlinux.org/title/TeX_Live"; \
		elif command -v apt-get >/dev/null 2>&1; then \
			echo "  Debian/Ubuntu: sudo apt-get install texlive-latex-base texlive-latex-recommended"; \
			echo "  Docs: https://www.tug.org/texlive/"; \
		elif command -v dnf >/dev/null 2>&1; then \
			echo "  Fedora: sudo dnf install texlive-scheme-medium"; \
			echo "  Docs: https://www.tug.org/texlive/"; \
		else \
			echo "  Visit: https://www.tug.org/texlive/"; \
		fi; \
	fi