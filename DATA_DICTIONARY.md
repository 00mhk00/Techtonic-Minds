# Data Dictionary - Airline Data Warehouse

## Overview
This document describes all tables, columns, data types, and relationships in the airline data warehouse.

---

## Dimension Tables

### dim_date
Date dimension for calendar-based analysis.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| date_id | INT | Primary key | 1 |
| full_date | DATE | Full date value | 2024-01-15 |
| day_of_week | INT | ISO day of week (1=Monday, 7=Sunday) | 1 |
| day_name | VARCHAR(10) | Name of the day | Monday |
| day_of_month | INT | Day number in month | 15 |
| day_of_year | INT | Day number in year | 15 |
| week_of_year | INT | ISO week number | 3 |
| month | INT | Month number (1-12) | 1 |
| month_name | VARCHAR(10) | Name of the month | January |
| quarter | INT | Quarter (1-4) | 1 |
| year | INT | Year | 2024 |
| is_weekend | BOOLEAN | Weekend flag | FALSE |
| is_holiday | BOOLEAN | Holiday flag | FALSE |
| season | VARCHAR(10) | Season (Spring/Summer/Fall/Winter) | Winter |

### dim_time
Time dimension for intraday analysis.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| time_id | INT | Primary key | 1 |
| hour | INT | Hour (0-23) | 14 |
| minute | INT | Minute (0, 15, 30, 45) | 30 |
| time_of_day | VARCHAR(20) | Period of day | Afternoon |
| period | VARCHAR(10) | AM/PM | PM |
| is_business_hours | BOOLEAN | Business hours flag (9-17) | TRUE |

### dim_airport
Airport master data.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| airport_id | INT | Primary key | 1 |
| iata_code | VARCHAR(3) | IATA 3-letter code | JFK |
| icao_code | VARCHAR(4) | ICAO 4-letter code | KJFK |
| airport_name | VARCHAR(255) | Full airport name | John F. Kennedy International Airport |
| city | VARCHAR(100) | City name | New York |
| state | VARCHAR(100) | State/province | NY |
| country | VARCHAR(100) | Country name | USA |
| latitude | DECIMAL(9,6) | Latitude coordinate | 40.641311 |
| longitude | DECIMAL(9,6) | Longitude coordinate | -73.778139 |
| timezone | VARCHAR(50) | Timezone identifier | America/New_York |
| altitude_ft | INT | Altitude in feet | 13 |
| hub_type | VARCHAR(20) | Hub classification | Major Hub |
| is_international | BOOLEAN | International airport flag | TRUE |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |
| updated_date | TIMESTAMP | Last update timestamp | 2024-01-01 10:00:00 |

**Business Rules:**
- IATA code is unique
- Hub types: "Major Hub", "Hub", "Regional", "Other"

### dim_aircraft
Aircraft type information.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| aircraft_id | INT | Primary key | 1 |
| aircraft_code | VARCHAR(10) | Aircraft type code | B738 |
| manufacturer | VARCHAR(50) | Manufacturer name | Boeing |
| model | VARCHAR(50) | Aircraft model | 737-800 |
| aircraft_type | VARCHAR(30) | Type classification | Narrow-body |
| economy_seats | INT | Economy class seats | 162 |
| business_seats | INT | Business class seats | 12 |
| first_class_seats | INT | First class seats | 0 |
| total_capacity | INT | Total passenger capacity | 174 |
| range_km | INT | Maximum range in kilometers | 5765 |
| cruise_speed_kmh | INT | Cruise speed in km/h | 842 |
| fuel_capacity_liters | INT | Fuel capacity | 26000 |
| max_takeoff_weight_kg | INT | MTOW in kilograms | 79010 |
| year_manufactured | INT | Manufacturing year | 2020 |
| is_active | BOOLEAN | Active status | TRUE |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |
| updated_date | TIMESTAMP | Last update timestamp | 2024-01-01 10:00:00 |

**Business Rules:**
- total_capacity = economy_seats + business_seats + first_class_seats
- Aircraft types: "Narrow-body", "Wide-body", "Regional"

### dim_airline
Airline information.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| airline_id | INT | Primary key | 1 |
| airline_code | VARCHAR(3) | IATA 2-letter airline code | AA |
| airline_name | VARCHAR(100) | Full airline name | American Airlines |
| country | VARCHAR(100) | Home country | USA |
| alliance | VARCHAR(50) | Airline alliance | Oneworld |
| fleet_size | INT | Number of aircraft | 1000 |
| founded_year | INT | Year founded | 1930 |
| hub_airport_id | INT | Primary hub airport (FK) | 1 |
| is_low_cost | BOOLEAN | Low-cost carrier flag | FALSE |
| rating | DECIMAL(3,2) | Customer rating (1-5) | 4.2 |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |
| updated_date | TIMESTAMP | Last update timestamp | 2024-01-01 10:00:00 |

**Relationships:**
- FK: hub_airport_id → dim_airport.airport_id

**Business Rules:**
- Alliances: "Oneworld", "Star Alliance", "SkyTeam", NULL (independent)

### dim_customer
Customer/passenger profiles.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| customer_id | INT | Primary key | 1 |
| customer_code | VARCHAR(20) | Unique customer code | CUST00000001 |
| first_name | VARCHAR(50) | First name | John |
| last_name | VARCHAR(50) | Last name | Smith |
| email | VARCHAR(100) | Email address | john.smith@email.com |
| phone | VARCHAR(20) | Phone number | +1-555-1234 |
| date_of_birth | DATE | Date of birth | 1985-06-15 |
| gender | VARCHAR(10) | Gender | Male |
| country | VARCHAR(100) | Country of residence | USA |
| city | VARCHAR(100) | City of residence | New York |
| loyalty_tier | VARCHAR(20) | Loyalty program tier | Gold |
| loyalty_points | INT | Current loyalty points | 25000 |
| membership_date | DATE | Program join date | 2020-01-01 |
| preferred_airline_id | INT | Preferred airline (FK) | 1 |
| preferred_class | VARCHAR(20) | Preferred cabin class | Business |
| total_flights | INT | Lifetime flight count | 45 |
| is_active | BOOLEAN | Active customer flag | TRUE |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |
| updated_date | TIMESTAMP | Last update timestamp | 2024-01-01 10:00:00 |

**Relationships:**
- FK: preferred_airline_id → dim_airline.airline_id

**Business Rules:**
- Loyalty tiers: "None", "Silver", "Gold", "Platinum", "Diamond"
- Preferred classes: "Economy", "Premium Economy", "Business", "First"

### dim_route
Flight routes between airports.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| route_id | INT | Primary key | 1 |
| route_code | VARCHAR(10) | Route identifier | JFK-LAX |
| origin_airport_id | INT | Origin airport (FK) | 1 |
| destination_airport_id | INT | Destination airport (FK) | 2 |
| distance_km | INT | Distance in kilometers | 3983 |
| typical_duration_minutes | INT | Typical flight duration | 350 |
| route_type | VARCHAR(20) | Route classification | Long-haul |
| is_popular | BOOLEAN | Popular route flag | TRUE |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |

**Relationships:**
- FK: origin_airport_id → dim_airport.airport_id
- FK: destination_airport_id → dim_airport.airport_id

**Business Rules:**
- Route types: "Short-haul" (<500km), "Medium-haul" (500-3000km), "Long-haul" (>3000km)
- Route code format: ORIGIN-DESTINATION (IATA codes)

---

## Fact Tables

### fact_flight
Core fact table for flight operations.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| flight_id | BIGINT | Primary key | 1 |
| flight_number | VARCHAR(10) | Flight number | AA1234 |
| airline_id | INT | Airline (FK) | 1 |
| aircraft_id | INT | Aircraft type (FK) | 1 |
| route_id | INT | Route (FK) | 1 |
| origin_airport_id | INT | Origin airport (FK) | 1 |
| destination_airport_id | INT | Destination airport (FK) | 2 |
| scheduled_departure_date_id | INT | Scheduled departure date (FK) | 1 |
| scheduled_departure_time_id | INT | Scheduled departure time (FK) | 56 |
| scheduled_arrival_date_id | INT | Scheduled arrival date (FK) | 1 |
| scheduled_arrival_time_id | INT | Scheduled arrival time (FK) | 72 |
| actual_departure_date_id | INT | Actual departure date (FK) | 1 |
| actual_departure_time_id | INT | Actual departure time (FK) | 58 |
| actual_arrival_date_id | INT | Actual arrival date (FK) | 1 |
| actual_arrival_time_id | INT | Actual arrival time (FK) | 74 |
| scheduled_duration_minutes | INT | Scheduled flight time | 350 |
| actual_duration_minutes | INT | Actual flight time | 365 |
| departure_delay_minutes | INT | Departure delay | 15 |
| arrival_delay_minutes | INT | Arrival delay | 30 |
| flight_status | VARCHAR(20) | Flight status | On-Time |
| is_cancelled | BOOLEAN | Cancellation flag | FALSE |
| is_diverted | BOOLEAN | Diversion flag | FALSE |
| cancellation_reason | VARCHAR(100) | Reason for cancellation | NULL |
| total_seats | INT | Total available seats | 174 |
| economy_seats_sold | INT | Economy seats sold | 135 |
| business_seats_sold | INT | Business seats sold | 10 |
| first_class_seats_sold | INT | First class seats sold | 0 |
| total_passengers | INT | Total passengers | 145 |
| load_factor | DECIMAL(5,2) | Load factor percentage | 83.33 |
| total_revenue | DECIMAL(12,2) | Total flight revenue | 45750.00 |
| weather_delay_minutes | INT | Weather-related delay | 10 |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |

**Relationships:**
- Multiple FKs to dim_date, dim_time, dim_airline, dim_aircraft, dim_route, dim_airport

**Business Rules:**
- Flight statuses: "On-Time", "Delayed", "Cancelled", "Diverted"
- load_factor = (total_passengers / total_seats) * 100
- total_passengers = economy_seats_sold + business_seats_sold + first_class_seats_sold

**Key Metrics:**
- On-time performance: % of flights with arrival_delay_minutes <= 15
- Average delay: Mean of arrival_delay_minutes
- Cancellation rate: % of flights where is_cancelled = TRUE
- Capacity utilization: Average load_factor

### fact_booking
Booking and revenue fact table.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| booking_id | BIGINT | Primary key | 1 |
| booking_reference | VARCHAR(10) | Booking confirmation code | ABC123 |
| customer_id | INT | Customer (FK) | 1 |
| flight_id | BIGINT | Flight (FK) | 1 |
| airline_id | INT | Airline (FK) | 1 |
| booking_date_id | INT | Booking date (FK) | 1 |
| booking_time_id | INT | Booking time (FK) | 45 |
| departure_date_id | INT | Flight departure date (FK) | 30 |
| booking_channel | VARCHAR(30) | Booking channel | Website |
| cabin_class | VARCHAR(20) | Cabin class | Economy |
| num_passengers | INT | Number of passengers | 1 |
| base_fare | DECIMAL(10,2) | Base ticket price | 250.00 |
| taxes | DECIMAL(10,2) | Taxes and fees | 37.50 |
| fees | DECIMAL(10,2) | Additional fees | 25.00 |
| total_amount | DECIMAL(10,2) | Total booking amount | 312.50 |
| currency | VARCHAR(3) | Currency code | USD |
| booking_status | VARCHAR(20) | Booking status | Completed |
| is_group_booking | BOOLEAN | Group booking flag | FALSE |
| is_refunded | BOOLEAN | Refund flag | FALSE |
| checked_bags | INT | Number of checked bags | 1 |
| loyalty_points_earned | INT | Points earned | 312 |
| loyalty_points_redeemed | INT | Points redeemed | 0 |
| days_before_departure | INT | Booking window | 45 |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |

**Relationships:**
- FKs to dim_customer, fact_flight, dim_airline, dim_date, dim_time

**Business Rules:**
- Booking channels: "Website", "Mobile App", "Call Center", "Travel Agency", "Online Travel Agency", "Airport Counter", "Kiosk"
- Booking statuses: "Confirmed", "Pending", "Cancelled", "Completed", "No-Show"
- total_amount = base_fare + taxes + fees
- Booking window categories: 0-6, 7-13, 14-29, 30-59, 60+ days

**Key Metrics:**
- Total revenue: SUM(total_amount) WHERE booking_status = 'Completed'
- Average booking value: AVG(total_amount)
- Conversion rate: % of Confirmed/Completed vs Total bookings
- Advance purchase rate: Distribution of days_before_departure

### fact_passenger_journey
Individual passenger experience fact table.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| journey_id | BIGINT | Primary key | 1 |
| customer_id | INT | Customer (FK) | 1 |
| booking_id | BIGINT | Booking (FK) | 1 |
| flight_id | BIGINT | Flight (FK) | 1 |
| seat_number | VARCHAR(5) | Seat assignment | 12A |
| cabin_class | VARCHAR(20) | Cabin class | Economy |
| fare_paid | DECIMAL(10,2) | Fare amount | 312.50 |
| checked_in | BOOLEAN | Check-in status | TRUE |
| check_in_method | VARCHAR(20) | Check-in method | Mobile |
| check_in_time_minutes_before | INT | Minutes before departure | 90 |
| checked_bags | INT | Number of checked bags | 1 |
| baggage_weight_kg | DECIMAL(5,2) | Total baggage weight | 20.5 |
| meal_preference | VARCHAR(30) | Meal selection | Vegetarian |
| special_assistance | BOOLEAN | Special needs flag | FALSE |
| extra_legroom | BOOLEAN | Extra legroom flag | FALSE |
| priority_boarding | BOOLEAN | Priority boarding flag | FALSE |
| satisfaction_rating | INT | Customer rating (1-5) | 4 |
| complaint_filed | BOOLEAN | Complaint flag | FALSE |
| created_date | TIMESTAMP | Record creation timestamp | 2024-01-01 10:00:00 |

**Relationships:**
- FKs to dim_customer, fact_booking, fact_flight

**Business Rules:**
- Check-in methods: "Mobile", "Web", "Kiosk", "Counter", "Not Checked In"
- Meal preferences: "Standard", "Vegetarian", "Vegan", "Kosher", "Halal", "Gluten-Free", "Low-Sodium", "Diabetic", "Child Meal", "None"
- Satisfaction rating: 1 (Very Poor) to 5 (Excellent)

**Key Metrics:**
- Customer satisfaction: AVG(satisfaction_rating)
- Complaint rate: % where complaint_filed = TRUE
- Check-in conversion: % where checked_in = TRUE
- Ancillary revenue potential: % with extra services

---

## Star Schema Relationships

```
                    dim_date
                       |
                       |
    dim_airline   fact_flight ---- dim_time
        |              |
        |              |
    dim_aircraft   dim_route
                       |
                   dim_airport


    dim_customer ---- fact_booking ---- fact_flight
                          |
                          |
                  fact_passenger_journey
```

---

## Data Quality Rules

1. **Referential Integrity**: All foreign keys must reference existing records
2. **Data Completeness**: 
   - No NULL values in primary keys
   - Required fields: flight_number, customer_code, booking_reference
3. **Data Consistency**:
   - Dates: arrival_date >= departure_date
   - Capacity: passengers <= total_seats
   - Revenue: total_amount = base_fare + taxes + fees
4. **Business Logic**:
   - Load factor between 0 and 100
   - Delays can be negative (early arrival)
   - Cancelled flights have 0 passengers

---

## Common Query Patterns

### On-Time Performance
```sql
SELECT COUNT(*) * 100.0 / SUM(COUNT(*)) OVER()
FROM fact_flight
WHERE flight_status = 'On-Time'
```

### Revenue per Passenger
```sql
SELECT total_revenue / NULLIF(total_passengers, 0)
FROM fact_flight
```

### Customer Lifetime Value
```sql
SELECT customer_id, SUM(total_amount)
FROM fact_booking
WHERE booking_status = 'Completed'
GROUP BY customer_id
```

---

*Last Updated: January 2026*
