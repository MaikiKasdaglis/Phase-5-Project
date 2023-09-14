#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource


# Local imports
from config import app, db, api
# Add your model imports
from models import User, Month, Pairing, Day, Year
import requests


# Views go here!
#======================DAY MATH========================================
def tfp_pay_function(total_tfp):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = user.tfp_pay * total_tfp
    # print(total) 
    return round(total, 2) 

def more_better_function_rate(tfp, rate):
    total = tfp * rate
    return total
def more_better_function_pay(total_tfp, rate):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = user.tfp_pay * (total_tfp * rate)
    # print(total) 
    return round(total, 2) 

#===========================1.5=======================================
def one_point_five_rate(tfp):
    total = tfp * 1.5
    return total
def one_point_five_pay(tfp):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = (tfp * 1.5)* user.tfp_pay
    return round(total, 2)
#===========================2=======================================
def double_rate(tfp):
    total = tfp * 2
    return total
def double_pay(tfp):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = (tfp * 2)* user.tfp_pay
    return round(total, 2)
#===========================2.5=======================================
def double_point_five_rate(tfp):
    total = tfp * 2.5
    return total
def double_point_five_pay(tfp):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = (tfp * 2.5)* user.tfp_pay
    return round(total, 2)
#===========================3=======================================
def triple_rate(tfp):
    total = tfp * 3
    return total
def triple_pay(tfp):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = (tfp * 3)* user.tfp_pay
    return round(total, 2)
#===========================A_Pay // TAFB // Overrides=========================
def a_position_hours(*hours):
    sum = 0 
    for n in hours:
        sum = sum + n
    return sum
def a_position_pay(position, hours):
    if position:
        user = User.query.filter(User.id == session.get('user_id')).first()
        total = user.a_postion_pay * hours
        return total 
    else:
        return 0 
def container_a_position_pay(hours):
        user = User.query.filter(User.id == session.get('user_id')).first()
        total = user.a_postion_pay * hours
        return total 

def override_pay(overrides):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = user.override_pay * overrides
    return total 

def tafb_pay(tafb):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = user.per_diem_pay * tafb
    return total
def int_tafb_pay(tafb):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = user.international_per_diem_pay * tafb
    return total
#===========================Totals=========================
def totals(*hours):
    sum = 0 
    for n in hours:
        sum = sum + n
    return sum
#=====================================================================

@app.route('/')
def index():
    return '<h1>Phase 4 Project Server</h1>'

class Users(Resource):
    def get(self):
        users = [u.to_dict() for u in User.query.all()]
        return make_response(users, 200)
    def post(self):
        request_obj = request.get_json()
        try:
            new_user = User(
                username =request_obj["username"],
                user_role = request_obj["user_role"],
                email =request_obj["email"],
                tfp_pay = request_obj["tfp_pay"],
                per_diem_pay =request_obj["per_diem_pay"],
                international_per_diem_pay =request_obj["international_per_diem_pay"],
                override_pay =request_obj["override_pay"],
                a_postion_pay =request_obj["a_postion_pay"],
                # _password_hash=request_obj["a_postion_pay"],
            )
            new_user.password_hash = request_obj["_password_hash"]
            #i had to add an underscore to seed. when bcrypt is working, likely it will need to be removed 
            db.session.add(new_user)
            db.session.commit()
            session['user_id'] = new_user.id
            #THE ABOVE CODE WILL BE UTILIZED WITH ZUSTAND
        except Exception as e:
            message = {'errors': [e.__str__()]}
            return make_response(message, 422)
        return make_response(new_user.to_dict(),200)
api.add_resource(Users, '/users')

class UsersById(Resource):
    def get(self,id):
        response_obj = User.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                "error": "User not found"
            }
            return make_response(response_dict, 404)
        else:
            return make_response(response_obj.to_dict(), 200)
    def patch (self, id):
        response_obj = User.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                "error": "User not found"
            }
            return make_response(response_dict, 404)
        else:
            request_object = request.get_json()
            try:
                for attr in request_object:
                    setattr(response_obj, attr, request_object[attr])
                    # response_obj.password_hash = request_object["_password_hash"]
                    #will likely need above code when refactor for bcrypt
                    db.session.add(response_obj)
                    db.session.commit()
            except Exception as e:
                message = {'errors': [e.__str__()]}
                return make_response(message, 422)
            return make_response(response_obj.to_dict(), 200)
    def delete(self, id):
        response_obj = User.query.filter_by(id=id).first()
        if response_obj == None: 
            response_dict = {
                "error": "User not found"
            }
            return make_response(response_dict, 404)
        else:
            db.session.delete(response_obj)
            db.session.commit()
            response_dict = {"message": "deleted fo sho!"}
            return response_dict, 200
api.add_resource(UsersById, '/users/<int:id>')

class Years(Resource):
    def get(self):
        years =[y.to_dict() for y in Year.query.all()]
        return make_response(years, 200)
    def post(self):
        request_obj = request.get_json()
        try:
            new_year = Year(
                year = request_obj["year"],
                user_id = request_obj["user_id"],

                #=============TAFB
                year_tafb_total = request_obj["year_tafb_total"],
                year_tafb_pay = tafb_pay(request_obj["year_tafb_total"]),
                #=============TAFB
                year_int_tafb_total = request_obj["year_int_tafb_total"],
                year_int_tafb_pay = int_tafb_pay(request_obj["year_int_tafb_pay"]),
                #================TFP LYFE
                year_tfp = request_obj["year_tfp"],
                year_tfp_pay = tfp_pay_function(request_obj["year_tfp"]),
                #================ VACATION/SICK LYFE
                year_vacation_sick = request_obj["year_vacation_sick"],
                year_vacation_sick_pay = tfp_pay_function(request_obj["year_vacation_sick"]),
                #================VJA LYFE
                year_vja = request_obj["year_vja"],
                year_vja_rated= one_point_five_rate(request_obj["year_vja"]),
                year_vja_pay= one_point_five_pay(request_obj["year_vja"]),
                #================ HOLIDAY LYFE
                year_holiday = request_obj["year_holiday"],
                year_holiday_rated = double_rate(request_obj["year_holiday"]),
                year_holiday_pay = double_pay(request_obj["year_holiday"]),
                #================ TIME_HALF
                year_time_half = request_obj["year_time_half"],
                year_time_half_rated = one_point_five_rate(request_obj["year_time_half"]),
                year_time_half_pay = one_point_five_pay(request_obj["year_time_half"]),
                #================ DOUBLE TIME LYFE
                year_double_time = request_obj["year_double_time"],
                year_double_time_rated = more_better_function_rate(request_obj["year_double_time"],2),
                year_double_time_pay = more_better_function_pay(request_obj["year_double_time"],2),
                #================ DOUBLE & HALF LYFE
                year_double_half = request_obj["year_double_half"],
                year_double_half_rated = more_better_function_rate(request_obj["year_double_half"],2.5),
                year_double_half_pay = more_better_function_pay(request_obj["year_double_half"],2.5),
                #================ TRIPLE LYFE
                year_triple = request_obj["year_triple"],
                year_triple_rated = more_better_function_rate(request_obj["year_triple"],3),
                year_triple_pay = more_better_function_pay(request_obj["year_triple"],3),
                #================ OVERRIDES LYFE
                year_overrides = request_obj["year_overrides"],
                year_overrides_pay = override_pay(request_obj["year_overrides"]),
                #================ A-POSITION LYFE
                year_a_hours = request_obj["year_a_hours"],
                year_a_pay = container_a_position_pay(request_obj["year_a_hours"]),
                #============Totals ACTUAL 
                year_total_credits = totals(request_obj["year_tfp"],request_obj["year_vacation_sick"],request_obj["year_vja"],request_obj["year_holiday"],request_obj["year_time_half"],request_obj["year_double_time"],request_obj["year_double_half"],request_obj["year_triple"]),
                #============Totals RATED 
                year_total_credits_rated = totals(request_obj["year_tfp"],request_obj["year_vacation_sick"],one_point_five_rate(request_obj["year_vja"]),double_rate(request_obj["year_holiday"]),one_point_five_rate(request_obj["year_time_half"]),more_better_function_rate(request_obj["year_double_time"],2),more_better_function_rate(request_obj["year_double_half"],2.5),more_better_function_rate(request_obj["year_triple"],3)),
                #============Totals PAY 
                year_total_pay = totals(tfp_pay_function(request_obj["year_tfp"]),tfp_pay_function(request_obj["year_vacation_sick"]),one_point_five_pay(request_obj["year_vja"]),double_pay(request_obj["year_holiday"]),one_point_five_pay(request_obj["year_time_half"]),more_better_function_pay(request_obj["year_double_time"],2),more_better_function_pay(request_obj["year_double_half"],2.5),more_better_function_pay(request_obj["year_triple"],3), tafb_pay(request_obj["year_tafb_total"]),int_tafb_pay(request_obj["year_int_tafb_total"]),override_pay(request_obj["year_overrides"]),container_a_position_pay(request_obj["year_a_hours"])),
                #============Totals DUTY HOURS 
                year_duty_hours = request_obj["year_duty_hours"],
            )
            db.session.add(new_year)
            db.session.commit()
            # Create associated months
            month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            for month in range(1, 13):
                new_month = Month(
                    month=month_names[month-1],
                    year=new_year.year,
                    month_guarantee_hours=0,
                    year_id=new_year.id,
                    month_tfp=0,
                    month_vja=0,
                    month_holiday=0,
                    month_time_half=0,
                    month_double_time=0,
                    month_double_half=0,
                    month_triple=0,
                    month_overrides=0,
                    month_a_hours=0,
                    month_tafb_total=0,
                    month_int_tafb_total=0,
                    month_duty_hours=0,
                    month_vacation_sick=0
                )
                db.session.add(new_month)
                db.session.commit()

            # Create pairings for each month
                pairing_names = ["Pairing 1", "Pairing 2", "Pairing 3", "Pairing 4"]
                for pairing in range(1, 5):
                    new_pairing = Pairing(
                        pairing_name=pairing_names[pairing-1],
                        tafb_total=0,
                        int_tafb_total=0,
                        reserve_block=False,
                        month_id=new_month.id,
                        pairing_tfp = 0,
                        pairing_vja = 0,
                        pairing_holiday = 0,
                        pairing_time_half = 0,
                        pairing_double_time = 0,
                        pairing_double_half = 0,
                        pairing_triple = 0,
                        pairing_overrides = 0,
                        pairing_a_hours = 0,
                        pairing_duty_hours = 0,
                        pairing_vacation_sick = 0,
                    )
                    db.session.add(new_pairing)
                    db.session.commit()
                    day_names = ["Day 1", "Day 2", "Day 3"]
                    for day in range(3):
                        new_day = Day(
                            pairing_id=new_pairing.id,
                            date=day_names[day],
                            total_tfp=0,
                            vja= 0,
                            holiday= 0,
                            time_half= 0,
                            double_time= 0,
                            double_half= 0,
                            triple= 0,
                            a_hours = 0,
                            overrides=0,
                            reserve_no_fly=False,
                            a_position = False,
                            daily_duty_hours = 0,
                            vacation_sick = 0,
                            comments = '',
                            type_of_day =  'TBD'
                        )
                        db.session.add(new_day)
                        db.session.commit()
        except Exception as e:
            message = {'errors': [e.__str__()]}
            return make_response(message, 422)
        return make_response(new_year.to_dict(),200)
api.add_resource(Years, '/years')

class YearsById(Resource):
    def get(self, id):
        response_obj = Year.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Year not found'
            }
            return make_response(response_dict, 404)
        else:
            return make_response(response_obj.to_dict(), 200)
    def patch(self, id):
        response_obj = Year.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Year not found'
            }
            return make_response(response_dict, 404)
        else:
            request_object = request.get_json()
            try:
                for attr in request_object:
                    setattr(response_obj, attr, request_object[attr])

                #============VACATION/SICK
                if "year_vacation_sick" in request_object:
                    response_obj.year_vacation_sick_pay = tfp_pay_function(request_object["year_vacation_sick"])
                #============REGULAR TFP
                if "year_tfp" in request_object:
                    response_obj.year_tfp_pay = tfp_pay_function(request_object["year_tfp"])
                #============VJA
                if "year_vja" in request_object:
                    response_obj.year_vja_rated = one_point_five_rate(request_object["year_vja"])
                    response_obj.year_vja_pay = one_point_five_pay(request_object["year_vja"])
                #============HOLIDAY
                if "year_holiday" in request_object:
                    response_obj.year_holiday_rated = double_rate(request_object["year_holiday"])
                    response_obj.year_holiday_pay = double_pay(request_object["year_holiday"])
                #============TIME_HALF
                if "year_time_half" in request_object:
                    response_obj.year_time_half_rated  = one_point_five_rate(request_object["year_time_half"])
                    response_obj.year_time_half_pay = one_point_five_pay(request_object["year_time_half"])
                #============DOUBLE_TIME
                if "year_double_time" in request_object:
                    response_obj.year_double_time_rated = double_rate(request_object["year_double_time"])
                    response_obj.year_double_time_pay = double_pay(request_object["year_double_time"])
                #============DOUBLE_HALF
                if "year_double_half" in request_object:
                    response_obj.year_double_half_rated = double_point_five_rate(request_object["year_double_half"])
                    response_obj.year_double_half_pay = double_point_five_pay(request_object["year_double_half"])
                #============TRIPLE
                if "year_triple" in request_object:
                    response_obj.year_triple_rated = triple_rate(request_object["year_triple"])
                    response_obj.year_triple_pay = triple_pay(request_object["year_triple"])
                #============OVERRIDES
                response_obj.year_overrides_pay = override_pay(request_object["year_overrides"])
                #============A-POSITON
                if "year_a_hours" in request_object:
                    response_obj.year_a_pay = container_a_position_pay(request_object["year_a_hours"])
                #=============TAFB
                response_obj.year_tafb_pay = tafb_pay(request_object["year_tafb_total"])
                response_obj.year_int_tafb_pay = int_tafb_pay(request_object["year_int_tafb_total"])
                #============Totals ACTUAL 
                response_obj.year_total_credits = totals(request_object["year_tfp"],request_object["year_vacation_sick"],request_object["year_vja"],request_object["year_holiday"],request_object["year_time_half"],request_object["year_double_time"],request_object["year_double_half"],request_object["year_triple"])
                #============Totals RATED
                response_obj.year_total_credits_rated= totals(request_object["year_tfp"],request_object["year_vacation_sick"],one_point_five_rate(request_object["year_vja"]),double_rate(request_object["year_holiday"]),one_point_five_rate(request_object["year_time_half"]),more_better_function_rate(request_object["year_double_time"],2),more_better_function_rate(request_object["year_double_half"],2.5),more_better_function_rate(request_object["year_triple"],3))
                #============Totals PAY
                response_obj.year_total_pay = totals(tfp_pay_function(request_object["year_tfp"]),tfp_pay_function(request_object["year_vacation_sick"]),one_point_five_pay(request_object["year_vja"]),double_pay(request_object["year_holiday"]),one_point_five_pay(request_object["year_time_half"]),more_better_function_pay(request_object["year_double_time"],2),more_better_function_pay(request_object["year_double_half"],2.5),more_better_function_pay(request_object["year_triple"],3), tafb_pay(request_object["year_tafb_total"]),int_tafb_pay(request_object["year_int_tafb_total"]),override_pay(request_object["year_overrides"]),container_a_position_pay(request_object["year_a_hours"]))
                #=====================


                db.session.add(response_obj)
                db.session.commit()
            except Exception as e:
                message = {'errors': [e.__str__()]}
                return make_response(message, 422)
            return make_response(response_obj.to_dict(), 200)
    def delete(self, id):
        response_obj = Year.query.filter_by(id=id).first()
        if response_obj == None: 
            response_dict = {
                "error": "Year not found"
            }
            return make_response(response_dict, 404)
        else:
            db.session.delete(response_obj)
            db.session.commit()
            response_dict = {"message": "deleted fo sho!"}
            return response_dict, 200
api.add_resource(YearsById, '/years/<int:id>')

class Months(Resource):
    def get(self):
        months =[m.to_dict() for m in Month.query.all()]
        return make_response(months, 200)
    def post(self): 
        request_obj = request.get_json()
        try:
            new_month = Month(
                month = request_obj["month"],
                year = request_obj["year"],
                year_id = request_obj["year_id"],
                #=============TAFB
                month_tafb_total = request_obj["month_tafb_total"],
                month_tafb_pay = tafb_pay(request_obj["month_tafb_total"]),
                #=============TAFB
                month_int_tafb_total = request_obj["month_int_tafb_total"],
                month_int_tafb_pay = int_tafb_pay(request_obj["month_int_tafb_pay"]),
                #================TFP LYFE
                month_tfp = request_obj["month_tfp"],
                month_tfp_pay = tfp_pay_function(request_obj["month_tfp"]),
                #================ VACATION/SICK LYFE
                month_vacation_sick = request_obj["month_vacation_sick"],
                month_vacation_sick_pay = tfp_pay_function(request_obj["month_vacation_sick"]),
                #================VJA LYFE
                month_vja = request_obj["month_vja"],
                month_vja_rated= one_point_five_rate(request_obj["month_vja"]),
                month_vja_pay= one_point_five_pay(request_obj["month_vja"]),
                #================ HOLIDAY LYFE
                month_holiday = request_obj["month_holiday"],
                month_holiday_rated = double_rate(request_obj["month_holiday"]),
                month_holiday_pay = double_pay(request_obj["month_holiday"]),
                #================ TIME_HALF
                month_time_half = request_obj["month_time_half"],
                month_time_half_rated = one_point_five_rate(request_obj["month_time_half"]),
                month_time_half_pay = one_point_five_pay(request_obj["month_time_half"]),
                #================ DOUBLE TIME LYFE
                month_double_time = request_obj["month_double_time"],
                month_double_time_rated = more_better_function_rate(request_obj["month_double_time"],2),
                month_double_time_pay = more_better_function_pay(request_obj["month_double_time"],2),
                #================ DOUBLE & HALF LYFE
                month_double_half = request_obj["month_double_half"],
                month_double_half_rated = more_better_function_rate(request_obj["month_double_half"],2.5),
                month_double_half_pay = more_better_function_pay(request_obj["month_double_half"],2.5),
                #================ TRIPLE LYFE
                month_triple = request_obj["month_triple"],
                month_triple_rated = more_better_function_rate(request_obj["month_triple"],3),
                month_triple_pay = more_better_function_pay(request_obj["month_triple"],3),
                #================ OVERRIDES LYFE
                month_overrides = request_obj["month_overrides"],
                month_overrides_pay = override_pay(request_obj["month_overrides"]),
                #================ A-POSITION LYFE
                month_a_hours = request_obj["month_a_hours"],
                month_a_pay = container_a_position_pay(request_obj["month_a_hours"]),
                #===============Reserve Stuff 
                #===========================THESE MUST BE TOTALED FROM PAIRINGS?
                month_guarantee_hours = request_obj["month_guarantee_hours"],
                month_guarantee_hours_worked_rated = request_obj["month_guarantee_hours_worked_rated"],
                #============Totals ACTUAL 
                month_total_credits = totals(request_obj["month_tfp"],request_obj["month_vacation_sick"],request_obj["month_vja"],request_obj["month_holiday"],request_obj["month_time_half"],request_obj["month_double_time"],request_obj["month_double_half"],request_obj["month_triple"]),
                #============Totals RATED 
                month_total_credits_rated = totals(request_obj["month_tfp"],request_obj["month_vacation_sick"],one_point_five_rate(request_obj["month_vja"]),double_rate(request_obj["month_holiday"]),one_point_five_rate(request_obj["month_time_half"]),more_better_function_rate(request_obj["month_double_time"],2),more_better_function_rate(request_obj["month_double_half"],2.5),more_better_function_rate(request_obj["month_triple"],3)),
                #============Totals PAY 
                month_total_pay = totals(tfp_pay_function(request_obj["month_tfp"]),tfp_pay_function(request_obj["month_vacation_sick"]),one_point_five_pay(request_obj["month_vja"]),double_pay(request_obj["month_holiday"]),one_point_five_pay(request_obj["month_time_half"]),more_better_function_pay(request_obj["month_double_time"],2),more_better_function_pay(request_obj["month_double_half"],2.5),more_better_function_pay(request_obj["month_triple"],3), tafb_pay(request_obj["month_tafb_total"]),int_tafb_pay(request_obj["month_int_tafb_total"]),override_pay(request_obj["month_overrides"]),container_a_position_pay(request_obj["month_a_hours"])),
                #============Totals DUTY HOURS 
                month_duty_hours = request_obj["month_duty_hours"],
                
            )
            db.session.add(new_month)
            db.session.commit()
        except Exception as e:
            message = {'errors': [e.__str__()]}
            return make_response(message, 422)
        return make_response(new_month.to_dict(),200)
api.add_resource(Months, '/months')

class MonthsById(Resource):
    def get(self, id):
        response_obj = Month.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Month not found'
            }
            return make_response(response_dict, 404)
        else:
            return make_response(response_obj.to_dict(), 200)
    def patch(self,id):
        response_obj = Month.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Month not found'
            }
            return make_response(response_dict, 404)
        else:
            request_object = request.get_json()
            try:
                for attr in request_object:
                    setattr(response_obj, attr, request_object[attr])

                 #============VACATION/SICK
                if "month_vacation_sick" in request_object:
                    response_obj.month_vacation_sick_pay = tfp_pay_function(request_object["month_vacation_sick"])
                #============REGULAR TFP
                if "month_tfp" in request_object:
                    response_obj.month_tfp_pay = tfp_pay_function(request_object["month_tfp"])
                #============VJA
                if "month_vja" in request_object:
                    response_obj.month_vja_rated = one_point_five_rate(request_object["month_vja"])
                    response_obj.month_vja_pay = one_point_five_pay(request_object["month_vja"])
                #============HOLIDAY
                if "month_holiday" in request_object:
                    response_obj.month_holiday_rated = double_rate(request_object["month_holiday"])
                    response_obj.month_holiday_pay = double_pay(request_object["month_holiday"])
                #============TIME_HALF
                if "month_time_half" in request_object:
                    response_obj.month_time_half_rated  = one_point_five_rate(request_object["month_time_half"])
                    response_obj.month_time_half_pay = one_point_five_pay(request_object["month_time_half"])
                #============DOUBLE_TIME
                if "month_double_time" in request_object:
                    response_obj.month_double_time_rated = double_rate(request_object["month_double_time"])
                    response_obj.month_double_time_pay = double_pay(request_object["month_double_time"])
                #============DOUBLE_HALF
                if "month_double_half" in request_object:
                    response_obj.month_double_half_rated = double_point_five_rate(request_object["month_double_half"])
                    response_obj.month_double_half_pay = double_point_five_pay(request_object["month_double_half"])
                #============TRIPLE
                if "month_triple" in request_object:
                    response_obj.month_triple_rated = triple_rate(request_object["month_triple"])
                    response_obj.month_triple_pay = triple_pay(request_object["month_triple"])
                #============OVERRIDES
                response_obj.month_overrides_pay = override_pay(request_object["month_overrides"])
                #============A-POSITON
                if "month_a_hours" in request_object:
                    response_obj.month_a_pay = container_a_position_pay(request_object["month_a_hours"])
                #=============TAFB
                response_obj.month_tafb_pay = tafb_pay(request_object["month_tafb_total"])
                response_obj.month_int_tafb_pay = int_tafb_pay(request_object["month_int_tafb_total"])
                #===============Reserve Stuff 
                #===========================THESE MUST BE TOTALED FROM PAIRINGS?
                # sum_month_guarantee_hours = 0
                # pairings = Pairing.query.filter_by(month_id=response_obj.id)
                # for p in pairings:
                #     if p.reserve_block:
                #         sum_month_guarantee_hours += p.pairing_guarantee_hours
                # response_obj.month_guarantee_hours = sum_month_guarantee_hours



                # response_obj.month_guarantee_hours = request_object["month_guarantee_hours"],
                # response_obj.month_guarantee_hours_worked_rated = request_object["month_guarantee_hours_worked_rated"],

                #============Totals ACTUAL 
                response_obj.month_total_credits = totals(request_object["month_tfp"],request_object["month_vacation_sick"],request_object["month_vja"],request_object["month_holiday"],request_object["month_time_half"],request_object["month_double_time"],request_object["month_double_half"],request_object["month_triple"])
                #============Totals RATED
                response_obj.month_total_credits_rated= totals(request_object["month_tfp"],request_object["month_vacation_sick"],one_point_five_rate(request_object["month_vja"]),double_rate(request_object["month_holiday"]),one_point_five_rate(request_object["month_time_half"]),more_better_function_rate(request_object["month_double_time"],2),more_better_function_rate(request_object["month_double_half"],2.5),more_better_function_rate(request_object["month_triple"],3))
                #============Totals PAY
                response_obj.month_total_pay = totals(tfp_pay_function(request_object["month_tfp"]),tfp_pay_function(request_object["month_vacation_sick"]),one_point_five_pay(request_object["month_vja"]),double_pay(request_object["month_holiday"]),one_point_five_pay(request_object["month_time_half"]),more_better_function_pay(request_object["month_double_time"],2),more_better_function_pay(request_object["month_double_half"],2.5),more_better_function_pay(request_object["month_triple"],3), tafb_pay(request_object["month_tafb_total"]),int_tafb_pay(request_object["month_int_tafb_total"]),override_pay(request_object["month_overrides"]),container_a_position_pay(request_object["month_a_hours"]))
                #=====================

                db.session.add(response_obj)
                db.session.commit()
            except Exception as e:
                message = {'errors': [e.__str__()]}
                return make_response(message, 422)
            return make_response(response_obj.to_dict(), 200)
    def delete(self, id):
        response_obj = Month.query.filter_by(id=id).first()
        if response_obj == None: 
            response_dict = {
                "error": "Month not found"
            }
            return make_response(response_dict, 404)
        else:
            db.session.delete(response_obj)
            db.session.commit()
            response_dict = {"message": "deleted fo sho!"}
            return response_dict, 200
api.add_resource(MonthsById, '/months/<int:id>')

class Pairings(Resource):
    def get(self):
        pairings =[p.to_dict() for p in Pairing.query.all()]
        return make_response(pairings, 200)
    def post(self):
        request_obj = request.get_json()
        try:
            new_pairing = Pairing(
                pairing_name = request_obj["pairing_name"],
                month_id = request_obj["month_id"],

                
                #=============TAFB
                tafb_total = request_obj["tafb_total"],
                tafb_pay = tafb_pay(request_obj["tafb_total"]),
                #=============TAFB
                int_tafb_total = request_obj["int_tafb_total"],
                int_tafb_pay = int_tafb_pay(request_obj["int_tafb_total"]),
                #================TFP LYFE
                pairing_tfp = request_obj["pairing_tfp"],
                pairing_tfp_pay = tfp_pay_function(request_obj["pairing_tfp"]),
                #================ VACATION/SICK LYFE
                pairing_vacation_sick = request_obj["pairing_vacation_sick"],
                pairing_vacation_sick_pay = tfp_pay_function(request_obj["pairing_vacation_sick"]),
                #================VJA LYFE
                pairing_vja = request_obj["pairing_vja"],
                pairing_vja_rated= one_point_five_rate(request_obj["pairing_vja"]),
                pairing_vja_pay= one_point_five_pay(request_obj["pairing_vja"]),
                #================ HOLIDAY LYFE
                pairing_holiday = request_obj["pairing_holiday"],
                pairing_holiday_rated = double_rate(request_obj["pairing_holiday"]),
                pairing_holiday_pay = double_pay(request_obj["pairing_holiday"]),
                #================ TIME_HALF
                pairing_time_half = request_obj["pairing_time_half"],
                pairing_time_half_rated = one_point_five_rate(request_obj["pairing_time_half"]),
                pairing_time_half_pay = one_point_five_pay(request_obj["pairing_time_half"]),
                #================ DOUBLE TIME LYFE
                pairing_double_time = request_obj["pairing_double_time"],
                pairing_double_time_rated = more_better_function_rate(request_obj["pairing_double_time"],2),
                pairing_double_time_pay = more_better_function_pay(request_obj["pairing_double_time"],2),
                #================ DOUBLE & HALF LYFE
                pairing_double_half = request_obj["pairing_double_half"],
                pairing_double_half_rated = more_better_function_rate(request_obj["pairing_double_half"],2.5),
                pairing_double_half_pay = more_better_function_pay(request_obj["pairing_double_half"],2.5),
                #================ TRIPLE LYFE
                pairing_triple = request_obj["pairing_triple"],
                pairing_triple_rated = more_better_function_rate(request_obj["pairing_triple"],3),
                pairing_triple_pay = more_better_function_pay(request_obj["pairing_triple"],3),
                #================ OVERRIDES LYFE
                pairing_overrides = request_obj["pairing_overrides"],
                pairing_overrides_pay = override_pay(request_obj["pairing_overrides"]),
                #================ A-POSITION LYFE
                pairing_a_hours = request_obj["pairing_a_hours"],
                pairing_a_pay = container_a_position_pay(request_obj["pairing_a_hours"]),

                #===============Reserve Stuff 
                reserve_block = request_obj["reserve_block"],

                #hella need some function here!!!!!!!!!!!!!!!!!!
                pairing_guarantee_hours = request_obj["pairing_guarantee_hours"],

                #===============Hours that can be subtraced from guarantee on frontend
                pairing_guarantee_hours_worked_rated = totals(request_obj["pairing_tfp"],request_obj["pairing_vacation_sick"],one_point_five_rate(request_obj["pairing_vja"]),double_rate(request_obj["pairing_holiday"]),one_point_five_rate(request_obj["pairing_time_half"]),more_better_function_rate(request_obj["pairing_double_time"],2),more_better_function_rate(request_obj["pairing_double_half"],2.5),more_better_function_rate(request_obj["pairing_triple"],3)) if request_obj["reserve_block"] else 0,

                #============Totals ACTUAL 
                pairing_total_credits = totals(request_obj["pairing_tfp"],request_obj["pairing_vacation_sick"],request_obj["pairing_vja"],request_obj["pairing_holiday"],request_obj["pairing_time_half"],request_obj["pairing_double_time"],request_obj["pairing_double_half"],request_obj["pairing_triple"]),
                #============Totals RATED 
                pairing_total_credits_rated = totals(request_obj["pairing_tfp"],request_obj["pairing_vacation_sick"],one_point_five_rate(request_obj["pairing_vja"]),double_rate(request_obj["pairing_holiday"]),one_point_five_rate(request_obj["pairing_time_half"]),more_better_function_rate(request_obj["pairing_double_time"],2),more_better_function_rate(request_obj["pairing_double_half"],2.5),more_better_function_rate(request_obj["pairing_triple"],3)),
                #============Totals PAY 
                pairing_total_pay = totals(tfp_pay_function(request_obj["pairing_tfp"]),tfp_pay_function(request_obj["pairing_vacation_sick"]),one_point_five_pay(request_obj["pairing_vja"]),double_pay(request_obj["pairing_holiday"]),one_point_five_pay(request_obj["pairing_time_half"]),more_better_function_pay(request_obj["pairing_double_time"],2),more_better_function_pay(request_obj["pairing_double_half"],2.5),more_better_function_pay(request_obj["pairing_triple"],3), tafb_pay(request_obj["tafb_total"]),int_tafb_pay(request_obj["int_tafb_total"]),override_pay(request_obj["pairing_overrides"]),container_a_position_pay(request_obj["pairing_a_hours"])),
                #============Totals DUTY HOURS 
                pairing_duty_hours = request_obj["pairing_duty_hours"],
                #========New additions=======

            )
            db.session.add(new_pairing)
            db.session.commit()
            day_names = ["Day 1", "Day 2", "Day 3"]
            for day in range(3):
                new_day = Day(
                    pairing_id=new_pairing.id,
                    date=day_names[day],
                    total_tfp=0,
                    vja= 0,
                    holiday= 0,
                    time_half= 0,
                    double_time= 0,
                    double_half= 0,
                    triple= 0,
                    a_hours = 0,
                    overrides=0,
                    reserve_no_fly=False,
                    a_position = False,
                    daily_duty_hours = 0,
                    vacation_sick = 0,
                    comments = '',
                    type_of_day =  'TBD'
                )
                db.session.add(new_day)
                db.session.commit()

        except Exception as e:
            message = {'errors': [e.__str__()]}
            return make_response(message, 422)
        return make_response(new_pairing.to_dict(),200)
api.add_resource(Pairings, '/pairings')

class PairingsById(Resource):
    def get(self,id):
        response_obj = Pairing.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Pairing not found'
            }
            return make_response(response_dict, 404)
        else:
            return make_response(response_obj.to_dict(), 200)
    def patch(self, id):
        response_obj = Pairing.query.filter_by(id=id).first()
        
        if response_obj == None:
            response_dict = {
                'error': 'Pairing not found'
            }
            return make_response(response_dict, 404)
        else:
            request_object = request.get_json()
            try:
                # =====================COMMENT BACK IN IF YOUR DUMB FUCKING IDEA FAILS. 
                for attr in request_object:
                    setattr(response_obj, attr, request_object[attr])

                #New shit ============
                #============VACATION/SICK
                if "pairing_vacation_sick" in request_object:
                    response_obj.pairing_vacation_sick_pay = tfp_pay_function(request_object["pairing_vacation_sick"])
                #============REGULAR TFP
                if "pairing_tfp" in request_object:
                    response_obj.pairing_tfp_pay = tfp_pay_function(request_object["pairing_tfp"])
                #============VJA
                if "pairing_vja" in request_object:
                    response_obj.pairing_vja_rated = one_point_five_rate(request_object["pairing_vja"])
                    response_obj.pairing_vja_pay = one_point_five_pay(request_object["pairing_vja"])
                #============HOLIDAY
                if "pairing_holiday" in request_object:
                    response_obj.pairing_holiday_rated = double_rate(request_object["pairing_holiday"])
                    response_obj.pairing_holiday_pay = double_pay(request_object["pairing_holiday"])
                #============TIME_HALF
                if "pairing_time_half" in request_object:
                    response_obj.pairing_time_half_rated  = one_point_five_rate(request_object["pairing_time_half"])
                    response_obj.pairing_time_half_pay = one_point_five_pay(request_object["pairing_time_half"])
                #============DOUBLE_TIME
                if "pairing_double_time" in request_object:
                    response_obj.pairing_double_time_rated = double_rate(request_object["pairing_double_time"])
                    response_obj.pairing_double_time_pay = double_pay(request_object["pairing_double_time"])
                #============DOUBLE_HALF
                if "pairing_double_half" in request_object:
                    response_obj.pairing_double_half_rated = double_point_five_rate(request_object["pairing_double_half"])
                    response_obj.pairing_double_half_pay = double_point_five_pay(request_object["pairing_double_half"])
                #============TRIPLE
                if "pairing_triple" in request_object:
                    response_obj.pairing_triple_rated = triple_rate(request_object["pairing_triple"])
                    response_obj.pairing_triple_pay = triple_pay(request_object["pairing_triple"])
                #============OVERRIDES
                response_obj.pairing_overrides_pay = override_pay(request_object["pairing_overrides"])
                #============A-POSITON
                if "pairing_a_hours" in request_object:
                    response_obj.pairing_a_pay = container_a_position_pay(request_object["pairing_a_hours"])
                #=============TAFB
                response_obj.tafb_pay = tafb_pay(request_object["tafb_total"])
                response_obj.int_tafb_pay = int_tafb_pay(request_object["int_tafb_total"])


                #===============Reserve Stuff 
                response_obj.reserve_block = request_object["reserve_block"]
                response_obj.pairing_reserve_no_fly_hours = request_object["pairing_reserve_no_fly_hours"]

                #===============Reserve GUARANTEE HOURS 
                if "reserve_block" in request_object:
                    day_count = Day.query.filter_by(pairing_id=response_obj.id).count()
                    if request_object["reserve_block"]:
                        response_obj.pairing_guarantee_hours = 6 * day_count
                    else:
                        response_obj.pairing_guarantee_hours = 0
                
                #===============Reserve  WORKED TOWARDS GUARANTEE  
                response_obj.pairing_guarantee_hours_worked_rated = totals(request_object["pairing_reserve_no_fly_hours"],
                request_object["pairing_tfp"],request_object["pairing_vacation_sick"],one_point_five_rate(request_object["pairing_vja"]),double_rate(request_object["pairing_holiday"]),one_point_five_rate(request_object["pairing_time_half"]),more_better_function_rate(request_object["pairing_double_time"],2),more_better_function_rate(request_object["pairing_double_half"],2.5),more_better_function_rate(request_object["pairing_triple"],3)) if request_object["reserve_block"] else 0



                # #============Totals ACTUAL 
                # response_obj.pairing_total_credits = totals(request_object["pairing_tfp"],request_object["pairing_vacation_sick"],request_object["pairing_vja"],request_object["pairing_holiday"],request_object["pairing_time_half"],request_object["pairing_double_time"],request_object["pairing_double_half"],request_object["pairing_triple"])
                # #============Totals RATED
                # response_obj.pairing_total_credits_rated= totals(request_object["pairing_tfp"],request_object["pairing_vacation_sick"],one_point_five_rate(request_object["pairing_vja"]),one_point_five_rate(request_object["pairing_holiday"]),one_point_five_rate(request_object["pairing_time_half"]),more_better_function_rate(request_object["pairing_double_time"],2),more_better_function_rate(request_object["pairing_double_half"],2.5),more_better_function_rate(request_object["pairing_triple"],3))
                # #============Totals PAY
                # response_obj.pairing_total_pay = totals(tfp_pay_function(request_object["pairing_tfp"]),tfp_pay_function(request_object["pairing_vacation_sick"]),one_point_five_pay(request_object["pairing_vja"]),one_point_five_pay(request_object["pairing_holiday"]),one_point_five_pay(request_object["pairing_time_half"]),more_better_function_pay(request_object["pairing_double_time"],2),more_better_function_pay(request_object["pairing_double_half"],2.5),more_better_function_pay(request_object["pairing_triple"],3), tafb_pay(request_object["tafb_total"]),int_tafb_pay(request_object["int_tafb_total"]),override_pay(request_object["pairing_overrides"]),container_a_position_pay(request_object["pairing_a_hours"]))
                # #=====================
                db.session.add(response_obj)
                db.session.commit()

                all_cascade_patch_pairing =Pairing.query.filter_by(month_id=response_obj.month_id)
                     #===============Reserve Stuff 
                sum_pairing_guarantee_hours = 0
                sum_pairing_guarantee_hours_worked_rated = 0
                #=============TAFB
                sum_tafb_total = 0
                sum_int_tafb_total = 0
                #============REGULAR TFP
                sum_pairing_tfp = 0
                #============VACATION/SICK
                sum_pairing_vacation_sick = 0
                #============VJA
                sum_pairing_vja = 0
                #============HOLIDAY
                sum_pairing_holiday = 0
                #============time_half
                sum_pairing_time_half = 0
                #================ DOUBLE TIME LYFE
                sum_pairing_double_time = 0
                #================ DOUBLE & HALF LYFE
                sum_pairing_double_half = 0
                #================ TRIPLE LYFE
                sum_pairing_triple = 0
                #================ OVERRIDES LYFE
                sum_pairing_overrides = 0
                #================ A-POSITION LYFE
                sum_pairing_a_hours = 0
                #============Totals
                sum_pairing_total_credits = 0
                #========New additions=======
                sum_pairing_duty_hours = 0
                sum_pairing_reserve_no_fly_hours =0

                for pairing in all_cascade_patch_pairing:
                    if pairing.pairing_guarantee_hours != None:
                        sum_pairing_guarantee_hours += pairing.pairing_guarantee_hours
                    if pairing.pairing_guarantee_hours_worked_rated != None:
                        sum_pairing_guarantee_hours_worked_rated += pairing.pairing_guarantee_hours_worked_rated
                    if pairing.tafb_total != None:
                        sum_tafb_total += pairing.tafb_total
                    if pairing.int_tafb_total != None:
                        sum_int_tafb_total += pairing.int_tafb_total
                    if pairing.pairing_tfp != None:
                        sum_pairing_tfp += pairing.pairing_tfp
                    if pairing.pairing_vacation_sick != None:
                        sum_pairing_vacation_sick += pairing.pairing_vacation_sick
                    if pairing.pairing_vja != None:
                        sum_pairing_vja += pairing.pairing_vja
                    if pairing.pairing_holiday != None:
                        sum_pairing_holiday += pairing.pairing_holiday
                    if pairing.pairing_time_half != None:
                        sum_pairing_time_half += pairing.pairing_time_half
                    if pairing.pairing_double_time != None:
                        sum_pairing_double_time += pairing.pairing_double_time
                    if pairing.pairing_double_half != None:
                        sum_pairing_double_half += pairing.pairing_double_half
                    if pairing.pairing_triple != None:
                        sum_pairing_triple += pairing.pairing_triple
                    if pairing.pairing_overrides != None:
                        sum_pairing_overrides += pairing.pairing_overrides
                    if pairing.pairing_a_hours != None:
                        sum_pairing_a_hours += pairing.pairing_a_hours
                    if pairing.pairing_total_credits != None:
                        sum_pairing_total_credits += pairing.pairing_total_credits
                    if pairing.pairing_duty_hours != None:
                        sum_pairing_duty_hours += pairing.pairing_duty_hours
                    if pairing.pairing_reserve_no_fly_hours != None:
                        sum_pairing_reserve_no_fly_hours += pairing.pairing_reserve_no_fly_hours

                cascade_patch_month = Month.query.filter_by(id=response_obj.month_id).first()

                #========New additions=======
                cascade_patch_month.month_duty_hours = sum_pairing_duty_hours
                #=============TAFB
                cascade_patch_month.month_tafb_total = sum_tafb_total
                cascade_patch_month.month_tafb_pay = tafb_pay(sum_tafb_total)
                #=============TAFB INT
                cascade_patch_month.month_int_tafb_total = sum_int_tafb_total
                cascade_patch_month.month_int_tafb_pay = int_tafb_pay(sum_int_tafb_total)
                #============VACATION/SICK
                cascade_patch_month.month_vacation_sick = sum_pairing_vacation_sick
                cascade_patch_month.month_vacation_sick_pay = tfp_pay_function(sum_pairing_vacation_sick)
                #============REGULAR TFP
                cascade_patch_month.month_tfp = sum_pairing_tfp
                cascade_patch_month.month_tfp_pay = tfp_pay_function(sum_pairing_tfp)
                #============VJA
                cascade_patch_month.month_vja = sum_pairing_vja
                cascade_patch_month.month_vja_rated= one_point_five_rate(sum_pairing_vja)
                cascade_patch_month.month_vja_pay= one_point_five_pay(sum_pairing_vja)
                # #============HOLIDAY
                cascade_patch_month.month_holiday = sum_pairing_holiday
                cascade_patch_month.month_holiday_rated= double_rate(sum_pairing_holiday)
                cascade_patch_month.month_holiday_pay= double_pay(sum_pairing_holiday)
                #============TIME_HALF
                cascade_patch_month.month_time_half = sum_pairing_time_half
                cascade_patch_month.month_time_half_rated= one_point_five_rate(sum_pairing_time_half)
                cascade_patch_month.month_time_half_pay= one_point_five_pay(sum_pairing_time_half)
                #============DOUBLE_TIME
                cascade_patch_month.month_double_time = sum_pairing_double_time
                cascade_patch_month.month_double_time_rated= more_better_function_rate(sum_pairing_double_time,2)
                cascade_patch_month.month_double_time_pay= more_better_function_pay(sum_pairing_double_time,2)
                #============DOUBLE_HALF
                cascade_patch_month.month_double_half = sum_pairing_double_half
                cascade_patch_month.month_double_half_rated= more_better_function_rate(sum_pairing_double_half,2.5)
                cascade_patch_month.month_double_half_pay= more_better_function_pay(sum_pairing_double_half,2.5)
                #============TRIPLE
                cascade_patch_month.month_triple = sum_pairing_triple
                cascade_patch_month.month_triple_rated= more_better_function_rate(sum_pairing_triple,3)
                cascade_patch_month.month_triple_pay= more_better_function_pay(sum_pairing_triple,3)
                #============OVERRIDES
                cascade_patch_month.month_overrides = sum_pairing_overrides
                cascade_patch_month.month_overrides_pay = override_pay(sum_pairing_overrides)
                #============A-POSITON
                cascade_patch_month.month_a_hours = sum_pairing_a_hours
                cascade_patch_month.month_a_pay = container_a_position_pay(sum_pairing_a_hours)
                # #===============Reserve NO FLY HOURS 
                cascade_patch_month.month_reserve_no_fly_hours = sum_pairing_reserve_no_fly_hours
                cascade_patch_month.month_reserve_no_fly_pay = tfp_pay_function(sum_pairing_reserve_no_fly_hours)
                # #===============Reserve GUARANTEE HOURS 
                cascade_patch_month.month_guarantee_hours = sum_pairing_guarantee_hours
                cascade_patch_month.month_guarantee_hours_worked_rated = sum_pairing_guarantee_hours_worked_rated
                #============Totals ACTUAL 
                cascade_patch_month.month_total_credits = totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,sum_pairing_vja,sum_pairing_holiday,sum_pairing_time_half,sum_pairing_double_time,sum_pairing_double_half,sum_pairing_triple)
                #============Totals RATED
                cascade_patch_month.month_total_credits_rated= totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,one_point_five_rate(sum_pairing_vja),double_rate(sum_pairing_holiday),one_point_five_rate(sum_pairing_time_half),more_better_function_rate(sum_pairing_double_time,2),more_better_function_rate(sum_pairing_double_half,2.5),more_better_function_rate(sum_pairing_triple,3))
                #============Totals PAY
                cascade_patch_month.month_total_pay = totals(tfp_pay_function(sum_pairing_reserve_no_fly_hours),tfp_pay_function(sum_pairing_tfp),tfp_pay_function(sum_pairing_vacation_sick),one_point_five_pay(sum_pairing_vja),double_pay(sum_pairing_holiday),one_point_five_pay(sum_pairing_time_half),more_better_function_pay(sum_pairing_double_time,2),more_better_function_pay(sum_pairing_double_half,2.5),more_better_function_pay(sum_pairing_triple,3), tafb_pay(sum_tafb_total),int_tafb_pay(sum_int_tafb_total),override_pay(sum_pairing_overrides),container_a_position_pay(sum_pairing_a_hours))
                    # #=====================
                db.session.add(cascade_patch_month)
                db.session.commit()
              
                # THIS IS THE QUERY FOR ALL RELATED MONTHS
                all_cascade_patch_month = Month.query.filter_by(year_id=cascade_patch_month.year_id)
                #========New additions=======
                sum_month_duty_hours = 0
                #=============TAFB
                sum_month_tafb_total = 0
                sum_month_int_tafb_total = 0
                #============REGULAR TFP
                sum_month_tfp = 0
                #============VACATION/SICK
                sum_month_vacation_sick = 0
                #============VJA
                sum_month_vja = 0
                #============HOLIDAY
                sum_month_holiday = 0
                #============time_half
                sum_month_time_half = 0
                #================ DOUBLE TIME LYFE
                sum_month_double_time = 0
                #================ DOUBLE & HALF LYFE
                sum_month_double_half = 0
                #================ TRIPLE LYFE
                sum_month_triple = 0
                #================ OVERRIDES LYFE
                sum_month_overrides = 0
                #================ A-POSITION LYFE
                sum_month_a_hours = 0
                #============Totals
                sum_month_total_credits = 0
                #========Reserve No Fly=======
                sum_month_reserve_no_fly_hours = 0

                #HERE WILL BE A LINE OF FOR/INS THAT WILL TOTAL EACH CAT FOR THE YEAR
                for month in all_cascade_patch_month:
                    # if month.month_guarantee_hours != None:
                    #     sum_month_guarantee_hours += month.month_guarantee_hours
                    # if month.month_guarantee_hours_worked_rated != None:
                    #     sum_month_guarantee_hours_worked_rated += month.month_guarantee_hours_worked_rated
                    if month.month_tafb_total != None:
                        sum_month_tafb_total += month.month_tafb_total
                    if month.month_int_tafb_total != None:
                        sum_month_int_tafb_total += month.month_int_tafb_total
                    if month.month_tfp != None:
                        sum_month_tfp += month.month_tfp
                    if month.month_vacation_sick != None:
                        sum_month_vacation_sick += month.month_vacation_sick
                    if month.month_vja != None:
                        sum_month_vja += month.month_vja
                    if month.month_holiday != None:
                        sum_month_holiday += month.month_holiday
                    if month.month_time_half != None:
                        sum_month_time_half += month.month_time_half
                    if month.month_double_time != None:
                        sum_month_double_time += month.month_double_time
                    if month.month_double_half != None:
                        sum_month_double_half += month.month_double_half
                    if month.month_triple != None:
                        sum_month_triple += month.month_triple
                    if month.month_overrides != None:
                        sum_month_overrides += month.month_overrides
                    if month.month_a_hours != None:
                        sum_month_a_hours += month.month_a_hours
                    if month.month_total_credits != None:
                        sum_month_total_credits += month.month_total_credits
                    if month.month_duty_hours != None:
                        sum_month_duty_hours += month.month_duty_hours
                    if month.month_reserve_no_fly_hours != None:
                        sum_month_reserve_no_fly_hours += month.month_reserve_no_fly_hours

                    #THIS IS THE QUERY FOR THE YEAR WE'RE UPDATING WITH THE MONTHLY TOTALS 
                    cascade_patch_year = Year.query.filter_by(id=cascade_patch_month.year_id).first()
                    #THIS WILL BE LINES WHERE WE ASSIGN VALUE TO YEAR CATS WITH MONTHLY TOTALS
                    #========New additions=======
                    cascade_patch_year.year_duty_hours = sum_month_duty_hours
                    #=============TAFB
                    cascade_patch_year.year_tafb_total = sum_month_tafb_total
                    cascade_patch_year.year_tafb_pay = tafb_pay(sum_month_tafb_total)
                    #=============TAFB INT
                    cascade_patch_year.year_int_tafb = sum_month_int_tafb_total
                    cascade_patch_year.year_int_tafb_pay = int_tafb_pay(sum_month_int_tafb_total)
                    #============VACATION/SICK
                    cascade_patch_year.year_vacation_sick = sum_month_vacation_sick
                    cascade_patch_year.year_vacation_sick_pay = tfp_pay_function(sum_month_vacation_sick)
                    #============REGULAR TFP
                    cascade_patch_year.year_tfp = sum_month_tfp
                    cascade_patch_year.year_tfp_pay = tfp_pay_function(sum_month_tfp)
                    #============VJA
                    cascade_patch_year.year_vja = sum_month_vja
                    cascade_patch_year.year_vja_rated= one_point_five_rate(sum_month_vja)
                    cascade_patch_year.year_vja_pay= one_point_five_pay(sum_month_vja)
                    # #============HOLIDAY
                    cascade_patch_year.year_holiday = sum_month_holiday
                    cascade_patch_year.year_holiday_rated= double_rate(sum_month_holiday)
                    cascade_patch_year.year_holiday_pay= double_pay(sum_month_holiday)
                    #============TIME_HALF
                    cascade_patch_year.year_time_half = sum_month_time_half
                    cascade_patch_year.year_time_half_rated= one_point_five_rate(sum_month_time_half)
                    cascade_patch_year.year_time_half_pay= one_point_five_pay(sum_month_time_half)
                    #============DOUBLE_TIME
                    cascade_patch_year.year_double_time = sum_month_double_time
                    cascade_patch_year.year_double_time_rated= more_better_function_rate(sum_month_double_time,2)
                    cascade_patch_year.year_double_time_pay= more_better_function_pay(sum_month_double_time,2)
                    #============DOUBLE_HALF
                    cascade_patch_year.year_double_half = sum_month_double_half
                    cascade_patch_year.year_double_half_rated= more_better_function_rate(sum_month_double_half,2.5)
                    cascade_patch_year.year_double_half_pay= more_better_function_pay(sum_month_double_half,2.5)
                    #============TRIPLE
                    cascade_patch_year.year_triple = sum_month_triple
                    cascade_patch_year.year_triple_rated= more_better_function_rate(sum_month_triple,3)
                    cascade_patch_year.year_triple_pay= more_better_function_pay(sum_month_triple,3)
                    #============OVERRIDES
                    cascade_patch_year.year_overrides = sum_month_overrides
                    cascade_patch_year.year_overrides_pay = override_pay(sum_month_overrides)
                    #============A-POSITON
                    cascade_patch_year.year_a_hours = sum_month_a_hours
                    cascade_patch_year.year_a_pay = container_a_position_pay(sum_month_a_hours)
                    # # #===============Reserve Nofly HOURS 
                    cascade_patch_year.year_reserve_no_fly_hours = sum_month_reserve_no_fly_hours
                    cascade_patch_year.year_reserve_no_fly_pay = tfp_pay_function(sum_month_reserve_no_fly_hours)
                    # cascade_patch_year.year_guarantee_hours = sum_month_guarantee_hours
                    # cascade_patch_year.year_guarantee_hours_worked_rated = sum_month_guarantee_hours_worked_rated
                    #============Totals ACTUAL 
                    cascade_patch_year.year_total_credits = totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,sum_month_vja,sum_month_holiday,sum_month_time_half,sum_month_double_time,sum_month_double_half,sum_month_triple)
                    #============Totals RATED
                    cascade_patch_year.year_total_credits_rated= totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,one_point_five_rate(sum_month_vja),double_rate(sum_month_holiday),one_point_five_rate(sum_month_time_half),more_better_function_rate(sum_month_double_time,2),more_better_function_rate(sum_month_double_half,2.5),more_better_function_rate(sum_month_triple,3))
                    #============Totals PAY
                    cascade_patch_year.year_total_pay = totals(tfp_pay_function(sum_month_reserve_no_fly_hours),tfp_pay_function(sum_month_tfp),tfp_pay_function(sum_month_vacation_sick),one_point_five_pay(sum_month_vja),double_pay(sum_month_holiday),one_point_five_pay(sum_month_time_half),more_better_function_pay(sum_month_double_time,2),more_better_function_pay(sum_month_double_half,2.5),more_better_function_pay(sum_month_triple,3), tafb_pay(sum_month_tafb_total),int_tafb_pay(sum_month_int_tafb_total),override_pay(sum_month_overrides),container_a_position_pay(sum_month_a_hours))
                    # #=====================
                    db.session.add(cascade_patch_year)
                    db.session.commit()

            except Exception as e:
                message = {'errors': [e.__str__()]}
                return make_response(message, 422)
            return make_response(response_obj.to_dict(), 200)
    def delete(self, id):
        response_obj = Pairing.query.filter_by(id=id).first()
        if response_obj == None: 
            response_dict = {
                "error": "Pairing not found"
            }
            return make_response(response_dict, 404)
        else:
            id_to_use = response_obj.month_id
            db.session.delete(response_obj)
            db.session.commit()

            all_cascade_patch_pairing =Pairing.query.filter_by(month_id=id_to_use)
            #===============Reserve Stuff 
            sum_pairing_guarantee_hours = 0
            sum_pairing_guarantee_hours_worked_rated = 0
            #=============TAFB
            sum_tafb_total = 0
            sum_int_tafb_total = 0
            #============REGULAR TFP
            sum_pairing_tfp = 0
            #============VACATION/SICK
            sum_pairing_vacation_sick = 0
            #============VJA
            sum_pairing_vja = 0
            #============HOLIDAY
            sum_pairing_holiday = 0
            #============time_half
            sum_pairing_time_half = 0
            #================ DOUBLE TIME LYFE
            sum_pairing_double_time = 0
            #================ DOUBLE & HALF LYFE
            sum_pairing_double_half = 0
            #================ TRIPLE LYFE
            sum_pairing_triple = 0
            #================ OVERRIDES LYFE
            sum_pairing_overrides = 0
            #================ A-POSITION LYFE
            sum_pairing_a_hours = 0
            #============Totals
            sum_pairing_total_credits = 0
            #========New additions=======
            sum_pairing_duty_hours = 0
            sum_pairing_reserve_no_fly_hours =0

            for pairing in all_cascade_patch_pairing:
                if pairing.pairing_guarantee_hours != None:
                    sum_pairing_guarantee_hours += pairing.pairing_guarantee_hours
                if pairing.pairing_guarantee_hours_worked_rated != None:
                    sum_pairing_guarantee_hours_worked_rated += pairing.pairing_guarantee_hours_worked_rated
                if pairing.tafb_total != None:
                    sum_tafb_total += pairing.tafb_total
                if pairing.int_tafb_total != None:
                    sum_int_tafb_total += pairing.int_tafb_total
                if pairing.pairing_tfp != None:
                    sum_pairing_tfp += pairing.pairing_tfp
                if pairing.pairing_vacation_sick != None:
                    sum_pairing_vacation_sick += pairing.pairing_vacation_sick
                if pairing.pairing_vja != None:
                    sum_pairing_vja += pairing.pairing_vja
                if pairing.pairing_holiday != None:
                    sum_pairing_holiday += pairing.pairing_holiday
                if pairing.pairing_time_half != None:
                    sum_pairing_time_half += pairing.pairing_time_half
                if pairing.pairing_double_time != None:
                    sum_pairing_double_time += pairing.pairing_double_time
                if pairing.pairing_double_half != None:
                    sum_pairing_double_half += pairing.pairing_double_half
                if pairing.pairing_triple != None:
                    sum_pairing_triple += pairing.pairing_triple
                if pairing.pairing_overrides != None:
                    sum_pairing_overrides += pairing.pairing_overrides
                if pairing.pairing_a_hours != None:
                    sum_pairing_a_hours += pairing.pairing_a_hours
                if pairing.pairing_total_credits != None:
                    sum_pairing_total_credits += pairing.pairing_total_credits
                if pairing.pairing_duty_hours != None:
                    sum_pairing_duty_hours += pairing.pairing_duty_hours
                if pairing.pairing_reserve_no_fly_hours != None:
                    sum_pairing_reserve_no_fly_hours += pairing.pairing_reserve_no_fly_hours

            cascade_patch_month = Month.query.filter_by(id=id_to_use).first()
            #========New additions=======
            cascade_patch_month.month_duty_hours = sum_pairing_duty_hours
            #=============TAFB
            cascade_patch_month.month_tafb_total = sum_tafb_total
            cascade_patch_month.month_tafb_pay = tafb_pay(sum_tafb_total)
            #=============TAFB INT
            cascade_patch_month.month_int_tafb_total = sum_int_tafb_total
            cascade_patch_month.month_int_tafb_pay = int_tafb_pay(sum_int_tafb_total)
            #============VACATION/SICK
            cascade_patch_month.month_vacation_sick = sum_pairing_vacation_sick
            cascade_patch_month.month_vacation_sick_pay = tfp_pay_function(sum_pairing_vacation_sick)
            #============REGULAR TFP
            cascade_patch_month.month_tfp = sum_pairing_tfp
            cascade_patch_month.month_tfp_pay = tfp_pay_function(sum_pairing_tfp)
            #============VJA
            cascade_patch_month.month_vja = sum_pairing_vja
            cascade_patch_month.month_vja_rated= one_point_five_rate(sum_pairing_vja)
            cascade_patch_month.month_vja_pay= one_point_five_pay(sum_pairing_vja)
            # #============HOLIDAY
            cascade_patch_month.month_holiday = sum_pairing_holiday
            cascade_patch_month.month_holiday_rated= double_rate(sum_pairing_holiday)
            cascade_patch_month.month_holiday_pay= double_pay(sum_pairing_holiday)
            #============TIME_HALF
            cascade_patch_month.month_time_half = sum_pairing_time_half
            cascade_patch_month.month_time_half_rated= one_point_five_rate(sum_pairing_time_half)
            cascade_patch_month.month_time_half_pay= one_point_five_pay(sum_pairing_time_half)
            #============DOUBLE_TIME
            cascade_patch_month.month_double_time = sum_pairing_double_time
            cascade_patch_month.month_double_time_rated= more_better_function_rate(sum_pairing_double_time,2)
            cascade_patch_month.month_double_time_pay= more_better_function_pay(sum_pairing_double_time,2)
            #============DOUBLE_HALF
            cascade_patch_month.month_double_half = sum_pairing_double_half
            cascade_patch_month.month_double_half_rated= more_better_function_rate(sum_pairing_double_half,2.5)
            cascade_patch_month.month_double_half_pay= more_better_function_pay(sum_pairing_double_half,2.5)
            #============TRIPLE
            cascade_patch_month.month_triple = sum_pairing_triple
            cascade_patch_month.month_triple_rated= more_better_function_rate(sum_pairing_triple,3)
            cascade_patch_month.month_triple_pay= more_better_function_pay(sum_pairing_triple,3)
            #============OVERRIDES
            cascade_patch_month.month_overrides = sum_pairing_overrides
            cascade_patch_month.month_overrides_pay = override_pay(sum_pairing_overrides)
            #============A-POSITON
            cascade_patch_month.month_a_hours = sum_pairing_a_hours
            cascade_patch_month.month_a_pay = container_a_position_pay(sum_pairing_a_hours)
            # #===============Reserve NO FLY HOURS 
            cascade_patch_month.month_reserve_no_fly_hours = sum_pairing_reserve_no_fly_hours
            cascade_patch_month.month_reserve_no_fly_pay = tfp_pay_function(sum_pairing_reserve_no_fly_hours)
            # #===============Reserve GUARANTEE HOURS 
            cascade_patch_month.month_guarantee_hours = sum_pairing_guarantee_hours
            cascade_patch_month.month_guarantee_hours_worked_rated = sum_pairing_guarantee_hours_worked_rated
            #============Totals ACTUAL 
            cascade_patch_month.month_total_credits = totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,sum_pairing_vja,sum_pairing_holiday,sum_pairing_time_half,sum_pairing_double_time,sum_pairing_double_half,sum_pairing_triple)
            #============Totals RATED
            cascade_patch_month.month_total_credits_rated= totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,one_point_five_rate(sum_pairing_vja),double_rate(sum_pairing_holiday),one_point_five_rate(sum_pairing_time_half),more_better_function_rate(sum_pairing_double_time,2),more_better_function_rate(sum_pairing_double_half,2.5),more_better_function_rate(sum_pairing_triple,3))
            #============Totals PAY
            cascade_patch_month.month_total_pay = totals(tfp_pay_function(sum_pairing_reserve_no_fly_hours),tfp_pay_function(sum_pairing_tfp),tfp_pay_function(sum_pairing_vacation_sick),one_point_five_pay(sum_pairing_vja),double_pay(sum_pairing_holiday),one_point_five_pay(sum_pairing_time_half),more_better_function_pay(sum_pairing_double_time,2),more_better_function_pay(sum_pairing_double_half,2.5),more_better_function_pay(sum_pairing_triple,3), tafb_pay(sum_tafb_total),int_tafb_pay(sum_int_tafb_total),override_pay(sum_pairing_overrides),container_a_position_pay(sum_pairing_a_hours))
            # #=====================
            db.session.add(cascade_patch_month)
            db.session.commit()
            # THIS IS THE QUERY FOR ALL RELATED MONTHS
            all_cascade_patch_month = Month.query.filter_by(year_id=cascade_patch_month.year_id)
            #========New additions=======
            sum_month_duty_hours = 0
            #=============TAFB
            sum_month_tafb_total = 0
            sum_month_int_tafb_total = 0
            #============REGULAR TFP
            sum_month_tfp = 0
            #============VACATION/SICK
            sum_month_vacation_sick = 0
            #============VJA
            sum_month_vja = 0
            #============HOLIDAY
            sum_month_holiday = 0
            #============time_half
            sum_month_time_half = 0
            #================ DOUBLE TIME LYFE
            sum_month_double_time = 0
            #================ DOUBLE & HALF LYFE
            sum_month_double_half = 0
            #================ TRIPLE LYFE
            sum_month_triple = 0
            #================ OVERRIDES LYFE
            sum_month_overrides = 0
            #================ A-POSITION LYFE
            sum_month_a_hours = 0
            #============Totals
            sum_month_total_credits = 0
            #========Reserve No Fly=======
            sum_month_reserve_no_fly_hours = 0

            #HERE WILL BE A LINE OF FOR/INS THAT WILL TOTAL EACH CAT FOR THE YEAR
            for month in all_cascade_patch_month:
                # if month.month_guarantee_hours != None:
                #     sum_month_guarantee_hours += month.month_guarantee_hours
                # if month.month_guarantee_hours_worked_rated != None:
                #     sum_month_guarantee_hours_worked_rated += month.month_guarantee_hours_worked_rated
                if month.month_tafb_total != None:
                    sum_month_tafb_total += month.month_tafb_total
                if month.month_int_tafb_total != None:
                    sum_month_int_tafb_total += month.month_int_tafb_total
                if month.month_tfp != None:
                    sum_month_tfp += month.month_tfp
                if month.month_vacation_sick != None:
                    sum_month_vacation_sick += month.month_vacation_sick
                if month.month_vja != None:
                    sum_month_vja += month.month_vja
                if month.month_holiday != None:
                    sum_month_holiday += month.month_holiday
                if month.month_time_half != None:
                    sum_month_time_half += month.month_time_half
                if month.month_double_time != None:
                    sum_month_double_time += month.month_double_time
                if month.month_double_half != None:
                    sum_month_double_half += month.month_double_half
                if month.month_triple != None:
                    sum_month_triple += month.month_triple
                if month.month_overrides != None:
                    sum_month_overrides += month.month_overrides
                if month.month_a_hours != None:
                    sum_month_a_hours += month.month_a_hours
                if month.month_total_credits != None:
                    sum_month_total_credits += month.month_total_credits
                if month.month_duty_hours != None:
                    sum_month_duty_hours += month.month_duty_hours
                if month.month_reserve_no_fly_hours != None:
                    sum_month_reserve_no_fly_hours += month.month_reserve_no_fly_hours

                #THIS IS THE QUERY FOR THE YEAR WE'RE UPDATING WITH THE MONTHLY TOTALS 
                cascade_patch_year = Year.query.filter_by(id=cascade_patch_month.year_id).first()
                #THIS WILL BE LINES WHERE WE ASSIGN VALUE TO YEAR CATS WITH MONTHLY TOTALS
                #========New additions=======
                cascade_patch_year.year_duty_hours = sum_month_duty_hours
                #=============TAFB
                cascade_patch_year.year_tafb_total = sum_month_tafb_total
                cascade_patch_year.year_tafb_pay = tafb_pay(sum_month_tafb_total)
                #=============TAFB INT
                cascade_patch_year.year_int_tafb = sum_month_int_tafb_total
                cascade_patch_year.year_int_tafb_pay = int_tafb_pay(sum_month_int_tafb_total)
                #============VACATION/SICK
                cascade_patch_year.year_vacation_sick = sum_month_vacation_sick
                cascade_patch_year.year_vacation_sick_pay = tfp_pay_function(sum_month_vacation_sick)
                #============REGULAR TFP
                cascade_patch_year.year_tfp = sum_month_tfp
                cascade_patch_year.year_tfp_pay = tfp_pay_function(sum_month_tfp)
                #============VJA
                cascade_patch_year.year_vja = sum_month_vja
                cascade_patch_year.year_vja_rated= one_point_five_rate(sum_month_vja)
                cascade_patch_year.year_vja_pay= one_point_five_pay(sum_month_vja)
                # #============HOLIDAY
                cascade_patch_year.year_holiday = sum_month_holiday
                cascade_patch_year.year_holiday_rated= double_rate(sum_month_holiday)
                cascade_patch_year.year_holiday_pay= double_pay(sum_month_holiday)
                #============TIME_HALF
                cascade_patch_year.year_time_half = sum_month_time_half
                cascade_patch_year.year_time_half_rated= one_point_five_rate(sum_month_time_half)
                cascade_patch_year.year_time_half_pay= one_point_five_pay(sum_month_time_half)
                #============DOUBLE_TIME
                cascade_patch_year.year_double_time = sum_month_double_time
                cascade_patch_year.year_double_time_rated= more_better_function_rate(sum_month_double_time,2)
                cascade_patch_year.year_double_time_pay= more_better_function_pay(sum_month_double_time,2)
                #============DOUBLE_HALF
                cascade_patch_year.year_double_half = sum_month_double_half
                cascade_patch_year.year_double_half_rated= more_better_function_rate(sum_month_double_half,2.5)
                cascade_patch_year.year_double_half_pay= more_better_function_pay(sum_month_double_half,2.5)
                #============TRIPLE
                cascade_patch_year.year_triple = sum_month_triple
                cascade_patch_year.year_triple_rated= more_better_function_rate(sum_month_triple,3)
                cascade_patch_year.year_triple_pay= more_better_function_pay(sum_month_triple,3)
                #============OVERRIDES
                cascade_patch_year.year_overrides = sum_month_overrides
                cascade_patch_year.year_overrides_pay = override_pay(sum_month_overrides)
                #============A-POSITON
                cascade_patch_year.year_a_hours = sum_month_a_hours
                cascade_patch_year.year_a_pay = container_a_position_pay(sum_month_a_hours)
                # # #===============Reserve Nofly HOURS 
                cascade_patch_year.year_reserve_no_fly_hours = sum_month_reserve_no_fly_hours
                cascade_patch_year.year_reserve_no_fly_pay = tfp_pay_function(sum_month_reserve_no_fly_hours)
                # cascade_patch_year.year_guarantee_hours = sum_month_guarantee_hours
                # cascade_patch_year.year_guarantee_hours_worked_rated = sum_month_guarantee_hours_worked_rated
                #============Totals ACTUAL 
                cascade_patch_year.year_total_credits = totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,sum_month_vja,sum_month_holiday,sum_month_time_half,sum_month_double_time,sum_month_double_half,sum_month_triple)
                #============Totals RATED
                cascade_patch_year.year_total_credits_rated= totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,one_point_five_rate(sum_month_vja),double_rate(sum_month_holiday),one_point_five_rate(sum_month_time_half),more_better_function_rate(sum_month_double_time,2),more_better_function_rate(sum_month_double_half,2.5),more_better_function_rate(sum_month_triple,3))
                #============Totals PAY
                cascade_patch_year.year_total_pay = totals(tfp_pay_function(sum_month_reserve_no_fly_hours),tfp_pay_function(sum_month_tfp),tfp_pay_function(sum_month_vacation_sick),one_point_five_pay(sum_month_vja),double_pay(sum_month_holiday),one_point_five_pay(sum_month_time_half),more_better_function_pay(sum_month_double_time,2),more_better_function_pay(sum_month_double_half,2.5),more_better_function_pay(sum_month_triple,3), tafb_pay(sum_month_tafb_total),int_tafb_pay(sum_month_int_tafb_total),override_pay(sum_month_overrides),container_a_position_pay(sum_month_a_hours))
                # #=====================
                db.session.add(cascade_patch_year)
                db.session.commit()
            response_dict = {"message": "deleted fo sho!"}
            return response_dict, 200
api.add_resource(PairingsById, '/pairings/<int:id>')



class Days(Resource):
    def get(self):
        days =[d.to_dict() for d in Day.query.all()]
        return make_response(days, 200)
    def post(self):
        request_obj = request.get_json()
        try:
            new_day = Day(
                date = request_obj["date"],
                #============REGULAR TFP
                total_tfp = request_obj["total_tfp"],
                total_tfp_pay = tfp_pay_function(request_obj["total_tfp"]),
                #============VACATION/SICK
                vacation_sick = request_obj["vacation_sick"],
                vacation_sick_pay = tfp_pay_function(request_obj["vacation_sick"]),
                #============VJA
                vja = request_obj["vja"],
                vja_rated= one_point_five_rate(request_obj["vja"]),
                vja_pay= one_point_five_pay(request_obj["vja"]),
                #============HOLIDAY
                holiday = request_obj["holiday"],
                holiday_rated = double_rate(request_obj["holiday"]),
                holiday_pay = double_pay(request_obj["holiday"]),
                #============TIME_HALF
                time_half = request_obj["time_half"],
                time_half_rated  = one_point_five_rate(request_obj["time_half"]),
                time_half_pay = one_point_five_pay(request_obj["time_half"]),
                #============DOUBLE_TIME
                double_time = request_obj["double_time"],
                double_time_rated = double_rate(request_obj["double_time"]),
                double_time_pay = double_pay(request_obj["double_time"]),
                #============DOUBLE_HALF
                double_half = request_obj["double_half"],
                double_half_rated = double_point_five_rate(request_obj["double_half"]),
                double_half_pay = double_point_five_pay(request_obj["double_half"]),
                #============TRIPLE
                triple = request_obj["triple"],
                triple_rated = triple_rate(request_obj["triple"]),
                triple_pay = triple_pay(request_obj["triple"]),
                #============OVERRIDES
                overrides = request_obj["overrides"],
                overrides_pay = override_pay(request_obj["overrides"]),
                #============A-POSITON
                a_position = request_obj["a_position"],


                a_hours = totals(request_obj["total_tfp"],request_obj["vacation_sick"],request_obj["vja"],request_obj["holiday"],request_obj["time_half"],request_obj["double_time"],request_obj["double_half"],request_obj["triple"]) if request_obj["a_position"] else 0,

                
                a_pay = a_position_pay(request_obj["a_position"],totals(request_obj["total_tfp"],request_obj["vacation_sick"],request_obj["vja"],request_obj["holiday"],request_obj["time_half"],request_obj["double_time"],request_obj["double_half"],request_obj["triple"])),
                 #============Totals ACTUAL 
                total_credits = totals(request_obj["total_tfp"],request_obj["vacation_sick"],request_obj["vja"],request_obj["holiday"],request_obj["time_half"],request_obj["double_time"],request_obj["double_half"],request_obj["triple"]),
                 #============Totals RATED
                total_credits_rated = totals(request_obj["total_tfp"],request_obj["vacation_sick"],one_point_five_rate(request_obj["vja"]),double_rate(request_obj["holiday"]),one_point_five_rate(request_obj["time_half"]),double_rate(request_obj["double_time"]),double_point_five_rate(request_obj["double_half"]),triple_rate(request_obj["triple"])),
                 #============Totals PAY
                total_pay = totals(tfp_pay_function(request_obj["total_tfp"]),tfp_pay_function(request_obj["vacation_sick"]),one_point_five_pay(request_obj["vja"]),one_point_five_pay(request_obj["holiday"]),one_point_five_pay(request_obj["time_half"]),double_pay(request_obj["double_time"]),double_point_five_pay(request_obj["double_half"]),triple_pay(request_obj["triple"]),override_pay(request_obj["overrides"]),a_position_pay(request_obj["a_position"],totals(request_obj["total_tfp"],request_obj["vacation_sick"],request_obj["vja"],request_obj["holiday"],request_obj["time_half"],request_obj["double_time"],request_obj["double_half"],request_obj["triple"]))),

                daily_duty_hours = request_obj["daily_duty_hours"],

                reserve_no_fly = request_obj["reserve_no_fly"],
                pairing_id = request_obj["pairing_id"],

                comments = request_obj["comments"],
                type_of_day =  request_obj["type_of_day"],

                
            )
            # total = tfp_pay_function(request_obj["total_tfp"])
            db.session.add(new_day)
            db.session.commit()
        except Exception as e:
            message = {'errors': [e.__str__()]}
            return make_response(message, 422)
        return make_response(new_day.to_dict(),200)
api.add_resource(Days, '/days')

class DaysById(Resource):
    def get(self, id):
        response_obj = Day.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Day not found'
            }
            return make_response(response_dict, 404)
        else:
            return make_response(response_obj.to_dict(), 200)
    def patch(self,id):
        response_obj = Day.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Day not found'
            }
            return make_response(response_dict, 404)
        else:
            request_object = request.get_json()
            try:
                keys_to_exclude = [
                                "vja_rated",
                                "vja_pay",
                                "holiday_rated",
                                "holiday_pay",
                                "time_half_rated",
                                "time_half_pay",
                                "double_time_rated",
                                "double_time_pay",
                                "double_half_rated",
                                "double_half_pay",
                                "triple_rated",
                                "triple_pay",
                                "overrides_pay",
                                "a_hours",
                                "a_pay",
                                "total_credits",
                                "total_credits_rated",
                                "total_pay"
                                ]
                for attr in request_object:
                    if attr not in keys_to_exclude:
                        setattr(response_obj, attr, request_object[attr])
                #============VACATION/SICK
                if "vacation_sick" in request_object:
                    response_obj.vacation_sick_pay = tfp_pay_function(request_object["vacation_sick"])
                #============REGULAR TFP
                if "total_tfp" in request_object:
                    response_obj.total_tfp_pay = tfp_pay_function(request_object["total_tfp"])
                #============VJA
                if "vja" in request_object:
                    response_obj.vja_rated = one_point_five_rate(request_object["vja"])
                    response_obj.vja_pay = one_point_five_pay(request_object["vja"])
                #============HOLIDAY
                if "holiday" in request_object:
                    response_obj.holiday_rated = double_rate(request_object["holiday"])
                    response_obj.holiday_pay = double_pay(request_object["holiday"])
                    # request_object["holiday"] = response_obj.holiday  # Add this line
                #============TIME_HALF
                if "time_half" in request_object:
                    response_obj.time_half_rated  = one_point_five_rate(request_object["time_half"])
                    response_obj.time_half_pay = one_point_five_pay(request_object["time_half"])
                #============DOUBLE_TIME
                if "double_time" in request_object:
                    response_obj.double_time_rated = double_rate(request_object["double_time"])
                    response_obj.double_time_pay = double_pay(request_object["double_time"])
                #============DOUBLE_HALF
                if "double_half" in request_object:
                    response_obj.double_half_rated = double_point_five_rate(request_object["double_half"])
                    response_obj.double_half_pay = double_point_five_pay(request_object["double_half"])
                #============TRIPLE
                if "triple" in request_object:
                    response_obj.triple_rated = triple_rate(request_object["triple"])
                    response_obj.triple_pay = triple_pay(request_object["triple"])
                #============OVERRIDES
                response_obj.overrides_pay = override_pay(request_object["overrides"])
                #============A-POSITON
                response_obj.a_position = request_object["a_position"]

                response_obj.a_hours = totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"]) if request_object["a_position"] else 0
                
                response_obj.a_pay = a_position_pay(request_object["a_position"],totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"]))
                # #========New additions=======
                # response_obj.reserve_no_fly = request_object["reserve_no_fly"]
                # response_obj.total_tfp = request_object["total_tfp"] + 6 if request_object["reserve_no_fly"] else request_object["total_tfp"]


                #============Totals ACTUAL 
                response_obj.total_credits = totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"])
                # request_object["total_credits"] = response_obj.total_credits  # Add this line
                #============Totals RATED
                response_obj.total_credits_rated = totals(request_object["total_tfp"],request_object["vacation_sick"],one_point_five_rate(request_object["vja"]),double_rate(request_object["holiday"]),one_point_five_rate(request_object["time_half"]),double_rate(request_object["double_time"]),double_point_five_rate(request_object["double_half"]),triple_rate(request_object["triple"]))
                # request_object["total_credits_rated"] = response_obj.total_credits_rated  # Add this line
                #============Totals PAY
                response_obj.total_pay = totals(tfp_pay_function(request_object["total_tfp"]),tfp_pay_function(request_object["vacation_sick"]),one_point_five_pay(request_object["vja"]),double_pay(request_object["holiday"]),one_point_five_pay(request_object["time_half"]),double_pay(request_object["double_time"]),double_point_five_pay(request_object["double_half"]),triple_pay(request_object["triple"]),override_pay(request_object["overrides"]),a_position_pay(request_object["a_position"],totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"])))
                # request_object["total_pay"] = response_obj.total_pay  # Add this line
                db.session.add(response_obj)
                db.session.commit()
# region BRUH.....
# #==============CASCADE PATCH STUFF=====================================
#                 all_days = Day.query.filter_by(pairing_id=response_obj.pairing_id)
#                 #============REGULAR TFP
#                 sum_total_tfp = 0
#                 #============VACATION/SICK
#                 sum_vacation_sick = 0
#                 #============VJA
#                 sum_vja = 0
#                 #============HOLIDAY
#                 sum_holiday = 0
#                 #============time_half
#                 sum_time_half = 0
#                 #================ DOUBLE TIME LYFE
#                 sum_double_time = 0
#                 #================ DOUBLE & HALF LYFE
#                 sum_double_half = 0
#                 #================ TRIPLE LYFE
#                 sum_triple = 0
#                 #================ OVERRIDES LYFE
#                 sum_overrides = 0
#                 #================ A-POSITION LYFE
#                 sum_a_hours = 0
#                 #============Totals
#                 sum_total_credits = 0
#                 #========New additions=======
#                 sum_daily_duty_hours = 0

#                 for days in all_days:
#                     if days.total_tfp != None:
#                         sum_total_tfp += days.total_tfp
#                     if days.vacation_sick != None:
#                         sum_vacation_sick += days.vacation_sick
#                     if days.vja != None:
#                         sum_vja += days.vja
#                     if days.holiday != None:
#                         sum_holiday += days.holiday
#                     if days.time_half != None:
#                         sum_time_half += days.time_half
#                     if days.double_time != None:
#                         sum_double_time += days.double_time
#                     if days.double_half != None:
#                         sum_double_half += days.double_half
#                     if days.triple != None:
#                         sum_triple += days.triple
#                     if days.overrides != None:
#                         sum_overrides += days.overrides
#                     if days.a_hours != None:
#                         sum_a_hours += days.a_hours
#                     if days.total_credits != None:
#                         sum_total_credits += days.total_credits
#                     if days.daily_duty_hours != None:
#                         sum_daily_duty_hours += days.daily_duty_hours
                    
# # region differnet approach

#                 #=========shitty idea

#                 # pairing_id = response_obj.pairing_id  
#                 # pairing_payload = {
#                 #     'pairing_tfp': sum_total_tfp, 
#                 #     'pairing_vacation_sick': sum_vacation_sick,  
#                 #     'pairing_vja': sum_vja, 
#                 #     'pairing_holiday': sum_holiday  
#                 # }

#                 # # Make the patch request to update the 'cascade_patch_pairing' object
#                 # url = f'http://127.0.0.1:5555/pairings/{pairing_id}'
#                 # pairing_response = requests.patch(url, json=pairing_payload)

#                 # # Handle response and error cases for the 'cascade_patch_pairing' patch request
#                 # if pairing_response.status_code == 200:
#                 #     print("Patch request for 'cascade_patch_pairing' object successful")
#                 # else:
#                 #     print("Patch request for 'cascade_patch_pairing' object failed with status code:", pairing_response.status_code)
                
#                 # END shitty idea 

# # endregion

#                 cascade_patch_pairing = Pairing.query.filter_by(id=response_obj.pairing_id).first()

#                 cascade_patch_pairing.pairing_tfp = sum_total_tfp
#                 cascade_patch_pairing.pairing_vacation_sick = sum_vacation_sick
#                 cascade_patch_pairing.pairing_vja = sum_vja
#                 cascade_patch_pairing.pairing_holiday = sum_holiday
#                 cascade_patch_pairing.pairing_time_half = sum_time_half
#                 cascade_patch_pairing.pairing_double_time = sum_double_time
#                 cascade_patch_pairing.pairing_double_half = sum_double_half
#                 cascade_patch_pairing.pairing_triple = sum_triple
#                 cascade_patch_pairing.pairing_overrides = sum_overrides
#                 cascade_patch_pairing.pairing_a_hours = sum_a_hours
#                 cascade_patch_pairing.pairing_total_credits = sum_total_credits
#                 cascade_patch_pairing.pairing_duty_hours = sum_daily_duty_hours

#                 db.session.add(cascade_patch_pairing)
#                 db.session.commit()
#                 # print(cascade_patch_pairing)

#                 all_cascade_patch_pairing =Pairing.query.filter_by(month_id=cascade_patch_pairing.month_id)
#                 #===============Reserve Stuff 
#                 sum_pairing_guarantee_hours = 0
#                 sum_pairing_guarantee_hours_worked_rated = 0
#                 #=============TAFB
#                 sum_tafb_total = 0
#                 sum_int_tafb_total = 0
#                 #============REGULAR TFP
#                 sum_pairing_tfp = 0
#                 #============VACATION/SICK
#                 sum_pairing_vacation_sick = 0
#                 #============VJA
#                 sum_pairing_vja = 0
#                 #============HOLIDAY
#                 sum_pairing_holiday = 0
#                 #============time_half
#                 sum_pairing_time_half = 0
#                 #================ DOUBLE TIME LYFE
#                 sum_pairing_double_time = 0
#                 #================ DOUBLE & HALF LYFE
#                 sum_pairing_double_half = 0
#                 #================ TRIPLE LYFE
#                 sum_pairing_triple = 0
#                 #================ OVERRIDES LYFE
#                 sum_pairing_overrides = 0
#                 #================ A-POSITION LYFE
#                 sum_pairing_a_hours = 0
#                 #============Totals
#                 sum_pairing_total_credits = 0
#                 #========New additions=======
#                 sum_pairing_duty_hours = 0
            

#                 for pairing in all_cascade_patch_pairing:
#                     if pairing.pairing_guarantee_hours != None:
#                         sum_pairing_guarantee_hours += pairing.pairing_guarantee_hours
#                     if pairing.pairing_guarantee_hours_worked_rated != None:
#                         sum_pairing_guarantee_hours_worked_rated += pairing.pairing_guarantee_hours_worked_rated
#                     if pairing.tafb_total != None:
#                         sum_tafb_total += pairing.tafb_total
#                     if pairing.int_tafb_total != None:
#                         sum_int_tafb_total += pairing.int_tafb_total
#                     if pairing.pairing_tfp != None:
#                         sum_pairing_tfp += pairing.pairing_tfp
#                     if pairing.pairing_vacation_sick != None:
#                         sum_pairing_vacation_sick += pairing.pairing_vacation_sick
#                     if pairing.pairing_vja != None:
#                         sum_pairing_vja += pairing.pairing_vja
#                     if pairing.pairing_holiday != None:
#                         sum_pairing_holiday += pairing.pairing_holiday
#                     if pairing.pairing_time_half != None:
#                         sum_pairing_time_half += pairing.pairing_time_half
#                     if pairing.pairing_double_time != None:
#                         sum_pairing_double_time += pairing.pairing_double_time
#                     if pairing.pairing_double_half != None:
#                         sum_pairing_double_half += pairing.pairing_double_half
#                     if pairing.pairing_triple != None:
#                         sum_pairing_triple += pairing.pairing_triple
#                     if pairing.pairing_overrides != None:
#                         sum_pairing_overrides += pairing.pairing_overrides
#                     if pairing.pairing_a_hours != None:
#                         sum_pairing_a_hours += pairing.pairing_a_hours
#                     if pairing.pairing_total_credits != None:
#                         sum_pairing_total_credits += pairing.pairing_total_credits
#                     if pairing.pairing_duty_hours != None:
#                         sum_pairing_duty_hours += pairing.pairing_duty_hours

                    

#                     # print(pairing, 'total all these')
                
#                 cascade_patch_month = Month.query.filter_by(id=cascade_patch_pairing.month_id).first()

#                 # print(cascade_patch_month)

#                 cascade_patch_month.month_guarantee_hours = sum_pairing_guarantee_hours
#                 cascade_patch_month.month_guarantee_hours_worked_rated = sum_pairing_guarantee_hours_worked_rated
#                 cascade_patch_month.month_tafb_total = sum_tafb_total
#                 cascade_patch_month.month_int_tafb_total = sum_int_tafb_total
#                 cascade_patch_month.month_tfp = sum_pairing_tfp
#                 cascade_patch_month.month_vacation_sick = sum_pairing_vacation_sick
#                 cascade_patch_month.month_vja = sum_pairing_vja
#                 cascade_patch_month.month_holiday = sum_pairing_holiday
#                 cascade_patch_month.month_time_half = sum_pairing_time_half
#                 cascade_patch_month.month_double_time = sum_pairing_double_time
#                 cascade_patch_month.month_double_half = sum_pairing_double_half
#                 cascade_patch_month.month_triple = sum_pairing_triple
#                 cascade_patch_month.month_overrides = sum_pairing_overrides
#                 cascade_patch_month.month_a_hours = sum_pairing_a_hours
#                 cascade_patch_month.month_total_credits = sum_pairing_total_credits
#                 cascade_patch_month.month_duty_hours = sum_pairing_duty_hours

#                 db.session.add(cascade_patch_month)
#                 db.session.commit()
                
#                 # THIS IS THE QUERY FOR ALL RELATED MONTHS
#                 all_cascade_patch_month = Month.query.filter_by(year_id=cascade_patch_month.year_id)
#                 #HERE WILL BE SEVERAL LINES OF SUM CONTAINERS
#                 #=============TAFB
#                 sum_month_tafb_total = 0
#                 sum_month_int_tafb_total = 0
#                 #============REGULAR TFP
#                 sum_month_tfp = 0
#                 #============VACATION/SICK
#                 sum_month_vacation_sick = 0
#                 #============VJA
#                 sum_month_vja = 0
#                 #============HOLIDAY
#                 sum_month_holiday = 0
#                 #============time_half
#                 sum_month_time_half = 0
#                 #================ DOUBLE TIME LYFE
#                 sum_month_double_time = 0
#                 #================ DOUBLE & HALF LYFE
#                 sum_month_double_half = 0
#                 #================ TRIPLE LYFE
#                 sum_month_triple = 0
#                 #================ OVERRIDES LYFE
#                 sum_month_overrides = 0
#                 #================ A-POSITION LYFE
#                 sum_month_a_hours = 0
#                 #============Totals
#                 sum_month_total_credits = 0
#                 #========New additions=======
#                 sum_month_duty_hours = 0
#                 #HERE WILL BE A LINE OF FOR/INS THAT WILL TOTAL EACH CAT FOR THE YEAR
#                 for month in all_cascade_patch_month:
#                     if month.month_tafb_total != None:
#                         sum_month_tafb_total += month.month_tafb_total
#                     if month.month_int_tafb_total != None:
#                         sum_month_int_tafb_total += month.month_int_tafb_total
#                     if month.month_tfp != None:
#                         sum_month_tfp += month.month_tfp
#                     if month.month_vacation_sick != None:
#                         sum_month_vacation_sick += month.month_vacation_sick
#                     if month.month_vja != None:
#                         sum_month_vja += month.month_vja
#                     if month.month_holiday != None:
#                         sum_month_holiday += month.month_holiday
#                     if month.month_time_half != None:
#                         sum_month_time_half += month.month_time_half
#                     if month.month_double_time != None:
#                         sum_month_double_time += month.month_double_time
#                     if month.month_double_half != None:
#                         sum_month_double_half += month.month_double_half
#                     if month.month_triple != None:
#                         sum_month_triple += month.month_triple
#                     if month.month_overrides != None:
#                         sum_month_overrides += month.month_overrides
#                     if month.month_a_hours != None:
#                         sum_month_a_hours += month.month_a_hours
#                     if month.month_total_credits != None:
#                         sum_month_total_credits += month.month_total_credits
#                     if month.month_duty_hours != None:
#                         sum_month_duty_hours += month.month_duty_hours

#                 #THIS IS THE QUERY FOR THE YEAR WE'RE UPDATING WITH THE MONTHLY TOTALS 
#                 cascade_patch_year = Year.query.filter_by(id=cascade_patch_month.year_id).first()
#                 # print(cascade_patch_year)
#                 #THIS WILL BE LINES WHERE WE ASSIGN VALUE TO YEAR CATS WITH MONTHLY TOTALS
#                 cascade_patch_year.year_tafb_total = sum_month_tafb_total
#                 cascade_patch_year.year_int_tafb_total = sum_month_int_tafb_total
#                 cascade_patch_year.year_tfp = sum_month_tfp
#                 cascade_patch_year.year_vacation_sick = sum_month_vacation_sick
#                 cascade_patch_year.year_vja = sum_month_vja
#                 cascade_patch_year.year_holiday = sum_month_holiday
#                 cascade_patch_year.year_time_half = sum_month_time_half
#                 cascade_patch_year.year_double_time = sum_month_double_time
#                 cascade_patch_year.year_double_half = sum_month_double_half
#                 cascade_patch_year.year_triple = sum_month_triple
#                 cascade_patch_year.year_overrides = sum_month_overrides
#                 cascade_patch_year.year_a_hours = sum_month_a_hours
#                 cascade_patch_year.year_total_credits = sum_month_total_credits
#                 cascade_patch_year.year_duty_hours = sum_month_duty_hours
#                 #COMMIT UPDATES 
#                 db.session.add(cascade_patch_year)
#                 db.session.commit()
# endregion
            except Exception as e:
                message = {'errors': [e.__str__()]}
                return make_response(message, 422)
            return make_response(response_obj.to_dict(), 200)
    def delete(self,id):
        response_obj = Day.query.filter_by(id=id).first()
        if response_obj == None: 
            response_dict = {
                "error": "Day not found"
            }
            return make_response(response_dict, 404)
        else:
            db.session.delete(response_obj)
            db.session.commit()
            response_dict = {"message": "deleted fo sho!"}
            return response_dict, 200
api.add_resource(DaysById, '/days/<int:id>')


class CascadeTest(Resource):
    def get(self, id):
        response_obj = Day.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                'error': 'Day not found'
            }
            return make_response(response_dict, 404)
        else:
            return make_response(response_obj.to_dict(), 200)
    def patch(self, id):
        response_obj = Day.query.filter_by(id=id).first()
        if response_obj == None:
            response_dict = {
                "error": "Day not found"
            }
            return make_response(response_dict, 404)
        else:
            request_object = request.get_json()
            try:
                for attr in request_object:
                    setattr(response_obj, attr, request_object[attr])
                 #============VACATION/SICK
                if "vacation_sick" in request_object:
                    response_obj.vacation_sick_pay = tfp_pay_function(request_object["vacation_sick"])
                #============REGULAR TFP
                if "total_tfp" in request_object:
                    response_obj.total_tfp_pay = tfp_pay_function(request_object["total_tfp"])
                #============VJA
                if "vja" in request_object:
                    response_obj.vja_rated = one_point_five_rate(request_object["vja"])
                    response_obj.vja_pay = one_point_five_pay(request_object["vja"])
                #============HOLIDAY
                if "holiday" in request_object:
                    response_obj.holiday_rated = double_rate(request_object["holiday"])
                    response_obj.holiday_pay = double_pay(request_object["holiday"])
                    # request_object["holiday"] = response_obj.holiday  # Add this line
                #============TIME_HALF
                if "time_half" in request_object:
                    response_obj.time_half_rated  = one_point_five_rate(request_object["time_half"])
                    response_obj.time_half_pay = one_point_five_pay(request_object["time_half"])
                #============DOUBLE_TIME
                if "double_time" in request_object:
                    response_obj.double_time_rated = double_rate(request_object["double_time"])
                    response_obj.double_time_pay = double_pay(request_object["double_time"])
                #============DOUBLE_HALF
                if "double_half" in request_object:
                    response_obj.double_half_rated = double_point_five_rate(request_object["double_half"])
                    response_obj.double_half_pay = double_point_five_pay(request_object["double_half"])
                #============TRIPLE
                if "triple" in request_object:
                    response_obj.triple_rated = triple_rate(request_object["triple"])
                    response_obj.triple_pay = triple_pay(request_object["triple"])
                #============OVERRIDES
                response_obj.overrides_pay = override_pay(request_object["overrides"])
                #============A-POSITON
                response_obj.a_position = request_object["a_position"]

                response_obj.a_hours = totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"]) if request_object["a_position"] else 0
                
                response_obj.a_pay = a_position_pay(request_object["a_position"],totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"]))

                # #========RESERVE NO FLY=======
                response_obj.reserve_no_fly = request_object["reserve_no_fly"]
                response_obj.reserve_no_fly_holiday = request_object["reserve_no_fly_holiday"]

                if request_object["reserve_no_fly"]:
                    response_obj.reserve_no_fly_hours = 6
                elif request_object["reserve_no_fly_holiday"]:
                    response_obj.reserve_no_fly_hours = 12
                else:
                    response_obj.reserve_no_fly_hours = 0
                
                response_obj.reserve_no_fly_pay = tfp_pay_function(response_obj.reserve_no_fly_hours)

                # response_obj.reserve_no_fly = request_object["reserve_no_fly"]
                # response_obj.reserve_no_fly_holiday = request_object["reserve_no_fly_holiday"]
                # response_obj.reserve_no_fly_hours = request_object["reserve_no_fly_hours"] + 12 if request_object["reserve_no_fly_holiday"] else 0
                # response_obj.reserve_no_fly_hours = request_object["reserve_no_fly_hours"] + 6 if request_object["reserve_no_fly"] else 0




                #============Totals ACTUAL 
                response_obj.total_credits = totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"],response_obj.reserve_no_fly_hours )
                # request_object["total_credits"] = response_obj.total_credits  # Add this line
                #============Totals RATED
                response_obj.total_credits_rated = totals(request_object["total_tfp"],request_object["vacation_sick"],one_point_five_rate(request_object["vja"]),double_rate(request_object["holiday"]),one_point_five_rate(request_object["time_half"]),double_rate(request_object["double_time"]),double_point_five_rate(request_object["double_half"]),triple_rate(request_object["triple"]), response_obj.reserve_no_fly_hours)
                # request_object["total_credits_rated"] = response_obj.total_credits_rated  # Add this line
                #============Totals PAY
                response_obj.total_pay = totals(tfp_pay_function(request_object["total_tfp"]),tfp_pay_function(request_object["vacation_sick"]),one_point_five_pay(request_object["vja"]),double_pay(request_object["holiday"]),one_point_five_pay(request_object["time_half"]),double_pay(request_object["double_time"]),double_point_five_pay(request_object["double_half"]),triple_pay(request_object["triple"]),override_pay(request_object["overrides"]),a_position_pay(request_object["a_position"],totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"])), tfp_pay_function(response_obj.reserve_no_fly_hours))
                # request_object["total_pay"] = response_obj.total_pay  # Add this line
                db.session.add(response_obj)
                db.session.commit()

                all_days = Day.query.filter_by(pairing_id=response_obj.pairing_id)
                #============REGULAR TFP
                sum_total_tfp = 0
                #============VACATION/SICK
                sum_vacation_sick = 0
                #============VJA
                sum_vja = 0
                #============HOLIDAY
                sum_holiday = 0
                #============time_half
                sum_time_half = 0
                #================ DOUBLE TIME LYFE
                sum_double_time = 0
                #================ DOUBLE & HALF LYFE
                sum_double_half = 0
                #================ TRIPLE LYFE
                sum_triple = 0
                #================ OVERRIDES LYFE
                sum_overrides = 0
                #================ A-POSITION LYFE
                sum_a_hours = 0
                #============Totals
                sum_total_credits = 0
                #========New additions=======
                sum_daily_duty_hours = 0
                sum_reserve_no_fly_hours = 0 


                for days in all_days:
                    if days.total_tfp != None:
                        sum_total_tfp += days.total_tfp
                    if days.vacation_sick != None:
                        sum_vacation_sick += days.vacation_sick
                    if days.vja != None:
                        sum_vja += days.vja
                    if days.holiday != None:
                        sum_holiday += days.holiday
                    if days.time_half != None:
                        sum_time_half += days.time_half
                    if days.double_time != None:
                        sum_double_time += days.double_time
                    if days.double_half != None:
                        sum_double_half += days.double_half
                    if days.triple != None:
                        sum_triple += days.triple
                    if days.overrides != None:
                        sum_overrides += days.overrides
                    if days.a_hours != None:
                        sum_a_hours += days.a_hours
                    if days.total_credits != None:
                        sum_total_credits += days.total_credits
                    if days.daily_duty_hours != None:
                        sum_daily_duty_hours += days.daily_duty_hours
                    if days.reserve_no_fly_hours != None:
                        sum_reserve_no_fly_hours += days.reserve_no_fly_hours
                    
                    cascade_patch_pairing = Pairing.query.filter_by(id=response_obj.pairing_id).first()
                    
                    #New shit ============
                    cascade_patch_pairing.pairing_duty_hours = sum_daily_duty_hours
                    #=============TAFB
                    # print(cascade_patch_pairing.tafb_total, ' the fuck is going on')
                    if cascade_patch_pairing.tafb_total:
                        cascade_patch_pairing.tafb_pay = tafb_pay(cascade_patch_pairing.tafb_total)
                    #=============TAFB INT
                    if cascade_patch_pairing.int_tafb_total:
                        cascade_patch_pairing.int_tafb_pay = int_tafb_pay(cascade_patch_pairing.int_tafb_total)
                    #============VACATION/SICK
                    cascade_patch_pairing.pairing_vacation_sick = sum_vacation_sick
                    cascade_patch_pairing.pairing_vacation_sick_pay = tfp_pay_function(sum_vacation_sick)
                    #============REGULAR TFP
                    cascade_patch_pairing.pairing_tfp = sum_total_tfp
                    cascade_patch_pairing.pairing_tfp_pay = tfp_pay_function(sum_total_tfp)
                    #============VJA
                    cascade_patch_pairing.pairing_vja = sum_vja
                    cascade_patch_pairing.pairing_vja_rated= one_point_five_rate(sum_vja)
                    cascade_patch_pairing.pairing_vja_pay= one_point_five_pay(sum_vja)
                    # #============HOLIDAY
                    cascade_patch_pairing.pairing_holiday = sum_holiday
                    cascade_patch_pairing.pairing_holiday_rated= double_rate(sum_holiday)
                    cascade_patch_pairing.pairing_holiday_pay= double_pay(sum_holiday)
                    #============TIME_HALF
                    cascade_patch_pairing.pairing_time_half = sum_time_half
                    cascade_patch_pairing.pairing_time_half_rated= one_point_five_rate(sum_time_half)
                    cascade_patch_pairing.pairing_time_half_pay= one_point_five_pay(sum_time_half)
                    #============DOUBLE_TIME
                    cascade_patch_pairing.pairing_double_time = sum_double_time
                    cascade_patch_pairing.pairing_double_time_rated= more_better_function_rate(sum_double_time,2)
                    cascade_patch_pairing.pairing_double_time_pay= more_better_function_pay(sum_double_time,2)
                    #============DOUBLE_HALF
                    cascade_patch_pairing.pairing_double_half = sum_double_half
                    cascade_patch_pairing.pairing_double_half_rated= more_better_function_rate(sum_double_half,2.5)
                    cascade_patch_pairing.pairing_double_half_pay= more_better_function_pay(sum_double_half,2.5)
                    #============TRIPLE
                    cascade_patch_pairing.pairing_triple = sum_triple
                    cascade_patch_pairing.pairing_triple_rated= more_better_function_rate(sum_triple,3)
                    cascade_patch_pairing.pairing_triple_pay= more_better_function_pay(sum_triple,3)
                    #============OVERRIDES
                    cascade_patch_pairing.pairing_overrides = sum_overrides
                    cascade_patch_pairing.pairing_overrides_pay = override_pay(sum_overrides)
                    #============A-POSITON
                    cascade_patch_pairing.pairing_a_hours = sum_a_hours
                    cascade_patch_pairing.pairing_a_pay = container_a_position_pay(sum_a_hours)
                    # #===============Reserve Stuff 
                    cascade_patch_pairing.reserve_block = cascade_patch_pairing.reserve_block
                    # #===============Reserve GUARANTEE HOURS 
                    if cascade_patch_pairing.reserve_block:
                        day_count = Day.query.filter_by(pairing_id=cascade_patch_pairing.id).count()
                        if cascade_patch_pairing.reserve_block:
                            cascade_patch_pairing.pairing_guarantee_hours = 6 * day_count
                        else:
                            cascade_patch_pairing.pairing_guarantee_hours = 0
                    # #===============Reserve NO FLY HOURS 
                    cascade_patch_pairing.pairing_reserve_no_fly_hours = sum_reserve_no_fly_hours
                    cascade_patch_pairing.pairing_reserve_no_fly_pay = tfp_pay_function(sum_reserve_no_fly_hours)

                    #===============Reserve  WORKED TOWARDS GUARANTEE  
                    cascade_patch_pairing.pairing_guarantee_hours_worked_rated = totals(sum_total_tfp,sum_reserve_no_fly_hours, sum_vacation_sick,one_point_five_rate(sum_vja),double_rate(sum_holiday),one_point_five_rate(sum_time_half),more_better_function_rate(sum_double_time,2),more_better_function_rate(sum_double_half,2.5),more_better_function_rate(sum_triple,3)) if cascade_patch_pairing.reserve_block else 0
                    #============Totals ACTUAL 
                    cascade_patch_pairing.pairing_total_credits = totals(sum_total_tfp,sum_reserve_no_fly_hours, sum_vacation_sick,sum_vja,sum_holiday,sum_time_half,sum_double_time,sum_double_half,sum_triple)
                    #============Totals RATED
                    cascade_patch_pairing.pairing_total_credits_rated= totals(sum_reserve_no_fly_hours,sum_total_tfp,sum_vacation_sick,one_point_five_rate(sum_vja),double_rate(sum_holiday),one_point_five_rate(sum_time_half),more_better_function_rate(sum_double_time,2),more_better_function_rate(sum_double_half,2.5),more_better_function_rate(sum_triple,3))
                    #============Totals PAY
                    cascade_patch_pairing.pairing_total_pay = totals(tfp_pay_function(sum_total_tfp),tfp_pay_function(sum_vacation_sick),one_point_five_pay(sum_vja),double_pay(sum_holiday),one_point_five_pay(sum_time_half),more_better_function_pay(sum_double_time,2),more_better_function_pay(sum_double_half,2.5),more_better_function_pay(sum_triple,3), tafb_pay(cascade_patch_pairing.tafb_total),int_tafb_pay(cascade_patch_pairing.int_tafb_total),override_pay(sum_overrides),container_a_position_pay(sum_a_hours), tfp_pay_function(sum_reserve_no_fly_hours))
                    # #=====================


                    db.session.add(cascade_patch_pairing)
                    db.session.commit()

                    all_cascade_patch_pairing =Pairing.query.filter_by(month_id=cascade_patch_pairing.month_id)
                     #===============Reserve Stuff 
                    sum_pairing_guarantee_hours = 0
                    sum_pairing_guarantee_hours_worked_rated = 0
                    #=============TAFB
                    sum_tafb_total = 0
                    sum_int_tafb_total = 0
                    #============REGULAR TFP
                    sum_pairing_tfp = 0
                    #============VACATION/SICK
                    sum_pairing_vacation_sick = 0
                    #============VJA
                    sum_pairing_vja = 0
                    #============HOLIDAY
                    sum_pairing_holiday = 0
                    #============time_half
                    sum_pairing_time_half = 0
                    #================ DOUBLE TIME LYFE
                    sum_pairing_double_time = 0
                    #================ DOUBLE & HALF LYFE
                    sum_pairing_double_half = 0
                    #================ TRIPLE LYFE
                    sum_pairing_triple = 0
                    #================ OVERRIDES LYFE
                    sum_pairing_overrides = 0
                    #================ A-POSITION LYFE
                    sum_pairing_a_hours = 0
                    #============Totals
                    sum_pairing_total_credits = 0
                    #========New additions=======
                    sum_pairing_duty_hours = 0
                    sum_pairing_reserve_no_fly_hours =0

                    for pairing in all_cascade_patch_pairing:
                        if pairing.pairing_guarantee_hours != None:
                            sum_pairing_guarantee_hours += pairing.pairing_guarantee_hours
                        if pairing.pairing_guarantee_hours_worked_rated != None:
                            sum_pairing_guarantee_hours_worked_rated += pairing.pairing_guarantee_hours_worked_rated
                        if pairing.tafb_total != None:
                            sum_tafb_total += pairing.tafb_total
                        if pairing.int_tafb_total != None:
                            sum_int_tafb_total += pairing.int_tafb_total
                        if pairing.pairing_tfp != None:
                            sum_pairing_tfp += pairing.pairing_tfp
                        if pairing.pairing_vacation_sick != None:
                            sum_pairing_vacation_sick += pairing.pairing_vacation_sick
                        if pairing.pairing_vja != None:
                            sum_pairing_vja += pairing.pairing_vja
                        if pairing.pairing_holiday != None:
                            sum_pairing_holiday += pairing.pairing_holiday
                        if pairing.pairing_time_half != None:
                            sum_pairing_time_half += pairing.pairing_time_half
                        if pairing.pairing_double_time != None:
                            sum_pairing_double_time += pairing.pairing_double_time
                        if pairing.pairing_double_half != None:
                            sum_pairing_double_half += pairing.pairing_double_half
                        if pairing.pairing_triple != None:
                            sum_pairing_triple += pairing.pairing_triple
                        if pairing.pairing_overrides != None:
                            sum_pairing_overrides += pairing.pairing_overrides
                        if pairing.pairing_a_hours != None:
                            sum_pairing_a_hours += pairing.pairing_a_hours
                        if pairing.pairing_total_credits != None:
                            sum_pairing_total_credits += pairing.pairing_total_credits
                        if pairing.pairing_duty_hours != None:
                            sum_pairing_duty_hours += pairing.pairing_duty_hours
                        if pairing.pairing_reserve_no_fly_hours != None:
                            sum_pairing_reserve_no_fly_hours += pairing.pairing_reserve_no_fly_hours

                    cascade_patch_month = Month.query.filter_by(id=cascade_patch_pairing.month_id).first()
                    #========New additions=======
                    cascade_patch_month.month_duty_hours = sum_pairing_duty_hours
                    #=============TAFB
                    cascade_patch_month.month_tafb_total = sum_tafb_total
                    cascade_patch_month.month_tafb_pay = tafb_pay(sum_tafb_total)
                    #=============TAFB INT
                    cascade_patch_month.month_int_tafb_total = sum_int_tafb_total
                    cascade_patch_month.month_int_tafb_pay = int_tafb_pay(sum_int_tafb_total)
                    #============VACATION/SICK
                    cascade_patch_month.month_vacation_sick = sum_pairing_vacation_sick
                    cascade_patch_month.month_vacation_sick_pay = tfp_pay_function(sum_pairing_vacation_sick)
                    #============REGULAR TFP
                    cascade_patch_month.month_tfp = sum_pairing_tfp
                    cascade_patch_month.month_tfp_pay = tfp_pay_function(sum_pairing_tfp)
                    #============VJA
                    cascade_patch_month.month_vja = sum_pairing_vja
                    cascade_patch_month.month_vja_rated= one_point_five_rate(sum_pairing_vja)
                    cascade_patch_month.month_vja_pay= one_point_five_pay(sum_pairing_vja)
                    # #============HOLIDAY
                    cascade_patch_month.month_holiday = sum_pairing_holiday
                    cascade_patch_month.month_holiday_rated= double_rate(sum_pairing_holiday)
                    cascade_patch_month.month_holiday_pay= double_pay(sum_pairing_holiday)
                    #============TIME_HALF
                    cascade_patch_month.month_time_half = sum_pairing_time_half
                    cascade_patch_month.month_time_half_rated= one_point_five_rate(sum_pairing_time_half)
                    cascade_patch_month.month_time_half_pay= one_point_five_pay(sum_pairing_time_half)
                    #============DOUBLE_TIME
                    cascade_patch_month.month_double_time = sum_pairing_double_time
                    cascade_patch_month.month_double_time_rated= more_better_function_rate(sum_pairing_double_time,2)
                    cascade_patch_month.month_double_time_pay= more_better_function_pay(sum_pairing_double_time,2)
                    #============DOUBLE_HALF
                    cascade_patch_month.month_double_half = sum_pairing_double_half
                    cascade_patch_month.month_double_half_rated= more_better_function_rate(sum_pairing_double_half,2.5)
                    cascade_patch_month.month_double_half_pay= more_better_function_pay(sum_pairing_double_half,2.5)
                    #============TRIPLE
                    cascade_patch_month.month_triple = sum_pairing_triple
                    cascade_patch_month.month_triple_rated= more_better_function_rate(sum_pairing_triple,3)
                    cascade_patch_month.month_triple_pay= more_better_function_pay(sum_pairing_triple,3)
                    #============OVERRIDES
                    cascade_patch_month.month_overrides = sum_pairing_overrides
                    cascade_patch_month.month_overrides_pay = override_pay(sum_pairing_overrides)
                    #============A-POSITON
                    cascade_patch_month.month_a_hours = sum_pairing_a_hours
                    cascade_patch_month.month_a_pay = container_a_position_pay(sum_pairing_a_hours)
                    # #===============Reserve NO FLY HOURS 
                    cascade_patch_month.month_reserve_no_fly_hours = sum_pairing_reserve_no_fly_hours
                    cascade_patch_month.month_reserve_no_fly_pay = tfp_pay_function(sum_pairing_reserve_no_fly_hours)
                    # #===============Reserve GUARANTEE HOURS 
                    cascade_patch_month.month_guarantee_hours = sum_pairing_guarantee_hours
                    cascade_patch_month.month_guarantee_hours_worked_rated = sum_pairing_guarantee_hours_worked_rated
                    #============Totals ACTUAL 
                    cascade_patch_month.month_total_credits = totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,sum_pairing_vja,sum_pairing_holiday,sum_pairing_time_half,sum_pairing_double_time,sum_pairing_double_half,sum_pairing_triple)
                    #============Totals RATED
                    cascade_patch_month.month_total_credits_rated= totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,one_point_five_rate(sum_pairing_vja),double_rate(sum_pairing_holiday),one_point_five_rate(sum_pairing_time_half),more_better_function_rate(sum_pairing_double_time,2),more_better_function_rate(sum_pairing_double_half,2.5),more_better_function_rate(sum_pairing_triple,3))
                    #============Totals PAY
                    cascade_patch_month.month_total_pay = totals(tfp_pay_function(sum_pairing_reserve_no_fly_hours),tfp_pay_function(sum_pairing_tfp),tfp_pay_function(sum_pairing_vacation_sick),one_point_five_pay(sum_pairing_vja),double_pay(sum_pairing_holiday),one_point_five_pay(sum_pairing_time_half),more_better_function_pay(sum_pairing_double_time,2),more_better_function_pay(sum_pairing_double_half,2.5),more_better_function_pay(sum_pairing_triple,3), tafb_pay(sum_tafb_total),int_tafb_pay(sum_int_tafb_total),override_pay(sum_pairing_overrides),container_a_position_pay(sum_pairing_a_hours))
                    # #=====================
                    db.session.add(cascade_patch_month)
                    db.session.commit()
                    # THIS IS THE QUERY FOR ALL RELATED MONTHS
                    all_cascade_patch_month = Month.query.filter_by(year_id=cascade_patch_month.year_id)
                    #========New additions=======
                    sum_month_duty_hours = 0
                    #=============TAFB
                    sum_month_tafb_total = 0
                    sum_month_int_tafb_total = 0
                    #============REGULAR TFP
                    sum_month_tfp = 0
                    #============VACATION/SICK
                    sum_month_vacation_sick = 0
                    #============VJA
                    sum_month_vja = 0
                    #============HOLIDAY
                    sum_month_holiday = 0
                    #============time_half
                    sum_month_time_half = 0
                    #================ DOUBLE TIME LYFE
                    sum_month_double_time = 0
                    #================ DOUBLE & HALF LYFE
                    sum_month_double_half = 0
                    #================ TRIPLE LYFE
                    sum_month_triple = 0
                    #================ OVERRIDES LYFE
                    sum_month_overrides = 0
                    #================ A-POSITION LYFE
                    sum_month_a_hours = 0
                    #============Totals
                    sum_month_total_credits = 0
                    #========Reserve No Fly=======
                    sum_month_reserve_no_fly_hours = 0

                    #HERE WILL BE A LINE OF FOR/INS THAT WILL TOTAL EACH CAT FOR THE YEAR
                    for month in all_cascade_patch_month:
                        # if month.month_guarantee_hours != None:
                        #     sum_month_guarantee_hours += month.month_guarantee_hours
                        # if month.month_guarantee_hours_worked_rated != None:
                        #     sum_month_guarantee_hours_worked_rated += month.month_guarantee_hours_worked_rated
                        if month.month_tafb_total != None:
                            sum_month_tafb_total += month.month_tafb_total
                        if month.month_int_tafb_total != None:
                            sum_month_int_tafb_total += month.month_int_tafb_total
                        if month.month_tfp != None:
                            sum_month_tfp += month.month_tfp
                        if month.month_vacation_sick != None:
                            sum_month_vacation_sick += month.month_vacation_sick
                        if month.month_vja != None:
                            sum_month_vja += month.month_vja
                        if month.month_holiday != None:
                            sum_month_holiday += month.month_holiday
                        if month.month_time_half != None:
                            sum_month_time_half += month.month_time_half
                        if month.month_double_time != None:
                            sum_month_double_time += month.month_double_time
                        if month.month_double_half != None:
                            sum_month_double_half += month.month_double_half
                        if month.month_triple != None:
                            sum_month_triple += month.month_triple
                        if month.month_overrides != None:
                            sum_month_overrides += month.month_overrides
                        if month.month_a_hours != None:
                            sum_month_a_hours += month.month_a_hours
                        if month.month_total_credits != None:
                            sum_month_total_credits += month.month_total_credits
                        if month.month_duty_hours != None:
                            sum_month_duty_hours += month.month_duty_hours
                        if month.month_reserve_no_fly_hours != None:
                            sum_month_reserve_no_fly_hours += month.month_reserve_no_fly_hours

                        #THIS IS THE QUERY FOR THE YEAR WE'RE UPDATING WITH THE MONTHLY TOTALS 
                        cascade_patch_year = Year.query.filter_by(id=cascade_patch_month.year_id).first()
                        #THIS WILL BE LINES WHERE WE ASSIGN VALUE TO YEAR CATS WITH MONTHLY TOTALS
                        #========New additions=======
                        cascade_patch_year.year_duty_hours = sum_month_duty_hours
                        #=============TAFB
                        cascade_patch_year.year_tafb_total = sum_month_tafb_total
                        cascade_patch_year.year_tafb_pay = tafb_pay(sum_month_tafb_total)
                        #=============TAFB INT
                        cascade_patch_year.year_int_tafb = sum_month_int_tafb_total
                        cascade_patch_year.year_int_tafb_pay = int_tafb_pay(sum_month_int_tafb_total)
                        #============VACATION/SICK
                        cascade_patch_year.year_vacation_sick = sum_month_vacation_sick
                        cascade_patch_year.year_vacation_sick_pay = tfp_pay_function(sum_month_vacation_sick)
                        #============REGULAR TFP
                        cascade_patch_year.year_tfp = sum_month_tfp
                        cascade_patch_year.year_tfp_pay = tfp_pay_function(sum_month_tfp)
                        #============VJA
                        cascade_patch_year.year_vja = sum_month_vja
                        cascade_patch_year.year_vja_rated= one_point_five_rate(sum_month_vja)
                        cascade_patch_year.year_vja_pay= one_point_five_pay(sum_month_vja)
                        # #============HOLIDAY
                        cascade_patch_year.year_holiday = sum_month_holiday
                        cascade_patch_year.year_holiday_rated= double_rate(sum_month_holiday)
                        cascade_patch_year.year_holiday_pay= double_pay(sum_month_holiday)
                        #============TIME_HALF
                        cascade_patch_year.year_time_half = sum_month_time_half
                        cascade_patch_year.year_time_half_rated= one_point_five_rate(sum_month_time_half)
                        cascade_patch_year.year_time_half_pay= one_point_five_pay(sum_month_time_half)
                        #============DOUBLE_TIME
                        cascade_patch_year.year_double_time = sum_month_double_time
                        cascade_patch_year.year_double_time_rated= more_better_function_rate(sum_month_double_time,2)
                        cascade_patch_year.year_double_time_pay= more_better_function_pay(sum_month_double_time,2)
                        #============DOUBLE_HALF
                        cascade_patch_year.year_double_half = sum_month_double_half
                        cascade_patch_year.year_double_half_rated= more_better_function_rate(sum_month_double_half,2.5)
                        cascade_patch_year.year_double_half_pay= more_better_function_pay(sum_month_double_half,2.5)
                        #============TRIPLE
                        cascade_patch_year.year_triple = sum_month_triple
                        cascade_patch_year.year_triple_rated= more_better_function_rate(sum_month_triple,3)
                        cascade_patch_year.year_triple_pay= more_better_function_pay(sum_month_triple,3)
                        #============OVERRIDES
                        cascade_patch_year.year_overrides = sum_month_overrides
                        cascade_patch_year.year_overrides_pay = override_pay(sum_month_overrides)
                        #============A-POSITON
                        cascade_patch_year.year_a_hours = sum_month_a_hours
                        cascade_patch_year.year_a_pay = container_a_position_pay(sum_month_a_hours)
                        # # #===============Reserve Nofly HOURS 
                        cascade_patch_year.year_reserve_no_fly_hours = sum_month_reserve_no_fly_hours
                        cascade_patch_year.year_reserve_no_fly_pay = tfp_pay_function(sum_month_reserve_no_fly_hours)
                        # cascade_patch_year.year_guarantee_hours = sum_month_guarantee_hours
                        # cascade_patch_year.year_guarantee_hours_worked_rated = sum_month_guarantee_hours_worked_rated
                        #============Totals ACTUAL 
                        cascade_patch_year.year_total_credits = totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,sum_month_vja,sum_month_holiday,sum_month_time_half,sum_month_double_time,sum_month_double_half,sum_month_triple)
                        #============Totals RATED
                        cascade_patch_year.year_total_credits_rated= totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,one_point_five_rate(sum_month_vja),double_rate(sum_month_holiday),one_point_five_rate(sum_month_time_half),more_better_function_rate(sum_month_double_time,2),more_better_function_rate(sum_month_double_half,2.5),more_better_function_rate(sum_month_triple,3))
                        #============Totals PAY
                        cascade_patch_year.year_total_pay = totals(tfp_pay_function(sum_month_reserve_no_fly_hours),tfp_pay_function(sum_month_tfp),tfp_pay_function(sum_month_vacation_sick),one_point_five_pay(sum_month_vja),double_pay(sum_month_holiday),one_point_five_pay(sum_month_time_half),more_better_function_pay(sum_month_double_time,2),more_better_function_pay(sum_month_double_half,2.5),more_better_function_pay(sum_month_triple,3), tafb_pay(sum_month_tafb_total),int_tafb_pay(sum_month_int_tafb_total),override_pay(sum_month_overrides),container_a_position_pay(sum_month_a_hours))
                        # #=====================
                        db.session.add(cascade_patch_year)
                        db.session.commit()
            except Exception as e:
                message = {'errors': [e.__str__()]}
                return make_response(message, 422)
            return make_response(response_obj.to_dict(), 200)
    def delete(self,id):
        response_obj = Day.query.filter_by(id=id).first()
        if response_obj == None: 
            response_dict = {
                "error": "Day not found"
            }
            return make_response(response_dict, 404)
        else:
            id_to_use = response_obj.pairing_id
            db.session.delete(response_obj)
            db.session.commit()
            all_days = Day.query.filter_by(pairing_id=id_to_use)
            #============REGULAR TFP
            sum_total_tfp = 0
            #============VACATION/SICK
            sum_vacation_sick = 0
            #============VJA
            sum_vja = 0
            #============HOLIDAY
            sum_holiday = 0
            #============time_half
            sum_time_half = 0
            #================ DOUBLE TIME LYFE
            sum_double_time = 0
            #================ DOUBLE & HALF LYFE
            sum_double_half = 0
            #================ TRIPLE LYFE
            sum_triple = 0
            #================ OVERRIDES LYFE
            sum_overrides = 0
            #================ A-POSITION LYFE
            sum_a_hours = 0
            #============Totals
            sum_total_credits = 0
            #========New additions=======
            sum_daily_duty_hours = 0
            sum_reserve_no_fly_hours = 0 


            for days in all_days:
                if days.total_tfp != None:
                    sum_total_tfp += days.total_tfp
                if days.vacation_sick != None:
                    sum_vacation_sick += days.vacation_sick
                if days.vja != None:
                    sum_vja += days.vja
                if days.holiday != None:
                    sum_holiday += days.holiday
                if days.time_half != None:
                    sum_time_half += days.time_half
                if days.double_time != None:
                    sum_double_time += days.double_time
                if days.double_half != None:
                    sum_double_half += days.double_half
                if days.triple != None:
                    sum_triple += days.triple
                if days.overrides != None:
                    sum_overrides += days.overrides
                if days.a_hours != None:
                    sum_a_hours += days.a_hours
                if days.total_credits != None:
                    sum_total_credits += days.total_credits
                if days.daily_duty_hours != None:
                    sum_daily_duty_hours += days.daily_duty_hours
                if days.reserve_no_fly_hours != None:
                    sum_reserve_no_fly_hours += days.reserve_no_fly_hours
                
                cascade_patch_pairing = Pairing.query.filter_by(id=id_to_use).first()
                
                #New shit ============
                cascade_patch_pairing.pairing_duty_hours = sum_daily_duty_hours
                #=============TAFB
                # print(cascade_patch_pairing.tafb_total, ' the fuck is going on')
                if cascade_patch_pairing.tafb_total:
                    cascade_patch_pairing.tafb_pay = tafb_pay(cascade_patch_pairing.tafb_total)
                #=============TAFB INT
                if cascade_patch_pairing.int_tafb_total:
                    cascade_patch_pairing.int_tafb_pay = int_tafb_pay(cascade_patch_pairing.int_tafb_total)
                #============VACATION/SICK
                cascade_patch_pairing.pairing_vacation_sick = sum_vacation_sick
                cascade_patch_pairing.pairing_vacation_sick_pay = tfp_pay_function(sum_vacation_sick)
                #============REGULAR TFP
                cascade_patch_pairing.pairing_tfp = sum_total_tfp
                cascade_patch_pairing.pairing_tfp_pay = tfp_pay_function(sum_total_tfp)
                #============VJA
                cascade_patch_pairing.pairing_vja = sum_vja
                cascade_patch_pairing.pairing_vja_rated= one_point_five_rate(sum_vja)
                cascade_patch_pairing.pairing_vja_pay= one_point_five_pay(sum_vja)
                # #============HOLIDAY
                cascade_patch_pairing.pairing_holiday = sum_holiday
                cascade_patch_pairing.pairing_holiday_rated= double_rate(sum_holiday)
                cascade_patch_pairing.pairing_holiday_pay= double_pay(sum_holiday)
                #============TIME_HALF
                cascade_patch_pairing.pairing_time_half = sum_time_half
                cascade_patch_pairing.pairing_time_half_rated= one_point_five_rate(sum_time_half)
                cascade_patch_pairing.pairing_time_half_pay= one_point_five_pay(sum_time_half)
                #============DOUBLE_TIME
                cascade_patch_pairing.pairing_double_time = sum_double_time
                cascade_patch_pairing.pairing_double_time_rated= more_better_function_rate(sum_double_time,2)
                cascade_patch_pairing.pairing_double_time_pay= more_better_function_pay(sum_double_time,2)
                #============DOUBLE_HALF
                cascade_patch_pairing.pairing_double_half = sum_double_half
                cascade_patch_pairing.pairing_double_half_rated= more_better_function_rate(sum_double_half,2.5)
                cascade_patch_pairing.pairing_double_half_pay= more_better_function_pay(sum_double_half,2.5)
                #============TRIPLE
                cascade_patch_pairing.pairing_triple = sum_triple
                cascade_patch_pairing.pairing_triple_rated= more_better_function_rate(sum_triple,3)
                cascade_patch_pairing.pairing_triple_pay= more_better_function_pay(sum_triple,3)
                #============OVERRIDES
                cascade_patch_pairing.pairing_overrides = sum_overrides
                cascade_patch_pairing.pairing_overrides_pay = override_pay(sum_overrides)
                #============A-POSITON
                cascade_patch_pairing.pairing_a_hours = sum_a_hours
                cascade_patch_pairing.pairing_a_pay = container_a_position_pay(sum_a_hours)
                # #===============Reserve Stuff 
                cascade_patch_pairing.reserve_block = cascade_patch_pairing.reserve_block
                # #===============Reserve GUARANTEE HOURS 
                if cascade_patch_pairing.reserve_block:
                    day_count = Day.query.filter_by(pairing_id=cascade_patch_pairing.id).count()
                    if cascade_patch_pairing.reserve_block:
                        cascade_patch_pairing.pairing_guarantee_hours = 6 * day_count
                    else:
                        cascade_patch_pairing.pairing_guarantee_hours = 0
                # #===============Reserve NO FLY HOURS 
                cascade_patch_pairing.pairing_reserve_no_fly_hours = sum_reserve_no_fly_hours
                cascade_patch_pairing.pairing_reserve_no_fly_pay = tfp_pay_function(sum_reserve_no_fly_hours)

                #===============Reserve  WORKED TOWARDS GUARANTEE  
                cascade_patch_pairing.pairing_guarantee_hours_worked_rated = totals(sum_total_tfp,sum_reserve_no_fly_hours, sum_vacation_sick,one_point_five_rate(sum_vja),double_rate(sum_holiday),one_point_five_rate(sum_time_half),more_better_function_rate(sum_double_time,2),more_better_function_rate(sum_double_half,2.5),more_better_function_rate(sum_triple,3)) if cascade_patch_pairing.reserve_block else 0
                #============Totals ACTUAL 
                cascade_patch_pairing.pairing_total_credits = totals(sum_total_tfp,sum_reserve_no_fly_hours, sum_vacation_sick,sum_vja,sum_holiday,sum_time_half,sum_double_time,sum_double_half,sum_triple)
                #============Totals RATED
                cascade_patch_pairing.pairing_total_credits_rated= totals(sum_reserve_no_fly_hours,sum_total_tfp,sum_vacation_sick,one_point_five_rate(sum_vja),double_rate(sum_holiday),one_point_five_rate(sum_time_half),more_better_function_rate(sum_double_time,2),more_better_function_rate(sum_double_half,2.5),more_better_function_rate(sum_triple,3))
                #============Totals PAY
                cascade_patch_pairing.pairing_total_pay = totals(tfp_pay_function(sum_total_tfp),tfp_pay_function(sum_vacation_sick),one_point_five_pay(sum_vja),double_pay(sum_holiday),one_point_five_pay(sum_time_half),more_better_function_pay(sum_double_time,2),more_better_function_pay(sum_double_half,2.5),more_better_function_pay(sum_triple,3), tafb_pay(cascade_patch_pairing.tafb_total),int_tafb_pay(cascade_patch_pairing.int_tafb_total),override_pay(sum_overrides),container_a_position_pay(sum_a_hours), tfp_pay_function(sum_reserve_no_fly_hours))
                # #=====================


                db.session.add(cascade_patch_pairing)
                db.session.commit()

                all_cascade_patch_pairing =Pairing.query.filter_by(month_id=cascade_patch_pairing.month_id)
                    #===============Reserve Stuff 
                sum_pairing_guarantee_hours = 0
                sum_pairing_guarantee_hours_worked_rated = 0
                #=============TAFB
                sum_tafb_total = 0
                sum_int_tafb_total = 0
                #============REGULAR TFP
                sum_pairing_tfp = 0
                #============VACATION/SICK
                sum_pairing_vacation_sick = 0
                #============VJA
                sum_pairing_vja = 0
                #============HOLIDAY
                sum_pairing_holiday = 0
                #============time_half
                sum_pairing_time_half = 0
                #================ DOUBLE TIME LYFE
                sum_pairing_double_time = 0
                #================ DOUBLE & HALF LYFE
                sum_pairing_double_half = 0
                #================ TRIPLE LYFE
                sum_pairing_triple = 0
                #================ OVERRIDES LYFE
                sum_pairing_overrides = 0
                #================ A-POSITION LYFE
                sum_pairing_a_hours = 0
                #============Totals
                sum_pairing_total_credits = 0
                #========New additions=======
                sum_pairing_duty_hours = 0
                sum_pairing_reserve_no_fly_hours =0

                for pairing in all_cascade_patch_pairing:
                    if pairing.pairing_guarantee_hours != None:
                        sum_pairing_guarantee_hours += pairing.pairing_guarantee_hours
                    if pairing.pairing_guarantee_hours_worked_rated != None:
                        sum_pairing_guarantee_hours_worked_rated += pairing.pairing_guarantee_hours_worked_rated
                    if pairing.tafb_total != None:
                        sum_tafb_total += pairing.tafb_total
                    if pairing.int_tafb_total != None:
                        sum_int_tafb_total += pairing.int_tafb_total
                    if pairing.pairing_tfp != None:
                        sum_pairing_tfp += pairing.pairing_tfp
                    if pairing.pairing_vacation_sick != None:
                        sum_pairing_vacation_sick += pairing.pairing_vacation_sick
                    if pairing.pairing_vja != None:
                        sum_pairing_vja += pairing.pairing_vja
                    if pairing.pairing_holiday != None:
                        sum_pairing_holiday += pairing.pairing_holiday
                    if pairing.pairing_time_half != None:
                        sum_pairing_time_half += pairing.pairing_time_half
                    if pairing.pairing_double_time != None:
                        sum_pairing_double_time += pairing.pairing_double_time
                    if pairing.pairing_double_half != None:
                        sum_pairing_double_half += pairing.pairing_double_half
                    if pairing.pairing_triple != None:
                        sum_pairing_triple += pairing.pairing_triple
                    if pairing.pairing_overrides != None:
                        sum_pairing_overrides += pairing.pairing_overrides
                    if pairing.pairing_a_hours != None:
                        sum_pairing_a_hours += pairing.pairing_a_hours
                    if pairing.pairing_total_credits != None:
                        sum_pairing_total_credits += pairing.pairing_total_credits
                    if pairing.pairing_duty_hours != None:
                        sum_pairing_duty_hours += pairing.pairing_duty_hours
                    if pairing.pairing_reserve_no_fly_hours != None:
                        sum_pairing_reserve_no_fly_hours += pairing.pairing_reserve_no_fly_hours

                cascade_patch_month = Month.query.filter_by(id=cascade_patch_pairing.month_id).first()
                #========New additions=======
                cascade_patch_month.month_duty_hours = sum_pairing_duty_hours
                #=============TAFB
                cascade_patch_month.month_tafb_total = sum_tafb_total
                cascade_patch_month.month_tafb_pay = tafb_pay(sum_tafb_total)
                #=============TAFB INT
                cascade_patch_month.month_int_tafb_total = sum_int_tafb_total
                cascade_patch_month.month_int_tafb_pay = int_tafb_pay(sum_int_tafb_total)
                #============VACATION/SICK
                cascade_patch_month.month_vacation_sick = sum_pairing_vacation_sick
                cascade_patch_month.month_vacation_sick_pay = tfp_pay_function(sum_pairing_vacation_sick)
                #============REGULAR TFP
                cascade_patch_month.month_tfp = sum_pairing_tfp
                cascade_patch_month.month_tfp_pay = tfp_pay_function(sum_pairing_tfp)
                #============VJA
                cascade_patch_month.month_vja = sum_pairing_vja
                cascade_patch_month.month_vja_rated= one_point_five_rate(sum_pairing_vja)
                cascade_patch_month.month_vja_pay= one_point_five_pay(sum_pairing_vja)
                # #============HOLIDAY
                cascade_patch_month.month_holiday = sum_pairing_holiday
                cascade_patch_month.month_holiday_rated= double_rate(sum_pairing_holiday)
                cascade_patch_month.month_holiday_pay= double_pay(sum_pairing_holiday)
                #============TIME_HALF
                cascade_patch_month.month_time_half = sum_pairing_time_half
                cascade_patch_month.month_time_half_rated= one_point_five_rate(sum_pairing_time_half)
                cascade_patch_month.month_time_half_pay= one_point_five_pay(sum_pairing_time_half)
                #============DOUBLE_TIME
                cascade_patch_month.month_double_time = sum_pairing_double_time
                cascade_patch_month.month_double_time_rated= more_better_function_rate(sum_pairing_double_time,2)
                cascade_patch_month.month_double_time_pay= more_better_function_pay(sum_pairing_double_time,2)
                #============DOUBLE_HALF
                cascade_patch_month.month_double_half = sum_pairing_double_half
                cascade_patch_month.month_double_half_rated= more_better_function_rate(sum_pairing_double_half,2.5)
                cascade_patch_month.month_double_half_pay= more_better_function_pay(sum_pairing_double_half,2.5)
                #============TRIPLE
                cascade_patch_month.month_triple = sum_pairing_triple
                cascade_patch_month.month_triple_rated= more_better_function_rate(sum_pairing_triple,3)
                cascade_patch_month.month_triple_pay= more_better_function_pay(sum_pairing_triple,3)
                #============OVERRIDES
                cascade_patch_month.month_overrides = sum_pairing_overrides
                cascade_patch_month.month_overrides_pay = override_pay(sum_pairing_overrides)
                #============A-POSITON
                cascade_patch_month.month_a_hours = sum_pairing_a_hours
                cascade_patch_month.month_a_pay = container_a_position_pay(sum_pairing_a_hours)
                # #===============Reserve NO FLY HOURS 
                cascade_patch_month.month_reserve_no_fly_hours = sum_pairing_reserve_no_fly_hours
                cascade_patch_month.month_reserve_no_fly_pay = tfp_pay_function(sum_pairing_reserve_no_fly_hours)
                # #===============Reserve GUARANTEE HOURS 
                cascade_patch_month.month_guarantee_hours = sum_pairing_guarantee_hours
                cascade_patch_month.month_guarantee_hours_worked_rated = sum_pairing_guarantee_hours_worked_rated
                #============Totals ACTUAL 
                cascade_patch_month.month_total_credits = totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,sum_pairing_vja,sum_pairing_holiday,sum_pairing_time_half,sum_pairing_double_time,sum_pairing_double_half,sum_pairing_triple)
                #============Totals RATED
                cascade_patch_month.month_total_credits_rated= totals(sum_pairing_reserve_no_fly_hours,sum_pairing_tfp,sum_pairing_vacation_sick,one_point_five_rate(sum_pairing_vja),double_rate(sum_pairing_holiday),one_point_five_rate(sum_pairing_time_half),more_better_function_rate(sum_pairing_double_time,2),more_better_function_rate(sum_pairing_double_half,2.5),more_better_function_rate(sum_pairing_triple,3))
                #============Totals PAY
                cascade_patch_month.month_total_pay = totals(tfp_pay_function(sum_pairing_reserve_no_fly_hours),tfp_pay_function(sum_pairing_tfp),tfp_pay_function(sum_pairing_vacation_sick),one_point_five_pay(sum_pairing_vja),double_pay(sum_pairing_holiday),one_point_five_pay(sum_pairing_time_half),more_better_function_pay(sum_pairing_double_time,2),more_better_function_pay(sum_pairing_double_half,2.5),more_better_function_pay(sum_pairing_triple,3), tafb_pay(cascade_patch_pairing.tafb_total),int_tafb_pay(cascade_patch_pairing.int_tafb_total),override_pay(sum_pairing_overrides),container_a_position_pay(sum_pairing_a_hours))
                # #=====================
                db.session.add(cascade_patch_month)
                db.session.commit()
                # THIS IS THE QUERY FOR ALL RELATED MONTHS
                all_cascade_patch_month = Month.query.filter_by(year_id=cascade_patch_month.year_id)
                #========New additions=======
                sum_month_duty_hours = 0
                #=============TAFB
                sum_month_tafb_total = 0
                sum_month_int_tafb_total = 0
                #============REGULAR TFP
                sum_month_tfp = 0
                #============VACATION/SICK
                sum_month_vacation_sick = 0
                #============VJA
                sum_month_vja = 0
                #============HOLIDAY
                sum_month_holiday = 0
                #============time_half
                sum_month_time_half = 0
                #================ DOUBLE TIME LYFE
                sum_month_double_time = 0
                #================ DOUBLE & HALF LYFE
                sum_month_double_half = 0
                #================ TRIPLE LYFE
                sum_month_triple = 0
                #================ OVERRIDES LYFE
                sum_month_overrides = 0
                #================ A-POSITION LYFE
                sum_month_a_hours = 0
                #============Totals
                sum_month_total_credits = 0
                #========Reserve No Fly=======
                sum_month_reserve_no_fly_hours = 0

                #HERE WILL BE A LINE OF FOR/INS THAT WILL TOTAL EACH CAT FOR THE YEAR
                for month in all_cascade_patch_month:
                    # if month.month_guarantee_hours != None:
                    #     sum_month_guarantee_hours += month.month_guarantee_hours
                    # if month.month_guarantee_hours_worked_rated != None:
                    #     sum_month_guarantee_hours_worked_rated += month.month_guarantee_hours_worked_rated
                    if month.month_tafb_total != None:
                        sum_month_tafb_total += month.month_tafb_total
                    if month.month_int_tafb_total != None:
                        sum_month_int_tafb_total += month.month_int_tafb_total
                    if month.month_tfp != None:
                        sum_month_tfp += month.month_tfp
                    if month.month_vacation_sick != None:
                        sum_month_vacation_sick += month.month_vacation_sick
                    if month.month_vja != None:
                        sum_month_vja += month.month_vja
                    if month.month_holiday != None:
                        sum_month_holiday += month.month_holiday
                    if month.month_time_half != None:
                        sum_month_time_half += month.month_time_half
                    if month.month_double_time != None:
                        sum_month_double_time += month.month_double_time
                    if month.month_double_half != None:
                        sum_month_double_half += month.month_double_half
                    if month.month_triple != None:
                        sum_month_triple += month.month_triple
                    if month.month_overrides != None:
                        sum_month_overrides += month.month_overrides
                    if month.month_a_hours != None:
                        sum_month_a_hours += month.month_a_hours
                    if month.month_total_credits != None:
                        sum_month_total_credits += month.month_total_credits
                    if month.month_duty_hours != None:
                        sum_month_duty_hours += month.month_duty_hours
                    if month.month_reserve_no_fly_hours != None:
                        sum_month_reserve_no_fly_hours += month.month_reserve_no_fly_hours

                    #THIS IS THE QUERY FOR THE YEAR WE'RE UPDATING WITH THE MONTHLY TOTALS 
                    cascade_patch_year = Year.query.filter_by(id=cascade_patch_month.year_id).first()
                    #THIS WILL BE LINES WHERE WE ASSIGN VALUE TO YEAR CATS WITH MONTHLY TOTALS
                    #========New additions=======
                    cascade_patch_year.year_duty_hours = sum_month_duty_hours
                    #=============TAFB
                    cascade_patch_year.year_tafb_total = sum_month_tafb_total
                    cascade_patch_year.year_tafb_pay = tafb_pay(sum_month_tafb_total)
                    #=============TAFB INT
                    cascade_patch_year.year_int_tafb = sum_month_int_tafb_total
                    cascade_patch_year.year_int_tafb_pay = int_tafb_pay(sum_month_int_tafb_total)
                    #============VACATION/SICK
                    cascade_patch_year.year_vacation_sick = sum_month_vacation_sick
                    cascade_patch_year.year_vacation_sick_pay = tfp_pay_function(sum_month_vacation_sick)
                    #============REGULAR TFP
                    cascade_patch_year.year_tfp = sum_month_tfp
                    cascade_patch_year.year_tfp_pay = tfp_pay_function(sum_month_tfp)
                    #============VJA
                    cascade_patch_year.year_vja = sum_month_vja
                    cascade_patch_year.year_vja_rated= one_point_five_rate(sum_month_vja)
                    cascade_patch_year.year_vja_pay= one_point_five_pay(sum_month_vja)
                    # #============HOLIDAY
                    cascade_patch_year.year_holiday = sum_month_holiday
                    cascade_patch_year.year_holiday_rated= double_rate(sum_month_holiday)
                    cascade_patch_year.year_holiday_pay= double_pay(sum_month_holiday)
                    #============TIME_HALF
                    cascade_patch_year.year_time_half = sum_month_time_half
                    cascade_patch_year.year_time_half_rated= one_point_five_rate(sum_month_time_half)
                    cascade_patch_year.year_time_half_pay= one_point_five_pay(sum_month_time_half)
                    #============DOUBLE_TIME
                    cascade_patch_year.year_double_time = sum_month_double_time
                    cascade_patch_year.year_double_time_rated= more_better_function_rate(sum_month_double_time,2)
                    cascade_patch_year.year_double_time_pay= more_better_function_pay(sum_month_double_time,2)
                    #============DOUBLE_HALF
                    cascade_patch_year.year_double_half = sum_month_double_half
                    cascade_patch_year.year_double_half_rated= more_better_function_rate(sum_month_double_half,2.5)
                    cascade_patch_year.year_double_half_pay= more_better_function_pay(sum_month_double_half,2.5)
                    #============TRIPLE
                    cascade_patch_year.year_triple = sum_month_triple
                    cascade_patch_year.year_triple_rated= more_better_function_rate(sum_month_triple,3)
                    cascade_patch_year.year_triple_pay= more_better_function_pay(sum_month_triple,3)
                    #============OVERRIDES
                    cascade_patch_year.year_overrides = sum_month_overrides
                    cascade_patch_year.year_overrides_pay = override_pay(sum_month_overrides)
                    #============A-POSITON
                    cascade_patch_year.year_a_hours = sum_month_a_hours
                    cascade_patch_year.year_a_pay = container_a_position_pay(sum_month_a_hours)
                    # # #===============Reserve Nofly HOURS 
                    cascade_patch_year.year_reserve_no_fly_hours = sum_month_reserve_no_fly_hours
                    cascade_patch_year.year_reserve_no_fly_pay = tfp_pay_function(sum_month_reserve_no_fly_hours)
                    # cascade_patch_year.year_guarantee_hours = sum_month_guarantee_hours
                    # cascade_patch_year.year_guarantee_hours_worked_rated = sum_month_guarantee_hours_worked_rated
                    #============Totals ACTUAL 
                    cascade_patch_year.year_total_credits = totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,sum_month_vja,sum_month_holiday,sum_month_time_half,sum_month_double_time,sum_month_double_half,sum_month_triple)
                    #============Totals RATED
                    cascade_patch_year.year_total_credits_rated= totals(sum_month_reserve_no_fly_hours, sum_month_tfp,sum_month_vacation_sick,one_point_five_rate(sum_month_vja),double_rate(sum_month_holiday),one_point_five_rate(sum_month_time_half),more_better_function_rate(sum_month_double_time,2),more_better_function_rate(sum_month_double_half,2.5),more_better_function_rate(sum_month_triple,3))
                    #============Totals PAY
                    cascade_patch_year.year_total_pay = totals(tfp_pay_function(sum_month_reserve_no_fly_hours),tfp_pay_function(sum_month_tfp),tfp_pay_function(sum_month_vacation_sick),one_point_five_pay(sum_month_vja),double_pay(sum_month_holiday),one_point_five_pay(sum_month_time_half),more_better_function_pay(sum_month_double_time,2),more_better_function_pay(sum_month_double_half,2.5),more_better_function_pay(sum_month_triple,3), tafb_pay(sum_month_tafb_total),int_tafb_pay(sum_month_int_tafb_total),override_pay(sum_month_overrides),container_a_position_pay(sum_month_a_hours))
                    # #=====================
                    db.session.add(cascade_patch_year)
                    db.session.commit()
            print('this gonna work?', id_to_use)
            response_dict = {"message": "deleted fo sho!"}
            return response_dict, 200
api.add_resource(CascadeTest, '/cascade_test/<int:id>')

class Login(Resource):
    def post(self):
        data = request.get_json()
        username = data['username']
        password = data['password']
        user = User.query.filter(User.username == username).first()
        if user:
            if user.authenticate(password):
                session['user_id'] = user.id
                return user.to_dict(), 200
        return {'error': 'Unauthorized'}, 401
    
api.add_resource(Login, '/login')

# check session 
class CheckSession(Resource):
    def get(self):
        user = User.query.filter(User.id == session.get('user_id')).first()
        if user:
            return user.to_dict()
        else:
            return {'message': '401: Not Authorized'}, 401

api.add_resource(CheckSession, '/check_session')

# logout
class Logout(Resource):
    def delete(self):
        session['user_id'] = None
        return {'message':'204: User Logged Out'}
api.add_resource(Logout, '/logout')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

