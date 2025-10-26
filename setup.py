#!/usr/bin/env python3
"""
Automated setup script for IT Support Chatbot
Checks dependencies, creates environment, and initializes the system
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*70)
    print(f"  {text}")
    print("="*70 + "\n")

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def check_env_file():
    """Check if .env file exists"""
    print("\nChecking environment configuration...")
    if os.path.exists('.env'):
        print("✓ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("   Please create .env file with your Azure OpenAI credentials")
        print("   You can copy .env.example and update it with your values:")
        print("   cp .env.example .env")
        return False

def install_dependencies():
    """Install required packages"""
    print("\nInstalling dependencies...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            check=True,
            capture_output=True
        )
        print("✓ All dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed to install dependencies")
        print(f"   Error: {e}")
        return False

def generate_mock_data():
    """Generate mock knowledge base data"""
    print("\nGenerating mock data...")
    if os.path.exists('it_knowledge_base.json'):
        print("⚠️  Knowledge base already exists")
        response = input("   Regenerate? (y/n): ")
        if response.lower() != 'y':
            print("✓ Using existing knowledge base")
            return True
    
    try:
        subprocess.run([sys.executable, "generate_mock_data.py"], check=True)
        print("✓ Mock data generated successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to generate mock data")
        return False

def build_vector_store():
    """Build FAISS vector store"""
    print("\nBuilding vector store...")
    
    if not os.path.exists('.env'):
        print("⚠️  Skipping vector store build - .env file required")
        print("   Run this script again after creating .env file")
        return False
    
    if os.path.exists('faiss_index'):
        print("⚠️  Vector store already exists")
        response = input("   Rebuild? (y/n): ")
        if response.lower() != 'y':
            print("✓ Using existing vector store")
            return True
    
    try:
        subprocess.run([sys.executable, "build_vector_store.py"], check=True)
        print("✓ Vector store built successfully")
        return True
    except subprocess.CalledProcessError as e:
        print("❌ Failed to build vector store")
        print(f"   Error: {e}")
        print("   Make sure your Azure OpenAI credentials in .env are correct")
        return False

def verify_files():
    """Verify all required files exist"""
    print("\nVerifying project files...")
    required_files = [
        'app.py',
        'chatbot.py',
        'function_calling.py',
        'build_vector_store.py',
        'generate_mock_data.py',
        'requirements.txt',
        '.env.example'
    ]
    
    all_exist = True
    for file in required_files:
        if os.path.exists(file):
            print(f"✓ {file}")
        else:
            print(f"❌ {file} - MISSING")
            all_exist = False
    
    return all_exist

def show_next_steps():
    """Display next steps"""
    print_header("Setup Complete!")
    
    print("Next steps:")
    print("\n1. If you haven't already, create .env file:")
    print("   cp .env.example .env")
    print("   Then edit .env with your Azure OpenAI credentials")
    
    print("\n2. If vector store wasn't built, run:")
    print("   python build_vector_store.py")
    
    print("\n3. Launch the chatbot:")
    print("   streamlit run app.py")
    
    print("\n4. Or test in Jupyter notebook:")
    print("   jupyter notebook IT_Support_Chatbot_Demo.ipynb")
    
    print("\n5. Or test via command line:")
    print("   python chatbot.py")
    
    print("\n📚 Read README.md for detailed documentation")
    print("🐛 Check troubleshooting section if you encounter issues")

def main():
    """Main setup function"""
    print_header("IT Support Chatbot - Automated Setup")
    
    # Track setup status
    steps = []
    
    # Step 1: Check Python version
    steps.append(("Python Version", check_python_version()))
    
    # Step 2: Verify files
    steps.append(("Project Files", verify_files()))
    
    # Step 3: Check .env
    steps.append(("Environment Config", check_env_file()))
    
    # Step 4: Install dependencies
    if all(step[1] for step in steps):
        steps.append(("Dependencies", install_dependencies()))
    
    # Step 5: Generate mock data
    if all(step[1] for step in steps):
        steps.append(("Mock Data", generate_mock_data()))
    
    # Step 6: Build vector store (optional if no .env)
    if all(step[1] for step in steps) and os.path.exists('.env'):
        steps.append(("Vector Store", build_vector_store()))
    
    # Summary
    print_header("Setup Summary")
    for step_name, status in steps:
        status_icon = "✓" if status else "❌"
        print(f"{status_icon} {step_name}")
    
    all_success = all(step[1] for step in steps)
    
    if all_success:
        show_next_steps()
    else:
        print("\n⚠️  Setup completed with warnings")
        print("   Review the messages above and resolve any issues")
        print("   You can run this script again after fixing issues")

if __name__ == "__main__":
    main()
