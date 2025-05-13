import sys
import subprocess
import os

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'pandas': '2.2.1',
        'numpy': '1.26.4',
        'matplotlib': '3.8.3',
        'seaborn': '0.13.2',
        'openpyxl': '3.1.2'
    }
    
    # Get the Python executable path
    python_path = sys.executable
    
    for package, version in required_packages.items():
        try:
            # Try to import the package
            __import__(package)
        except ImportError:
            print(f"Installing {package}...")
            try:
                # Use the full Python path to run pip
                subprocess.check_call([
                    python_path,
                    "-m",
                    "pip",
                    "install",
                    f"{package}=={version}"
                ])
                print(f"Successfully installed {package}")
            except subprocess.CalledProcessError as e:
                print(f"Error installing {package}: {str(e)}")
                print("Please try installing the package manually using:")
                print(f"{python_path} -m pip install {package}=={version}")
                sys.exit(1) 