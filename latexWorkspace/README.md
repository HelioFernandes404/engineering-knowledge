# LaTeX Workspace

This workspace is organized to help you manage LaTeX projects efficiently.

## Directory Structure

```
LaTeX/
├── templates/          # Ready-to-use LaTeX templates
│   ├── article/        # Academic article template
│   ├── report/         # Report template
│   ├── book/           # Book template
│   ├── beamer/         # Presentation template
│   └── cv/             # CV/Resume template
├── projects/           # Your active projects
├── assets/             # Shared resources
│   ├── images/         # Images and figures
│   ├── logos/          # Logos and branding
│   └── fonts/          # Custom fonts
├── bibliography/       # Shared bibliography files
└── styles/             # Custom style files and packages
```

## Getting Started

1. **Using Templates**: Copy a template from the `templates/` directory to `projects/` and rename it for your project.

2. **Managing Assets**: Store reusable images, logos, and fonts in the `assets/` directory.

3. **Bibliography**: Use the shared `bibliography/references.bib` file or create project-specific ones.

4. **Compilation**: Use your preferred LaTeX compiler (pdflatex, xelatex, lualatex) to build documents.

## Common Commands

```bash
# Compile a LaTeX document
pdflatex main.tex

# Compile with bibliography
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex

# Clean auxiliary files
rm -f *.aux *.log *.bbl *.blg *.toc *.out *.fdb_latexmk *.fls
```

## Tips

- Keep project-specific files in separate directories under `projects/`
- Use relative paths when referencing shared assets
- Consider using latexmk for automated compilation
- Use version control (git) for important projects