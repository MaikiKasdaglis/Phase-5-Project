#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
from datetime import datetime, timedelta

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, User, Year, Month, Pairing, Day
import random, datetime

fake = Faker()

def create_users():
    users = []
    role = ['flight_attendant', 'admin']
    for _ in range(15):
        u = User(
            username = fake.name(), 
            user_role = 'flight_attendant',
            email = fake.email(), 

            tfp_pay = 25.46,
            per_diem_pay = 2.35,
            international_per_diem_pay = 2.85,
            override_pay = 5.00,
            a_postion_pay = 2.00,
            password_hash = '123'
        )
        users.append(u)
    return users

def create_years():
    years = []
    for _ in range(15):
        y = Year(
            year = random.choice([2023, 2022]),
            user_id = fake.random_int(min=1, max=15),

            year_tfp = 10,
            year_vja = 10,
            year_holiday = 10,
            year_time_half = 10,
            year_double_time = 10,
            year_double_half = 10,
            year_triple =10,
            year_overrides = 0,
            year_a_hours = 10,
            year_tafb_total = 10,
            year_int_tafb_total = 10,

            year_duty_hours = 10,
            year_vacation_sick = 10,
        )
        years.append(y)
    return years
        

def create_months():
    months = []
    for _ in range(15):
        m = Month(
            month = fake.month(), 
            year = random.choice([2023, 2022]),
            guarantee_hours = fake.random_int(min=0, max=72),
            year_id = fake.random_int(min=1, max=15),

            month_tfp = 10,
            month_vja = 10,
            month_holiday = 10,
            month_time_half = 10,
            month_double_time = 10,
            month_double_half = 10,
            month_triple = 10,
            month_overrides = 10,
            month_a_hours = 10,
            month_tafb_total = 10, 
            month_int_tafb_total = 10,
            month_duty_hours = 10,
            month_vacation_sick = 10
        )
        months.append(m)
    return months

def create_pairings():
    pairings = []
    for _ in range(15): 
        p = Pairing(
            pairing_name = fake.date(),
            tafb_total = fake.random_int(min=0, max=50),
            int_tafb_total = fake.random_int(min=0, max=50),
            reserve_block = random.choice([True, False]),
            month_id = fake.random_int(min=1, max=15),

            pairing_tfp = 10,
            pairing_vja = 10,
            pairing_holiday = 10,
            pairing_time_half = 10,
            pairing_double_time = 10,
            pairing_double_half = 10,
            pairing_triple = 10,
            pairing_overrides = 10,
            pairing_a_hours = 10,

            pairing_duty_hours = 10,
            pairing_vacation_sick = 10,
        )
        pairings.append(p)
    return pairings

def create_days():
    current_year = datetime.datetime.now().year
    start_date = datetime.datetime(current_year, 1, 1)
    end_date = datetime.datetime(current_year, 12, 31)
    days = []
    for _ in range(25):
        d = Day(
            date=fake.date_between(start_date=start_date, end_date=end_date),
            total_tfp=fake.random_int(min=0, max=12),
            vja= 1,
            holiday= 1,
            time_half= 1,
            double_time= 1,
            double_half= 1,
            triple= 1,
            a_hours = 1,
            overrides=fake.random_int(min=0, max=5),
            reserve_no_fly=random.choice([True, False]),
            pairing_id=fake.random_int(min=1, max=15),
            a_position = random.choice([True, False]),

            daily_duty_hours = 1,
            vacation_sick = 1,
            comments = 'this is a comment',
            type_of_day =  random.choice(['Reserve', 'Trip', 'Sick', 'Vacation'])
        )
        days.append(d)
    return days

        
    

if __name__ == '__main__':
    with app.app_context():
        print('clearing db..')
        User.query.delete()
        Year.query.delete()
        Month.query.delete()
        Pairing.query.delete()
        Day.query.delete()

        print("Seeding Users...")
        users = create_users()
        db.session.add_all(users)
        db.session.commit()

        print("Seeding Years...")
        years = create_years()
        db.session.add_all(years)
        db.session.commit()

        print("Seeding Months...")
        months = create_months()
        db.session.add_all(months)
        db.session.commit()

        print("Seeding Pairings...")
        pairings = create_pairings()
        db.session.add_all(pairings)
        db.session.commit()

        print("Seeding Days...")
        Days = create_days()
        db.session.add_all(Days)
        db.session.commit()



