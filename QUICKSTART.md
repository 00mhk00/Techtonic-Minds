# Quick Start Guide - Airline Data Warehouse

## Prerequisites

- Python 3.8 or higher
- PostgreSQL or MySQL database (optional for full ETL)
- pip (Python package manager)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
cd airline-data-warehouse
pip install -r requirements.txt
```

### 2. Generate Dummy Data

Generate sample data with default settings (10,000 flights, 5,000 passengers):

```bash
cd scripts
python generate_data.py
```

Generate with custom parameters:

```bash
python generate_data.py --flights 20000 --passengers 10000 --start-date 2024-01-01 --end-date 2024-12-31
```

This will create CSV files in the `data/` directory:
- Dimension tables: dim_date, dim_time, dim_airport, etc.
- Fact tables: fact_flight, fact_booking, fact_passenger_journey

### 3. Set Up Database (Optional)

If you want to load data into a database:

#### PostgreSQL:
```sql
CREATE DATABASE airline_dw;
CREATE USER airline_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE airline_dw TO airline_user;
```

#### Run DDL Scripts:
```bash
psql -U airline_user -d airline_dw -f sql/schema/create_dimensions.sql
psql -U airline_user -d airline_dw -f sql/schema/create_facts.sql
```

### 4. Load Data into Database

```bash
cd scripts
python etl_pipeline.py --db-url postgresql://airline_user:your_password@localhost:5432/airline_dw --run-analytics
```

### 5. Run Sample Queries

```bash
psql -U airline_user -d airline_dw -f sql/queries/analytics.sql
```

## Working with CSV Files Only

If you don't want to set up a database, you can still work with the generated CSV files using pandas:

```python
import pandas as pd

# Load data
flights = pd.read_csv('data/fact_flight.csv')
bookings = pd.read_csv('data/fact_booking.csv')
airports = pd.read_csv('data/dim_airport.csv')

# Example analysis
print("Total flights:", len(flights))
print("On-time percentage:", 
      (flights['flight_status'] == 'On-Time').sum() / len(flights) * 100)
```

## Command Reference

### Data Generation Options

```bash
python generate_data.py --help

Options:
  --flights FLIGHTS         Number of flights to generate (default: 10000)
  --passengers PASSENGERS   Number of unique passengers (default: 5000)
  --start-date START_DATE  Start date YYYY-MM-DD (default: 2023-01-01)
  --end-date END_DATE      End date YYYY-MM-DD (default: 2024-12-31)
  --output-dir OUTPUT_DIR  Output directory (default: ../data)
```

### ETL Pipeline Options

```bash
python etl_pipeline.py --help

Options:
  --db-url DB_URL         Database connection URL
  --data-dir DATA_DIR     Directory with CSV files (default: ../data)
  --skip-verify          Skip data verification
  --run-analytics        Run sample analytics queries
```

## Data Warehouse Schema

### Dimension Tables
- **dim_date**: Date information (730+ rows for 2 years)
- **dim_time**: Time intervals (96 rows, 15-min intervals)
- **dim_airport**: 45+ major world airports
- **dim_aircraft**: 19 different aircraft types
- **dim_airline**: 27 major airlines
- **dim_customer**: Customer/passenger profiles
- **dim_route**: Flight routes between airports

### Fact Tables
- **fact_flight**: Flight operations and performance
- **fact_booking**: Ticket bookings and revenue
- **fact_passenger_journey**: Individual passenger experiences

## Sample Use Cases

### 1. On-Time Performance Dashboard
```sql
SELECT airline_name, 
       COUNT(*) as flights,
       AVG(departure_delay_minutes) as avg_delay
FROM fact_flight f
JOIN dim_airline a ON f.airline_id = a.airline_id
GROUP BY airline_name;
```

### 2. Revenue Analysis
```sql
SELECT SUM(total_amount) as revenue,
       COUNT(*) as bookings
FROM fact_booking
WHERE booking_status = 'Completed';
```

### 3. Route Profitability
```sql
SELECT r.route_code,
       SUM(b.total_amount) as revenue,
       COUNT(*) as bookings
FROM fact_booking b
JOIN fact_flight f ON b.flight_id = f.flight_id
JOIN dim_route r ON f.route_id = r.route_id
GROUP BY r.route_code
ORDER BY revenue DESC
LIMIT 10;
```

## Troubleshooting

### Issue: Module not found
**Solution**: Install requirements: `pip install -r requirements.txt`

### Issue: Database connection failed
**Solution**: Check your database URL and credentials

### Issue: Out of memory during data generation
**Solution**: Reduce the number of flights: `python generate_data.py --flights 5000`

### Issue: CSV files are empty
**Solution**: Make sure you run generate_data.py from the scripts/ directory

## Next Steps

1. **Explore the data**: Open CSV files in Excel or pandas
2. **Create visualizations**: Use Tableau, Power BI, or matplotlib
3. **Add more dimensions**: Extend the schema for your needs
4. **Implement real-time loading**: Modify ETL for incremental loads
5. **Add data quality checks**: Implement validation rules

## Support

For issues or questions, refer to the main README.md file.
