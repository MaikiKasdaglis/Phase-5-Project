#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, make_response, session
from flask_restful import Resource


# Local imports
from config import app, db, api
# Add your model imports
from models import User, Month, Pairing, Day, Year


# Views go here!

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

                year_tfp = request_obj["year_tfp"],
                year_vja= request_obj["year_vja"],
                year_holiday = request_obj["year_holiday"],
                year_time_half = request_obj["year_time_half"],
                year_double_time = request_obj["year_double_time"],
                year_double_half = request_obj["year_double_half"],
                year_triple = request_obj["year_triple"],
                year_overrides = request_obj["year_overrides"],
                year_a_hours = request_obj["year_a_hours"],
                year_tafb_total = request_obj["year_tafb_total"],
                year_int_tafb_total = request_obj["year_int_tafb_total"],
                year_duty_hours = request_obj["year_duty_hours"],
                year_vacation_sick = request_obj["year_vacation_sick"]
            )
            db.session.add(new_year)
            db.session.commit()
            # Create associated months
            month_names = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
            for month in range(1, 13):
                new_month = Month(
                    month=month_names[month-1],
                    year=new_year.year,
                    guarantee_hours=0,
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
                            date=day_names[day-1],
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
                    db.session.add(response_obj)
                    db.session.commit
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
                guarantee_hours = request_obj["guarantee_hours"],
                year_id = request_obj["year_id"],

                month_tfp = request_obj["month_tfp"],
                month_vja= request_obj["month_vja"],
                month_holiday = request_obj["month_holiday"],
                month_time_half = request_obj["month_time_half"],
                month_double_time = request_obj["month_double_time"],
                month_double_half = request_obj["month_double_half"],
                month_triple = request_obj["month_triple"],
                month_overrides = request_obj["month_overrides"],
                month_a_hours = request_obj["month_a_hours"],
                month_tafb_total = request_obj["month_tafb_total"],
                month_int_tafb_total = request_obj["month_int_tafb_total"],
                month_duty_hours = request_obj["month_duty_hours"],
                month_vacation_sick = request_obj["month_vacation_sick"]
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
                    db.session.add(response_obj)
                    db.session.commit
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

# functions
# def total_week(newPair):
#     n = Day.query.filter_by(pairing_id = newPair)
#     total = 0
#     print(n)
#     for day in n:
#         total += day.total_tfp
#     print(total)
#     return total


class Pairings(Resource):
    def get(self):
        pairings =[p.to_dict() for p in Pairing.query.all()]
        return make_response(pairings, 200)
    def post(self):
        request_obj = request.get_json()
        try:
            new_pairing = Pairing(
                pairing_name = request_obj["pairing_name"],
                tafb_total = request_obj["tafb_total"],
                int_tafb_total = request_obj["int_tafb_total"],
                reserve_block = request_obj["reserve_block"],
                month_id = request_obj["month_id"],

                pairing_tfp = request_obj["pairing_tfp"],
                pairing_vja = request_obj["pairing_vja"],
                pairing_holiday = request_obj["pairing_holiday"],
                pairing_time_half = request_obj["pairing_time_half"],
                pairing_double_time = request_obj["pairing_double_time"],
                pairing_double_half = request_obj["pairing_double_half"],
                pairing_triple = request_obj["pairing_triple"],
                pairing_overrides = request_obj["pairing_overrides"],
                pairing_a_hours = request_obj["pairing_a_hours"],
                pairing_duty_hours = request_obj["pairing_duty_hours"],
                pairing_vacation_sick = request_obj["pairing_vacation_sick"],
                
            )
            db.session.add(new_pairing)
            db.session.commit()
            # new_pairing.pairing_tfp = total_week(new_pairing.id)
            # db.session.add(new_pairing)
            # db.session.commit()
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
                for attr in request_object:
                    setattr(response_obj, attr, request_object[attr])
                    db.session.add(response_obj)
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
            db.session.delete(response_obj)
            db.session.commit()
            response_dict = {"message": "deleted fo sho!"}
            return response_dict, 200
api.add_resource(PairingsById, '/pairings/<int:id>')




# region Day Math Functions
#======================DAY MATH========================================
def tfp_pay_function(total_tfp):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = user.tfp_pay * total_tfp
    print(total) 
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
#===========================A_Pay and Overrides=========================
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

def override_pay(overrides):
    user = User.query.filter(User.id == session.get('user_id')).first()
    total = user.override_pay * overrides
    return total 
#===========================Totals=========================
def totals(*hours):
    sum = 0 
    for n in hours:
        sum = sum + n
    return sum
#=====================================================================
# endregion
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
                holiday_rated = one_point_five_rate(request_obj["holiday"]),
                holiday_pay = one_point_five_pay(request_obj["holiday"]),
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
                total_credits_rated = totals(request_obj["total_tfp"],request_obj["vacation_sick"],one_point_five_rate(request_obj["vja"]),one_point_five_rate(request_obj["holiday"]),one_point_five_rate(request_obj["time_half"]),double_rate(request_obj["double_time"]),double_point_five_rate(request_obj["double_half"]),triple_rate(request_obj["triple"])),
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
                    response_obj.holiday_rated = one_point_five_rate(request_object["holiday"])
                    response_obj.holiday_pay = one_point_five_pay(request_object["holiday"])
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

                #============Totals ACTUAL 
                response_obj.total_credits = totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"])
                # request_object["total_credits"] = response_obj.total_credits  # Add this line
                #============Totals RATED
                response_obj.total_credits_rated = totals(request_object["total_tfp"],request_object["vacation_sick"],one_point_five_rate(request_object["vja"]),one_point_five_rate(request_object["holiday"]),one_point_five_rate(request_object["time_half"]),double_rate(request_object["double_time"]),double_point_five_rate(request_object["double_half"]),triple_rate(request_object["triple"]))
                # request_object["total_credits_rated"] = response_obj.total_credits_rated  # Add this line
                #============Totals PAY
                response_obj.total_pay = totals(tfp_pay_function(request_object["total_tfp"]),tfp_pay_function(request_object["vacation_sick"]),one_point_five_pay(request_object["vja"]),one_point_five_pay(request_object["holiday"]),one_point_five_pay(request_object["time_half"]),double_pay(request_object["double_time"]),double_point_five_pay(request_object["double_half"]),triple_pay(request_object["triple"]),override_pay(request_object["overrides"]),a_position_pay(request_object["a_position"],totals(request_object["total_tfp"],request_object["vacation_sick"],request_object["vja"],request_object["holiday"],request_object["time_half"],request_object["double_time"],request_object["double_half"],request_object["triple"])))
                # request_object["total_pay"] = response_obj.total_pay  # Add this line
                db.session.add(response_obj)
                db.session.commit()


                all_days = Day.query.filter_by(pairing_id=response_obj.pairing_id)
                # print("all days" , all_days)
                total = 0
                for days in all_days:
                    if days.total_pay != None:
                        total += days.total_pay
                    print(days.total_pay)
                    print(days.date)
                print(total)
                
                cascade_patch_pairing = Pairing.query.filter_by(id=response_obj.pairing_id).first()
                print("this it the pairing", cascade_patch_pairing)



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

