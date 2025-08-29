# GitLab Configuration

This directory contains GitLab-specific configuration files for the Bike Chatbot project.

## Structure

```
.gitlab/
├── README.md                    # This file
├── issue_templates/             # Issue templates
│   ├── bug_report.md           # Template for bug reports
│   └── feature_request.md      # Template for feature requests
└── merge_request_templates/     # Merge request templates
    └── default.md              # Default merge request template
```

## CI/CD Pipeline

The `.gitlab-ci.yml` file in the root directory defines the CI/CD pipeline with the following stages:

### Stages

1. **Test** - Runs unit tests and generates coverage reports
2. **Lint** - Checks code formatting and style with Black, Flake8, and MyPy
3. **Build** - Verifies all modules can be imported successfully
4. **Deploy** - Deploys to staging (automatic) and production (manual)

### Environments

- **Staging**: Automatically deployed from `develop` branch
- **Production**: Manually deployed from `main` branch

### Cache

The pipeline caches:
- Python virtual environment (`.venv/`)
- Pip cache (`.pip-cache/`)

## Issue Templates

### Bug Report Template
Use this template when reporting bugs. Includes sections for:
- Description and reproduction steps
- Expected vs actual behavior
- Environment details
- Additional context

### Feature Request Template
Use this template when requesting new features. Includes sections for:
- Problem statement and proposed solution
- User stories and acceptance criteria
- Technical considerations

## Merge Request Template

The default merge request template includes:
- Change type classification
- Testing checklist
- Code review checklist
- Environment information

## Usage

When creating issues or merge requests in GitLab, these templates will be automatically available in the dropdown menu.
