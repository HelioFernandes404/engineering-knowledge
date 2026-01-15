# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## IDE Integration

This workspace uses the LaTeX Workshop extension for VS Code, which provides:
- Automatic compilation on save
- Live PDF preview with SyncTeX
- Intellisense for citations and references
- Error parsing and navigation
- Built-in snippet support

### VS Code Commands
- `Ctrl+Alt+B`: Build LaTeX project
- `Ctrl+Alt+V`: View PDF
- `Ctrl+Alt+J`: Navigate to source from PDF (SyncTeX)
- `Ctrl+Alt+C`: Clean auxiliary files

## Common Commands

### Manual Compilation (when needed)
```bash
# Basic compilation
pdflatex main.tex

# With bibliography support
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Using latexmk (automated compilation)
latexmk -pdf main.tex
latexmk -pvc main.tex  # continuous compilation

# Clean auxiliary files
rm -f *.aux *.log *.bbl *.blg *.toc *.out *.fdb_latexmk *.fls
# or
latexmk -c
```

## Project Architecture

This is a LaTeX workspace organized around templates and shared resources:

- **templates/**: Ready-to-use LaTeX templates (article, report, book, beamer, cv)
- **projects/**: Active projects (copy templates here to start new work)
- **assets/**: Shared resources (images/, logos/, fonts/)
- **bibliography/**: Shared bibliography files (references.bib)
- **styles/**: Custom style files and packages

### Working with Projects
1. Copy a template from `templates/` to `projects/` for new work
2. Templates reference shared bibliography as `references` (no path needed)
3. Use relative paths when referencing shared assets from `assets/`

### Template Structure
- Article template: Basic academic paper with abstract, sections, bibliography
- CV template: Professional resume with custom formatting and sections
- Bibliography: BibTeX format with example entries for articles, books, and conference papers

All templates use standard LaTeX packages (amsmath, graphicx, hyperref, geometry) and are configured for A4 paper with reasonable margins.

### CV Template Specific Commands
The CV template uses descriptive filenames for easy identification:

```bash
# Compile CV (Portuguese version)
latexmk -pdf helio_fernandes_pt.tex  # generates helio_fernandes_pt.pdf
make cv              # alternative using Makefile from root

# Clean CV files
make clean
```

The CV template uses `.latexmkrc` to automatically name the output PDF as `helio_fernandes_pt.pdf`. The filename pattern supports multiple language versions (_pt, _en, _es, etc), making it easy to maintain CVs in different languages.