from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.hybrid import hybrid_property

from config import db, bcrypt
# , bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users_table'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable = False)
    user_role = db.Column(db.String, nullable = False)
    email = db.Column(db.String)
    tfp_pay = db.Column(db.Float)
    per_diem_pay = db.Column(db.Float)
    international_per_diem_pay = db.Column(db.Float)
    override_pay = db.Column(db.Float)
    a_postion_pay = db.Column(db.Float)

    _password_hash = db.Column(db.String, nullable=False)
    # =================RELATIONSHIPS=====================================
    years_field = relationship('Year', back_populates='users_field', cascade = 'all, delete')
    # =================SERIALIZER RULES==================================
    serialize_rules = ( '-months_field', '-pairings_field', '-days_field')

    #===========bcrypt shit==============================================
    @hybrid_property
    def password_hash(self):
        return self._password_hash

    @password_hash.setter
    def password_hash(self, password):
        # utf-8 encoding and decoding is required in python 3
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
class Year(db.Model, SerializerMixin):
    __tablename__ = 'years_table'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)


    year_tfp = db.Column(db.Float)
    year_vja= db.Column(db.Float)
    year_holiday = db.Column(db.Float)
    year_time_half = db.Column(db.Float)
    year_double_time = db.Column(db.Float)
    year_double_half = db.Column(db.Float)
    year_triple = db.Column(db.Float)
    year_overrides = db.Column(db.Integer)
    year_a_hours = db.Column(db.Float)
    year_tafb_total = db.Column(db.Float)
    year_int_tafb_total = db.Column(db.Float)
    year_duty_hours = db.Column(db.Float)
    year_vacation_sick = db.Column(db.Float)

# =================RELATIONSHIPS=======================================
    user_id = db.Column(db.Integer, db.ForeignKey('users_table.id'))
    users_field = relationship('User', back_populates='years_field')

    months_field = relationship('Month', back_populates="years_field", cascade='all, delete')
# =================SERIALIZER RULES====================================
    serialize_rules = ('-users_field',  '-pairings_field','-days_field',)
    
class Month(db.Model, SerializerMixin):
    __tablename__ = 'months_table'
    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.String)
    year = db.Column(db.Integer)
    guarantee_hours = db.Column(db.Float)

    #================TOTALS===================
    month_tfp = db.Column(db.Float)
    month_vja= db.Column(db.Float)
    month_holiday = db.Column(db.Float)
    month_time_half = db.Column(db.Float)
    month_double_time = db.Column(db.Float)
    month_double_half = db.Column(db.Float)
    month_triple = db.Column(db.Float)
    month_overrides = db.Column(db.Integer)
    month_a_hours = db.Column(db.Float)
    month_tafb_total = db.Column(db.Float)
    month_int_tafb_total = db.Column(db.Float)
    month_duty_hours = db.Column(db.Float)
    month_vacation_sick = db.Column(db.Float)


    # =================RELATIONSHIPS=======================================
    year_id = db.Column(db.Integer, db.ForeignKey('years_table.id'))
    years_field = relationship('Year', back_populates='months_field')

    pairings_field = relationship('Pairing', back_populates='months_field', cascade = 'all, delete')
    # =================SERIALIZER RULES====================================
    serialize_rules = ('-years_field','-users_field', '-days_field')

    def __repr__(self):
        return f"<Month(id={self.id}, month='{self.month}', year_id = {self.year_id})>"


class Pairing(db.Model, SerializerMixin):
    __tablename__ = 'pairings_table'
    id = db.Column(db.Integer, primary_key=True)
    pairing_name = db.Column(db.String)
    tafb_total = db.Column(db.Float)
    int_tafb_total = db.Column(db.Float)
    reserve_block = db.Column(db.Boolean)
    #================TOTALS===================
    pairing_tfp = db.Column(db.Float)
    pairing_vja= db.Column(db.Float)


    pairing_holiday = db.Column(db.Float)


    pairing_time_half = db.Column(db.Float)
    pairing_double_time = db.Column(db.Float)
    pairing_double_half = db.Column(db.Float)
    pairing_triple = db.Column(db.Float)
    pairing_overrides = db.Column(db.Integer)
    pairing_a_hours = db.Column(db.Float)

    pairing_duty_hours = db.Column(db.Float)
    pairing_vacation_sick = db.Column(db.Float)

    # =================RELATIONSHIPS=======================================
    month_id = db.Column(db.Integer, db.ForeignKey('months_table.id'))
    months_field = relationship('Month', back_populates='pairings_field')

    days_field = relationship('Day', back_populates='pairings_field', cascade = 'all, delete')
    # =================SERIALIZER RULES====================================
    serialize_rules = ('-years_field','-months_field', '-users_field')

    def __repr__(self):
        return f"<Pairing(id={self.id}, pairing_name='{self.pairing_name}', month_id = {self.month_id})>"

class Day(db.Model, SerializerMixin):
    __tablename__ = 'days_table'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)
    #==========hours at diff rates
    #============REGULAR TFP
    total_tfp = db.Column(db.Float)
    total_tfp_pay = db.Column(db.Float)
    #============VACATION/SICK
    vacation_sick = db.Column(db.Float)
    vacation_sick_pay = db.Column(db.Float)
    #============VJA
    vja= db.Column(db.Float)
    vja_rated = db.Column(db.Float)
    vja_pay= db.Column(db.Float)
    #============HOLIDAY
    holiday = db.Column(db.Float)
    holiday_rated = db.Column(db.Float)
    holiday_pay = db.Column(db.Float)
    #============TIME_HALF
    time_half = db.Column(db.Float)
    time_half_rated = db.Column(db.Float)
    time_half_pay = db.Column(db.Float)
    #============DOUBLE_TIME
    double_time = db.Column(db.Float)
    double_time_rated = db.Column(db.Float)
    double_time_pay = db.Column(db.Float)
    #============DOUBLE_HALF
    double_half = db.Column(db.Float)
    double_half_rated = db.Column(db.Float)
    double_half_pay = db.Column(db.Float)
    #============TRIPLE
    triple = db.Column(db.Float)
    triple_rated = db.Column(db.Float)
    triple_pay = db.Column(db.Float)
    #============OVERRIDES
    overrides = db.Column(db.Integer)
    overrides_pay = db.Column(db.Float)
    #============A-POSITON
    a_position = db.Column(db.Boolean)
    a_hours = db.Column(db.Float)
    a_pay = db.Column(db.Float)
    #============Totals
    total_credits = db.Column(db.Float)
    total_credits_rated = db.Column(db.Float)
    total_pay = db.Column(db.Float)
    #========New additions=======
    reserve_no_fly = db.Column(db.Boolean)
    daily_duty_hours = db.Column(db.Float)
    comments = db.Column(db.String)
    type_of_day =  db.Column(db.String)
    
    
    # =================RELATIONSHIPS=======================================
    pairing_id = db.Column(db.Integer, db.ForeignKey('pairings_table.id'))
    pairings_field = relationship('Pairing', back_populates='days_field')
    # =================SERIALIZER RULES====================================
    serialize_rules = ('-years_field','-months_field', '-users_field', '-pairings_field')
    
    

    
    
