# Bike Chatbot Documentation

This directory contains comprehensive documentation for the Bike Chatbot project.

## 📚 Documentation Structure

```
docs/
├── README.md              # This file - documentation overview
├── api/                   # API documentation
│   ├── bikes.md          # Bike catalog API reference
│   ├── intents.md        # Intent parsing API reference
│   └── llm.md            # LLM integration API reference
├── deployment/            # Deployment guides
│   ├── docker.md         # Docker deployment guide
│   ├── gitlab-ci.md      # GitLab CI/CD guide
│   └── production.md     # Production deployment guide
├── development/           # Development guides
│   ├── setup.md          # Development environment setup
│   ├── testing.md        # Testing guide
│   └── contributing.md   # Contribution guidelines
└── user/                  # User documentation
    ├── cli.md            # CLI usage guide
    ├── web-app.md        # Web application guide
    └── troubleshooting.md # Troubleshooting guide
```

## 🚀 Quick Start

1. **For Users**: See [user/web-app.md](user/web-app.md) for web application usage
2. **For Developers**: See [development/setup.md](development/setup.md) for setup instructions
3. **For Contributors**: See [development/contributing.md](development/contributing.md) for contribution guidelines

## 📖 Documentation Sections

### User Documentation
- **[CLI Guide](user/cli.md)**: How to use the command-line interface
- **[Web App Guide](user/web-app.md)**: How to use the Streamlit web application
- **[Troubleshooting](user/troubleshooting.md)**: Common issues and solutions

### Developer Documentation
- **[Setup Guide](development/setup.md)**: Setting up the development environment
- **[Testing Guide](development/testing.md)**: Running tests and writing new tests
- **[Contributing Guide](development/contributing.md)**: How to contribute to the project

### API Documentation
- **[Bikes API](api/bikes.md)**: Bike catalog and recommendation functions
- **[Intents API](api/intents.md)**: User preference parsing functions
- **[LLM API](api/llm.md)**: OpenAI integration functions

### Deployment Documentation
- **[Docker Guide](deployment/docker.md)**: Containerized deployment
- **[GitLab CI/CD](deployment/gitlab-ci.md)**: Continuous integration and deployment
- **[Production Guide](deployment/production.md)**: Production deployment best practices

## 🔧 Building Documentation

To build and serve the documentation locally:

```bash
# Install documentation dependencies
pip install -r requirements.txt

# Serve documentation
python -m http.server 8000
```

Then visit `http://localhost:8000/docs/` to view the documentation.

## 📝 Contributing to Documentation

When contributing to the project, please also update the relevant documentation:

1. **Code Changes**: Update API documentation in `docs/api/`
2. **New Features**: Update user guides in `docs/user/`
3. **Setup Changes**: Update development guides in `docs/development/`
4. **Deployment Changes**: Update deployment guides in `docs/deployment/`

## 📋 Documentation Standards

- Use clear, concise language
- Include code examples where appropriate
- Keep documentation up-to-date with code changes
- Use consistent formatting and structure
- Include troubleshooting sections for complex topics

## 🔗 Related Links

- [Main README](../README.md) - Project overview
- [CONTRIBUTING.md](../CONTRIBUTING.md) - Contribution guidelines
- [CHANGELOG.md](../CHANGELOG.md) - Project changelog
- [LICENSE](../LICENSE) - Project license
