# Airline Data Warehouse Project

## Overview
This project simulates a complete data warehouse for an airline industry, including dimension and fact tables, ETL pipelines, and sample analytics queries.

## Project Structure
```
airline-data-warehouse/
├── data/                    # Generated dummy data (CSV files)
├── sql/                     # SQL DDL and query scripts
│   ├── schema/             # Table creation scripts
│   └── queries/            # Sample analytical queries
├── scripts/                # Python scripts for data generation and ETL
│   ├── generate_data.py    # Generate dummy airline data
│   ├── etl_pipeline.py     # ETL process
│   └── utils.py            # Utility functions
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

## Data Warehouse Schema

### Star Schema Design

#### Dimension Tables:
1. **dim_airport** - Airport information (IATA code, name, city, country, timezone)
2. **dim_aircraft** - Aircraft details (model, manufacturer, capacity, range)
3. **dim_airline** - Airline information (code, name, country, alliance)
4. **dim_customer** - Customer/passenger details (demographics, loyalty status)
5. **dim_date** - Date dimension (date, day, month, quarter, year, etc.)
6. **dim_time** - Time dimension (hour, minute, period of day)
7. **dim_route** - Flight routes (origin, destination, distance)

#### Fact Tables:
1. **fact_flight** - Flight operations (delays, cancellations, on-time performance)
2. **fact_booking** - Ticket bookings and revenue
3. **fact_passenger_journey** - Individual passenger trips

## Features

- **Realistic Data Generation**: Creates dummy data that mimics real airline operations
- **Complete Star Schema**: Dimension and fact tables optimized for analytics
- **ETL Pipeline**: Python-based ETL process to load data
- **Sample Queries**: Pre-built analytical queries for common use cases
- **Scalable**: Generate any volume of data for testing

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Usage

### 1. Generate Dummy Data
```bash
python scripts/generate_data.py --flights 10000 --passengers 5000
```

### 2. Create Database Schema
```sql
-- In your database client, run:
source sql/schema/create_dimensions.sql
source sql/schema/create_facts.sql
```

### 3. Run ETL Pipeline
```bash
python scripts/etl_pipeline.py
```

### 4. Execute Sample Queries
```sql
source sql/queries/analytics.sql
```

## Sample Analytics Use Cases

1. **On-Time Performance Analysis**: Track flight delays by airline, route, and time period
2. **Revenue Analytics**: Analyze booking revenue by customer segment, route, and season
3. **Capacity Utilization**: Monitor seat occupancy and load factors
4. **Customer Behavior**: Analyze booking patterns, loyalty program effectiveness
5. **Operational Metrics**: Flight cancellations, turnaround times, aircraft utilization

## Technologies Used

- **Python 3.8+**: Data generation and ETL
- **Pandas**: Data manipulation
- **Faker**: Realistic dummy data generation
- **SQL**: Data warehouse schema (PostgreSQL/MySQL compatible)

## Data Volume

Default data generation creates:
- 100+ Airports worldwide
- 50+ Aircraft types
- 25+ Airlines
- 10,000 Flights
- 5,000 Unique customers
- 50,000+ Booking records

## License

This is a demonstration project for educational purposes.

## Author

Created for Techtonic Minds assessment
