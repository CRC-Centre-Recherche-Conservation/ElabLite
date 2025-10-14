# Contributing to ElabLite

First off, thank you for considering contributing to ElabLite! It's people like you that make ElabLite such a great tool for the scientific community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Coding Guidelines](#coding-guidelines)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be kind and courteous to others.
You can read the full Code of Conduct [here](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/blob/main/CODE_OF_CONDUCT.md).

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues to avoid duplicates. When creating a bug report, include:

- **Clear title and description**
- **Steps to reproduce** the problem
- **Expected behavior** vs actual behavior
- **Screenshots** if applicable
- **Environment details** (OS, Python version, etc.)

Use the bug report template: [New Bug Report](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/issues/new?template=BUG-REPORT.yml)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, include:

- **Clear title and description**
- **Use case** - why would this be useful?
- **Examples** of how it would work
- **Mockups** if applicable

### Contributing Code

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (see commit message guidelines)
6. Push to your branch (`git push origin feature/AmazingFeature`)
7. Open a Pull Request

### Contributing Templates

Share your custom templates with the community:

1. Create templates following the JSON structure
2. Add documentation for your template
3. Submit via Pull Request to `templates/community/`

### Improving Documentation

Documentation improvements are always welcome:

- Fix typos or unclear explanations
- Add examples
- Translate documentation
- Add tutorials or how-tos

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment tool (venv or virtualenv)

### Setup Steps

1. **Clone your fork**:
   ```bash
   git clone https://github.com/YOUR_USERNAME/ElabLite.git
   cd ElabLite
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

### Project Structure

```
ElabLite/
├── app.py                 # Main entry point
├── models/                # Data models
│   ├── forms.py          # Form models
│   ├── technical.py      # Technical definitions
│   └── validator.py      # Validation logic
├── pages/                 # Streamlit pages
│   ├── 1-select_template.py
│   ├── 1-load_template.py
│   ├── 2-metadata_forms.py
│   ├── 3-metadata_preset.py
│   └── 4-metadata_management.py
├── utils/                 # Utility functions
│   ├── manager.py        # File management
│   ├── parser.py         # Template parsers
│   ├── save_manager.py   # Save operations
│   └── stepper.py        # UI components
└── static/                # Static assets
    └── icons/
```

## Coding Guidelines

### Python Style

Follow PEP 8 guidelines:

- Use 4 spaces for indentation
- Maximum line length: 120 characters
- Use descriptive variable names
- Add docstrings to functions and classes

Example:
```python
def generate_filename(row: pd.Series, selected_columns: list) -> str:
    """
    Generates a filename based on selected columns from a DataFrame row.
    
    Args:
        row (pd.Series): A row of data from a DataFrame
        selected_columns (list): Column names to include in filename
        
    Returns:
        str: The generated filename
        
    Example:
        >>> generate_filename(row, ['analysis', 'sample'])
        '20251014_XRF_PROJECT_analysis_sample.txt'
    """
    # Implementation here
```

### Streamlit Best Practices

- Use session state for data persistence
- Cache expensive operations with `@st.cache_data`
- Provide clear user feedback (success, error, warning messages)
- Keep UI responsive - avoid blocking operations

### Type Hints

Use type hints where possible:

```python
from typing import Dict, List, Optional

def parse_metadata(file_path: str) -> Optional[Dict]:
    """Parse metadata from file."""
    pass
```

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(parser): add support for XLSX templates

Added TemplatesReader support for XLSX format including:
- Reading metadata from Excel sheets
- Handling multiple sheets
- Type conversion for numeric fields

Closes #123
```

```
fix(save): prevent data loss on browser refresh

Added auto-save mechanism that triggers every 30 seconds
and before page navigation. Includes recovery dialog
if unsaved changes are detected.

Fixes #456
```

## Pull Request Process

### Before Submitting

1. **Update documentation** if needed
2. **Add tests** if applicable
3. **Test thoroughly** in different scenarios
4. **Check code style** (run linter if available)
5. **Update CHANGELOG** if it exists

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How did you test these changes?

## Screenshots
If applicable, add screenshots

## Checklist
- [ ] My code follows the project's style guidelines
- [ ] I have commented my code where necessary
- [ ] I have updated the documentation
- [ ] My changes generate no new warnings
- [ ] I have tested my changes
```

### Review Process

1. At least one maintainer review required
2. All checks must pass
3. No merge conflicts
4. Documentation updated

### After Merge

1. Delete your branch
2. Pull the latest changes
3. Continue with new features!

## Questions?

Feel free to:
- Open a [Issue](https://github.com/CRC-Centre-Recherche-Conservation/ElabLite/issues)
- Ask in an existing issue
- Contact the maintainers

## Recognition

Contributors will be:
- Listed in the README
- Credited in release notes
- Appreciated by the community! 🎉

---

Thank you for contributing to ElabLite! 💚