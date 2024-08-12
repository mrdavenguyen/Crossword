# Contributing Guidelines

## Coding Style
- Follow PEP 8 for Python code.
- Use 4 spaces for indentation.
- Limit lines to 79 characters.
- Variables: Use lower_case_with_underscores (e.g., user_name).
- Functions: Use lower_case_with_underscores (e.g., calculate_total).
- Classes: Use CapitalizedWords (e.g., CustomerOrder).
- Constants: Use UPPER_CASE_WITH_UNDERSCORES (e.g., MAX_RETRIES).
- Modules and Packages: Use lower_case_with_underscores (e.g., data_utils).
- File Names: Use lower_case_with_underscores for consistency with modules (e.g., data_processor.py).
- Mark Down File Names: Use uppercase no underscore for consistency with md files (e.g., CHANGELOG.md).
- Docstrings: Use triple quotes for docstrings and follow the convention for documentation.
- Imports: Keep imports at the top of the file and follow the import order: standard library imports, related third-party imports, and then local application imports.

## Commit Messages
- Use the present tense ("Add feature" not "Added feature").
- Capitalize the subject line.
- Limit the subject line to 50 characters.
- Use the imperative mood in the subject line (Add, Fix, Remove, Improve, Refactor, Introduce, Document, Resolve, Optimize).

## Pull Requests
- Ensure all tests pass before submitting a pull request.
- Include a clear description of the change.
- Reference relevant issue numbers.
