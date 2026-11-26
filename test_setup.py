"""
Quick Setup & Testing Script for Lead Research Agent
Run this to verify everything is configured correctly.
"""

import sys
import os
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test all critical imports."""
    print("🧪 Testing imports...")
    
    try:
        import streamlit
        print("  ✓ Streamlit")
    except ImportError as e:
        print(f"  ✗ Streamlit: {e}")
        return False
    
    try:
        import google.generativeai
        print("  ✓ Google Generative AI")
    except ImportError:
        print("  ⚠ Google Generative AI (optional)")
    
    try:
        from tavily import TavilyClient
        print("  ✓ Tavily")
    except ImportError as e:
        print(f"  ✗ Tavily: {e}")
        return False
    
    try:
        import sqlalchemy
        print("  ✓ SQLAlchemy")
    except ImportError as e:
        print(f"  ✗ SQLAlchemy: {e}")
        return False
    
    try:
        import dotenv
        print("  ✓ Python Dotenv")
    except ImportError as e:
        print(f"  ✗ Python Dotenv: {e}")
        return False
    
    return True


def test_environment():
    """Test environment configuration."""
    print("\n🔧 Testing environment configuration...")
    
    from config.settings import settings
    
    # Check database path
    db_path = Path(settings.DATABASE_PATH)
    if db_path.parent.exists():
        print(f"  ✓ Database directory: {db_path.parent}")
    else:
        print(f"  ⚠ Database directory will be created: {db_path.parent}")
    
    # Check API keys
    if settings.TAVILY_API_KEY and settings.TAVILY_API_KEY != "your_tavily_api_key":
        print("  ✓ Tavily API Key configured")
    else:
        print("  ✗ Tavily API Key NOT configured (required)")
        return False
    
    if settings.GOOGLE_PROJECT_ID and settings.GOOGLE_PROJECT_ID != "your_project_id":
        print("  ✓ Google Project ID configured")
    else:
        print("  ⚠ Google Project ID not configured")
    
    if settings.GEMINI_TEMPERATURE:
        print(f"  ✓ Gemini temperature: {settings.GEMINI_TEMPERATURE}")
    
    return True


def test_database():
    """Test database setup."""
    print("\n💾 Testing database...")
    
    try:
        from database.db import db
        
        # Initialize database
        db._ensure_db_exists()
        print("  ✓ Database initialized successfully")
        
        # Test connection
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            
            if tables:
                print(f"  ✓ Database tables created: {len(tables)} tables")
                return True
            else:
                print("  ⚠ No tables found in database")
                return False
    
    except Exception as e:
        print(f"  ✗ Database error: {e}")
        return False


def test_agents():
    """Test agent initialization."""
    print("\n🤖 Testing agents...")
    
    try:
        from agents.curator_agent import CuratorAgent
        from agents.editor_agent import EditorAgent
        
        curator = CuratorAgent()
        print("  ✓ Curator Agent initialized")
        
        editor = EditorAgent()
        print("  ✓ Editor Agent initialized")
        
        return True
    
    except Exception as e:
        print(f"  ✗ Agent initialization error: {e}")
        return False


def test_utils():
    """Test utility modules."""
    print("\n🔧 Testing utilities...")
    
    try:
        from utils.validators import validate_company_name, validate_website
        
        # Test company name validation
        is_valid, msg = validate_company_name("Test Company")
        if is_valid:
            print("  ✓ Company name validation")
        else:
            print(f"  ✗ Company name validation: {msg}")
            return False
        
        # Test website validation
        is_valid, msg = validate_website("https://example.com")
        if is_valid:
            print("  ✓ Website validation")
        else:
            print(f"  ✗ Website validation: {msg}")
            return False
        
        return True
    
    except Exception as e:
        print(f"  ✗ Utility test error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*50)
    print("  Lead Research Agent - Setup Verification")
    print("="*50 + "\n")
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_environment),
        ("Database", test_database),
        ("Agents", test_agents),
        ("Utilities", test_utils),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"  ✗ {name} test failed: {e}")
            results.append((name, False))
    
    # Summary
    print("\n" + "="*50)
    print("  Test Summary")
    print("="*50)
    
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status}: {name}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ All tests passed! Ready to run the application.")
        print("\nRun with: streamlit run streamlit_app/main.py")
    else:
        print("❌ Some tests failed. Please check the configuration.")
        print("\nCommon issues:")
        print("1. Missing .env file - copy .env.example to .env")
        print("2. Missing API keys - add them to .env")
        print("3. Missing dependencies - run: pip install -r requirements.txt")
    print("="*50 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
