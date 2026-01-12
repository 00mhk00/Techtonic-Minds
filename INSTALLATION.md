# Installation and Testing Script for Airline Data Warehouse

## Quick Test (Without Installing Dependencies)

If you want to quickly test the project structure without installing dependencies, 
you can use this simple test script.

### Test Data Generation (Simplified)

Create a file called `test_data_gen.py` in the scripts folder:

```python
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

# Simple test data generation
def create_test_data():
    data_dir = Path('../data')
    data_dir.mkdir(exist_ok=True)
    
    # Create a simple dim_airport.csv
    with open(data_dir / 'dim_airport.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['airport_id', 'iata_code', 'airport_name', 'city', 'country'])
        writer.writerow([1, 'JFK', 'John F. Kennedy International', 'New York', 'USA'])
        writer.writerow([2, 'LAX', 'Los Angeles International', 'Los Angeles', 'USA'])
        writer.writerow([3, 'ORD', 'O\'Hare International', 'Chicago', 'USA'])
    
    print("✓ Test data created successfully!")
    print(f"  Location: {data_dir.absolute()}")

if __name__ == '__main__':
    create_test_data()
```

## Full Installation (With All Dependencies)

### Windows

```powershell
# Navigate to project directory
cd airline-data-warehouse

# Create virtual environment (recommended)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Install dependencies
pip install pandas numpy faker python-dateutil psycopg2-binary sqlalchemy

# Generate data
cd scripts
python generate_data.py --flights 1000 --passengers 500
```

### Linux/Mac

```bash
# Navigate to project directory
cd airline-data-warehouse

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install pandas numpy faker python-dateutil psycopg2-binary sqlalchemy

# Generate data
cd scripts
python generate_data.py --flights 1000 --passengers 500
```

## Verify Installation

```python
# test_installation.py
try:
    import pandas as pd
    print("✓ pandas installed")
except ImportError:
    print("✗ pandas not installed")

try:
    import numpy as np
    print("✓ numpy installed")
except ImportError:
    print("✗ numpy not installed")

try:
    from faker import Faker
    print("✓ faker installed")
except ImportError:
    print("✗ faker not installed")

print("\nAll required packages are installed!")
```

## Alternative: Use Jupyter Notebook

If you prefer working with Jupyter notebooks:

```bash
pip install jupyter matplotlib seaborn
jupyter notebook
```

Then create a new notebook and run:

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load generated data
flights = pd.read_csv('../data/fact_flight.csv')
print(f"Total flights: {len(flights)}")

# Simple visualization
flights['flight_status'].value_counts().plot(kind='bar')
plt.title('Flight Status Distribution')
plt.show()
```

## Docker Option (No Installation Required)

If you have Docker installed, you can run everything in a container:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "scripts/generate_data.py"]
```

Build and run:
```bash
docker build -t airline-dw .
docker run -v $(pwd)/data:/app/data airline-dw
```

## Cloud Options

### Google Colab (Free, No Installation)

1. Go to [colab.research.google.com](https://colab.research.google.com)
2. Upload the scripts
3. Install packages in the first cell:
```python
!pip install faker pandas numpy
```
4. Run your scripts

### Azure Notebooks / AWS SageMaker

Similar process - upload files and install requirements.

## Minimal Requirements

If you only want to VIEW the data (not generate):
- No Python required
- Open CSV files in Excel, Google Sheets, or any spreadsheet software
- Use any SQL database client to run the provided SQL scripts

## Common Installation Issues

### Issue: pip not found
```bash
# Windows
python -m pip install --upgrade pip

# Linux/Mac
sudo apt-get install python3-pip  # Ubuntu/Debian
brew install python  # Mac with Homebrew
```

### Issue: Permission denied
```bash
# Use --user flag
pip install --user -r requirements.txt
```

### Issue: SSL Certificate error
```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```
