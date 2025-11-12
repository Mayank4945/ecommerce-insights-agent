"""
Quick Start Script for E-Commerce Insights Agent
Run this to verify installation and setup
"""

import sys
from pathlib import Path
import subprocess

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")

def check_python_version():
    """Check Python version"""
    print("Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.9+")
        return False

def check_dependencies():
    """Check if dependencies are installed"""
    print("\nChecking dependencies...")
    required = [
        ('streamlit', 'streamlit'),
        ('pandas', 'pandas'),
        ('google-generativeai', 'google.generativeai'),
        ('duckdb', 'duckdb'),
        ('plotly', 'plotly'),
        ('python-dotenv', 'dotenv')
    ]
    
    missing = []
    for package_name, import_name in required:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - MISSING")
            missing.append(package_name)
    
    return len(missing) == 0

def check_env_file():
    """Check if .env file exists and has API key"""
    print("\nChecking environment configuration...")
    env_path = Path('.env')
    
    if not env_path.exists():
        print("❌ .env file not found")
        print("   Run: copy .env.example .env")
        return False
    
    print("✅ .env file exists")
    
    # Check for API key
    with open(env_path, 'r') as f:
        content = f.read()
        if 'your_gemini_api_key_here' in content:
            print("⚠️  Gemini API key not configured")
            print("   Edit .env and add your API key")
            return False
    
    print("✅ API key appears to be configured")
    return True

def check_data_directory():
    """Check if data directory exists"""
    print("\nChecking data directory...")
    data_dir = Path('data')
    
    if not data_dir.exists():
        print("❌ data/ directory not found")
        print("   Creating data/ directory...")
        data_dir.mkdir()
        print("✅ Created data/ directory")
    else:
        print("✅ data/ directory exists")
    
    # Check for CSV files
    csv_files = list(data_dir.glob('*.csv'))
    if csv_files:
        print(f"✅ Found {len(csv_files)} CSV files")
        for csv in csv_files[:5]:  # Show first 5
            print(f"   - {csv.name}")
    else:
        print("⚠️  No CSV files found in data/")
        print("   Download from: https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce/")
    
    return True

def check_project_structure():
    """Check if all required directories exist"""
    print("\nChecking project structure...")
    
    required_dirs = [
        'src',
        'src/agents',
        'src/database',
        'src/memory',
        'src/utils',
        'data',
        'logs',
        'examples',
        'tests'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if Path(dir_path).exists():
            print(f"✅ {dir_path}/")
        else:
            print(f"❌ {dir_path}/ - MISSING")
            all_exist = False
    
    return all_exist

def test_imports():
    """Test importing main modules"""
    print("\nTesting module imports...")
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        
        from src.config import config
        print("✅ src.config")
        
        from src.database import DatabaseManager
        print("✅ src.database")
        
        from src.memory import MemoryManager
        print("✅ src.memory")
        
        from src.agents import AgentSystem
        print("✅ src.agents")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def run_quick_test():
    """Run a quick functionality test"""
    print("\nRunning quick functionality test...")
    
    try:
        sys.path.insert(0, str(Path.cwd()))
        
        from src.database import DatabaseManager
        from src.memory import MemoryManager
        
        # Test database
        db = DatabaseManager()
        print("✅ Database manager initialized")
        
        # Test memory
        memory = MemoryManager()
        memory.add_message('user', 'Test message')
        assert len(memory.messages) == 1
        print("✅ Memory manager working")
        
        # Cleanup
        db.close()
        print("✅ Quick test passed")
        
        return True
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def main():
    """Main setup verification"""
    print_header("E-Commerce Insights Agent - Setup Verification")
    
    print("This script will verify your installation and setup.\n")
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Data Directory", check_data_directory),
        ("Project Structure", check_project_structure),
        ("Module Imports", test_imports),
        ("Functionality", run_quick_test),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
            results.append((name, False))
    
    # Summary
    print_header("Summary")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nPassed: {passed}/{total}")
    
    if passed == total:
        print("\n🎉 All checks passed! You're ready to go!")
        print("\nNext steps:")
        print("1. Ensure CSV files are in data/ directory")
        print("2. Run: streamlit run app.py")
        print("3. Load data in the sidebar")
        print("4. Start asking questions!")
    else:
        print("\n⚠️  Some checks failed. Please fix the issues above.")
        print("\nCommon fixes:")
        print("- Install dependencies: pip install -r requirements.txt")
        print("- Create .env file: copy .env.example .env")
        print("- Add API key to .env file")
        print("- Download dataset to data/ directory")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
