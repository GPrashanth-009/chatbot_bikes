# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Enhanced Streamlit UI with chat avatars and quick suggestion buttons
- Preference badges and richer recommendation cards
- Shortlist functionality in sidebar
- Docker Compose configuration for containerized deployment
- Modern Python packaging with pyproject.toml
- UV dependency locking for reproducible builds
- GitLab CI/CD pipeline with testing and deployment stages
- Comprehensive VS Code configuration
- Issue and merge request templates

### Changed
- Improved chat interface with better visual design
- Enhanced recommendation scoring algorithm
- Updated project structure for better maintainability

### Fixed
- Budget parsing for values over 10k
- Preference merging logic
- Streamlit port configuration

## [0.1.0] - 2024-01-XX

### Added
- Initial release of Bike Chatbot
- Core bike catalog with 7 different bike models
- OpenAI integration for natural language processing
- Intent parsing for user preferences (budget, category, terrain, brand, motorized, lightweight)
- Bike recommendation engine with scoring algorithm
- CLI interface for command-line usage
- Streamlit web application with interactive chat interface
- Support for multiple bike categories: road, mountain, hybrid, gravel, city, e-bike
- Price filtering and budget-aware recommendations
- Terrain-based matching (paved, gravel, trail, urban)
- Brand preference support
- Electric bike detection and filtering
- Lightweight preference scoring

### Features
- **Bike Catalog**: In-memory catalog with detailed bike specifications
- **Smart Recommendations**: AI-powered bike suggestions based on user preferences
- **Natural Language Processing**: Understands user intent from free text
- **Interactive Web UI**: Modern Streamlit interface with chat-like experience
- **CLI Version**: Command-line interface for scripting and automation
- **Preference Learning**: Remembers and builds upon user preferences during conversation

### Technical Details
- **Python 3.9+** compatibility
- **OpenAI API** integration for conversational AI
- **Streamlit** for web interface
- **Type hints** throughout codebase
- **Modular architecture** for easy extension
- **Comprehensive documentation**

---

## Version History

- **0.1.0**: Initial release with core functionality
- **Unreleased**: Enhanced UI, Docker support, and development tools

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the AGPLv3 License - see the [LICENSE](LICENSE) file for details.
