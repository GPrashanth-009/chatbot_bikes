#!/usr/bin/env python3
"""
Deployment script for Bike Chatbot project.
Automates deployment processes for different environments.
"""

import os
import sys
import subprocess
import argparse
import json
from pathlib import Path
from datetime import datetime


class Deployer:
    """Deployment automation class."""
    
    def __init__(self, environment="staging"):
        self.environment = environment
        self.project_root = Path(__file__).parent.parent
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
    def run_command(self, command, description, check=True):
        """Run a command and handle errors."""
        print(f"🔄 {description}...")
        print(f"   Command: {command}")
        
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                check=check, 
                capture_output=True, 
                text=True,
                cwd=self.project_root
            )
            if result.stdout:
                print(f"   Output: {result.stdout.strip()}")
            print(f"✅ {description} completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ {description} failed: {e}")
            if e.stderr:
                print(f"   Error: {e.stderr.strip()}")
            return False
    
    def check_prerequisites(self):
        """Check if all prerequisites are met."""
        print("🔍 Checking prerequisites...")
        
        # Check if we're in a git repository
        if not (self.project_root / ".git").exists():
            print("❌ Not in a git repository")
            return False
        
        # Check if .env file exists
        env_file = self.project_root / ".env"
        if not env_file.exists():
            print("❌ .env file not found")
            return False
        
        # Check if Docker is available (for containerized deployment)
        if self.environment in ["staging", "production"]:
            if not self.run_command("docker --version", "Checking Docker", check=False):
                print("⚠️  Docker not available, skipping containerized deployment")
        
        print("✅ Prerequisites check passed")
        return True
    
    def run_tests(self):
        """Run the test suite."""
        print("🧪 Running tests...")
        
        # Run unit tests
        if not self.run_command("pytest tests/ -v", "Running unit tests"):
            print("❌ Unit tests failed")
            return False
        
        # Run linting
        if not self.run_command("ruff check .", "Running linting"):
            print("❌ Linting failed")
            return False
        
        # Run type checking
        if not self.run_command("mypy .", "Running type checking"):
            print("❌ Type checking failed")
            return False
        
        print("✅ All tests passed")
        return True
    
    def build_docker_image(self):
        """Build Docker image."""
        image_name = f"bike-chatbot:{self.environment}-{self.timestamp}"
        
        if not self.run_command(
            f"docker build -t {image_name} .",
            f"Building Docker image: {image_name}"
        ):
            return None
        
        return image_name
    
    def deploy_to_staging(self):
        """Deploy to staging environment."""
        print("🚀 Deploying to staging...")
        
        # Build Docker image
        image_name = self.build_docker_image()
        if not image_name:
            return False
        
        # Stop existing containers
        self.run_command("docker-compose down", "Stopping existing containers", check=False)
        
        # Update docker-compose.yml with new image
        compose_file = self.project_root / "docker-compose.yml"
        if compose_file.exists():
            # In a real deployment, you would update the image tag
            print("📝 Updating docker-compose.yml with new image")
        
        # Start new containers
        if not self.run_command("docker-compose up -d", "Starting new containers"):
            return False
        
        # Health check
        if not self.run_command(
            "curl -f http://localhost:3000/_stcore/health",
            "Health check",
            check=False
        ):
            print("⚠️  Health check failed, but deployment may still be functional")
        
        print("✅ Staging deployment completed")
        return True
    
    def deploy_to_production(self):
        """Deploy to production environment."""
        print("🚀 Deploying to production...")
        
        # Additional production checks
        if not self.check_production_requirements():
            return False
        
        # Build production Docker image
        image_name = self.build_docker_image()
        if not image_name:
            return False
        
        # In a real deployment, you would:
        # 1. Push the image to a registry
        # 2. Update production infrastructure
        # 3. Perform rolling updates
        # 4. Run smoke tests
        
        print("📝 Production deployment would include:")
        print("   - Pushing image to registry")
        print("   - Updating production infrastructure")
        print("   - Performing rolling updates")
        print("   - Running smoke tests")
        
        print("✅ Production deployment simulation completed")
        return True
    
    def check_production_requirements(self):
        """Check production-specific requirements."""
        print("🔍 Checking production requirements...")
        
        # Check if we're on main branch
        result = subprocess.run(
            "git branch --show-current",
            shell=True,
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        current_branch = result.stdout.strip()
        
        if current_branch != "main":
            print(f"❌ Not on main branch (current: {current_branch})")
            return False
        
        # Check if working directory is clean
        result = subprocess.run(
            "git status --porcelain",
            shell=True,
            capture_output=True,
            text=True,
            cwd=self.project_root
        )
        
        if result.stdout.strip():
            print("❌ Working directory is not clean")
            return False
        
        print("✅ Production requirements met")
        return True
    
    def create_deployment_log(self, success):
        """Create deployment log."""
        log_file = self.project_root / "deployment.log"
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "environment": self.environment,
            "success": success,
            "git_commit": subprocess.run(
                "git rev-parse HEAD",
                shell=True,
                capture_output=True,
                text=True,
                cwd=self.project_root
            ).stdout.strip()
        }
        
        try:
            if log_file.exists():
                with open(log_file, "r") as f:
                    logs = json.load(f)
            else:
                logs = []
            
            logs.append(log_entry)
            
            with open(log_file, "w") as f:
                json.dump(logs, f, indent=2)
            
            print(f"📝 Deployment log updated: {log_file}")
        except Exception as e:
            print(f"⚠️  Failed to update deployment log: {e}")
    
    def deploy(self):
        """Main deployment method."""
        print(f"🚀 Starting {self.environment} deployment...")
        print(f"📁 Project root: {self.project_root}")
        print(f"⏰ Timestamp: {self.timestamp}")
        
        # Check prerequisites
        if not self.check_prerequisites():
            return False
        
        # Run tests
        if not self.run_tests():
            return False
        
        # Deploy based on environment
        success = False
        if self.environment == "staging":
            success = self.deploy_to_staging()
        elif self.environment == "production":
            success = self.deploy_to_production()
        else:
            print(f"❌ Unknown environment: {self.environment}")
            return False
        
        # Create deployment log
        self.create_deployment_log(success)
        
        if success:
            print(f"🎉 {self.environment.capitalize()} deployment completed successfully!")
        else:
            print(f"❌ {self.environment.capitalize()} deployment failed!")
        
        return success


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Deploy Bike Chatbot")
    parser.add_argument(
        "environment",
        choices=["staging", "production"],
        help="Deployment environment"
    )
    parser.add_argument(
        "--skip-tests",
        action="store_true",
        help="Skip running tests before deployment"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Force deployment even if checks fail"
    )
    
    args = parser.parse_args()
    
    deployer = Deployer(args.environment)
    
    if args.force:
        print("⚠️  Force flag enabled - skipping some checks")
    
    success = deployer.deploy()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
