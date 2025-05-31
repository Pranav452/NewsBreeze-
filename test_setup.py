#!/usr/bin/env python3
"""
NewsBreeze Setup Test Script
Verifies that all dependencies and components are working correctly
"""

import sys
import importlib
import platform
import subprocess
import os

def test_python_version():
    """Test Python version compatibility"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version < (3, 8):
        print("   ❌ Python 3.8+ required")
        return False
    else:
        print("   ✅ Python version OK")
        return True

def test_dependencies():
    """Test required dependencies"""
    print("\n📦 Testing dependencies...")
    
    required_packages = [
        'flask',
        'flask_cors', 
        'feedparser',
        'requests',
        'transformers',
        'torch',
        'TTS',
        'numpy',
        'pandas',
        'beautifulsoup4'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - NOT FOUND")
            missing_packages.append(package)
    
    return len(missing_packages) == 0, missing_packages

def test_directories():
    """Test required directories"""
    print("\n📁 Testing directories...")
    
    directories = ['templates', 'static', 'static/audio']
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"   ✅ {directory}")
        else:
            try:
                os.makedirs(directory, exist_ok=True)
                print(f"   ✅ {directory} (created)")
            except Exception as e:
                print(f"   ❌ {directory} - {e}")
                return False
    
    return True

def test_files():
    """Test required files"""
    print("\n📄 Testing files...")
    
    required_files = [
        'app.py',
        'config.py', 
        'requirements.txt',
        'templates/index.html',
        'README.md'
    ]
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - NOT FOUND")
            return False
    
    return True

def test_network():
    """Test network connectivity for RSS feeds"""
    print("\n🌐 Testing network connectivity...")
    
    try:
        import requests
        response = requests.get("https://feeds.bbci.co.uk/news/rss.xml", timeout=10)
        if response.status_code == 200:
            print("   ✅ Network connectivity OK")
            return True
        else:
            print(f"   ❌ Network test failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ❌ Network test failed: {e}")
        return False

def test_memory():
    """Test available memory"""
    print("\n💾 Testing system resources...")
    
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_gb = memory.total / (1024**3)
        
        print(f"   Available RAM: {memory_gb:.1f} GB")
        
        if memory_gb >= 4:
            print("   ✅ Sufficient memory for AI models")
            return True
        else:
            print("   ⚠️  Low memory - AI models may load slowly")
            return True  # Not a critical failure
    except ImportError:
        print("   ⚠️  psutil not available, skipping memory check")
        return True

def run_basic_import_test():
    """Test basic imports from the application"""
    print("\n🧪 Testing application imports...")
    
    try:
        from config import config
        print("   ✅ Config import OK")
        
        # Test basic Flask app creation
        from flask import Flask
        test_app = Flask(__name__)
        print("   ✅ Flask app creation OK")
        
        return True
    except Exception as e:
        print(f"   ❌ Import test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎙️  NewsBreeze Setup Test")
    print("=" * 40)
    
    tests = [
        ("Python Version", test_python_version),
        ("Dependencies", test_dependencies),
        ("Directories", test_directories), 
        ("Files", test_files),
        ("Network", test_network),
        ("Memory", test_memory),
        ("Imports", run_basic_import_test)
    ]
    
    all_passed = True
    missing_deps = []
    
    for test_name, test_func in tests:
        try:
            if test_name == "Dependencies":
                result, missing = test_func()
                if not result:
                    missing_deps = missing
                    all_passed = False
            else:
                result = test_func()
                if not result:
                    all_passed = False
        except Exception as e:
            print(f"   ❌ {test_name} test failed: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! NewsBreeze is ready to run.")
        print("\nTo start the application:")
        print("   python run.py")
        print("   or")
        print("   python app.py")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        
        if missing_deps:
            print(f"\nMissing dependencies: {', '.join(missing_deps)}")
            print("Install them with:")
            print("   pip install -r requirements.txt")
    
    print("\n📚 For help, see README.md")
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 