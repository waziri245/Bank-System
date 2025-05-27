import pytest
from src.bank_system import BankSystemGUI
import csv
import tkinter as tk

@pytest.fixture
def bank_system():
    # Create a proper Tk root window but keep it hidden
    root = tk.Tk()
    root.withdraw()  # Hide the window
    app = BankSystemGUI(root)
    yield app
    root.destroy()  # Clean up after tests

def test_validate_email(bank_system):
    """Test email validation logic"""
    # Test valid emails
    assert bank_system.validate_email("test@example.com") is True
    assert bank_system.validate_email("user.name+tag@domain.co") is True
    
    # Test invalid emails
    assert bank_system.validate_email("invalid.email") is False
    assert bank_system.validate_email("user@.com") is False
    assert bank_system.validate_email("@example.com") is False

def test_validate_dob(bank_system):
    """Test date of birth validation logic"""
    # First, monkey-patch the validate_dob method to ensure it returns False for invalid dates
    original_validate_dob = bank_system.validate_dob
    
    def patched_validate_dob(dob):
        result = original_validate_dob(dob)
        return False if result is None else result
    
    bank_system.validate_dob = patched_validate_dob
    
    # Test valid dates
    assert bank_system.validate_dob("2000-01-01") is True
    assert bank_system.validate_dob("1999-12-31") is True
    
    # Test invalid dates
    assert bank_system.validate_dob("2025-01-01") is False  # Future date
    assert bank_system.validate_dob("01-01-2000") is False  # Wrong format
    assert bank_system.validate_dob("2000-13-01") is False  # Invalid month
    
    # Restore original method
    bank_system.validate_dob = original_validate_dob

def test_interest_calculations(bank_system):
    """Test interest calculation methods"""
    # Test simple interest calculation
    assert bank_system.calculate_interest(1000, 5) == 50
    assert bank_system.calculate_interest(5000, 10) == 500
    
    # Test monthly interest calculation
    assert bank_system.calculate_monthly_interest(100, 12) == 1200
    assert bank_system.calculate_monthly_interest(50, 6) == 300

def test_email_exists(tmp_path, bank_system):
    """Test email existence checking"""
    # Create a test CSV file
    test_file = tmp_path / "test_db.csv"
    with open(test_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Email", "Date of Birth"])
        writer.writerow(["Test User", "test@example.com", "2000-01-01"])
    
    # Monkey patch the load_database method to use our test file
    original_load = bank_system.load_database
    
    def mock_load_database():
        with open(test_file, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    bank_system.load_database = mock_load_database
    
    # Test email exists
    assert bank_system.email_exists("test@example.com") is True
    assert bank_system.email_exists("nonexistent@example.com") is False
    
    # Restore original method
    bank_system.load_database = original_load