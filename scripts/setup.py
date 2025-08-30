#!/usr/bin/env python3
"""
Setup script for Bike Chatbot project.
Automates the initial setup process for new developers.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True


def create_virtual_environment():
    """Create a virtual environment."""
    venv_path = Path(".venv")
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    return run_command("python -m venv .venv", "Creating virtual environment")


def get_activation_command():
    """Get the appropriate activation command for the current OS."""
    system = platform.system().lower()
    if system == "windows":
        return ".venv\\Scripts\\activate"
    else:
        return "source .venv/bin/activate"


def install_dependencies():
    """Install project dependencies."""
    # Determine the correct pip command
    if platform.system().lower() == "windows":
        pip_cmd = ".venv\\Scripts\\pip"
    else:
        pip_cmd = ".venv/bin/pip"
    
    # Upgrade pip first
    if not run_command(f"{pip_cmd} install --upgrade pip", "Upgrading pip"):
        return False
    
    # Install dependencies
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Installing dependencies"):
        return False
    
    # Install development dependencies
    if not run_command(f"{pip_cmd} install -e .[dev]", "Installing development dependencies"):
        return False
    
    return True


def setup_pre_commit():
    """Set up pre-commit hooks."""
    if not run_command("pre-commit install", "Installing pre-commit hooks"):
        print("⚠️  Pre-commit setup failed, but continuing...")
        return True
    return True


def create_env_file():
    """Create a .env file template."""
    env_file = Path(".env")
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    env_content = """# Bike Chatbot Environment Variables
# Copy this file to .env and fill in your actual values

# OpenAI API Configuration
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_MODEL=gpt-3.5-turbo

# Streamlit Configuration
STREAMLIT_SERVER_PORT=3000
STREAMLIT_SERVER_ADDRESS=localhost

# Development Configuration
DEBUG=True
LOG_LEVEL=INFO
"""
    
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file template")
        return True
    except Exception as e:
        print(f"❌ Failed to create .env file: {e}")
        return False


def run_tests():
    """Run the test suite to verify setup."""
    print("🧪 Running tests to verify setup...")
    if run_command("pytest tests/ -v", "Running test suite"):
        print("✅ All tests passed!")
        return True
    else:
        print("⚠️  Some tests failed, but setup may still be functional")
        return True


def print_next_steps():
    """Print next steps for the user."""
    activation_cmd = get_activation_command()
    
    print("\n" + "="*60)
    print("🎉 Setup completed successfully!")
    print("="*60)
    print("\n📋 Next steps:")
    print(f"1. Activate the virtual environment:")
    print(f"   {activation_cmd}")
    print("\n2. Set up your environment variables:")
    print("   - Copy .env.example to .env")
    print("   - Add your OpenAI API key to .env")
    print("\n3. Run the application:")
    print("   - Web app: streamlit run streamlit_app.py --server.port 3000")
    print("   - CLI: python main.py")
    print("\n4. View documentation:")
    print("   - README.md for project overview")
    print("   - docs/ for detailed documentation")
    print("\n🔧 Development commands:")
    print("   - make help          # Show all available commands")
    print("   - make test          # Run tests")
    print("   - make lint          # Run linting")
    print("   - make format        # Format code")
    print("\n📚 Useful links:")
    print("   - CONTRIBUTING.md    # Contribution guidelines")
    print("   - CHANGELOG.md       # Project changelog")
    print("   - LICENSE            # Project license")
    print("="*60)


def main():
    """Main setup function."""
    print("🚀 Bike Chatbot Setup Script")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create virtual environment
    if not create_virtual_environment():
        print("❌ Failed to create virtual environment")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Set up pre-commit hooks
    setup_pre_commit()
    
    # Create .env file
    create_env_file()
    
    # Run tests
    run_tests()
    
    # Print next steps
    print_next_steps()


if __name__ == "__main__":
    main()
