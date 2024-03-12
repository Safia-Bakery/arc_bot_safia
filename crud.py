from sqlalchemy.orm import Session
import models
import pytz
from typing import Optional
import requests
from sqlalchemy.sql import func
from sqlalchemy import or_,and_,Date,cast
from datetime import datetime 
timezonetash = pytz.timezone("Asia/Tashkent")

def getlistbrigada(db:Session,sphere_status,department):
    query = db.query(models.Brigada).filter(models.Brigada.sphere_status==sphere_status,models.Brigada.status==1,models.Brigada.department==department).all()
    return query


def get_request(db:Session,id):
    query = db.query(models.Requests).filter(models.Requests.id==id).first()
    return query

def accept_request(db:Session,id,brigada_id,user_manager):
    query = db.query(models.Requests).filter(models.Requests.id==id).first()
    if query:
        query.status=1
        query.brigada_id = brigada_id
        query.started_at = datetime.now(timezonetash)
        query.user_manager=user_manager
        db.commit()
        db.refresh(query)
        updated_data = query.update_time or {}
        updated_data[str(1)] = str(datetime.now(tz=timezonetash))
        query.update_time= updated_data
        db.query(models.Requests).filter(models.Requests.id==id).update({'update_time':updated_data})
        db.commit()
        return query
    else:
        return False


def reject_request(db:Session,status,id):
    query = db.query(models.Requests).filter(models.Requests.id==id).first()
    query.status=status
    query.finished_at = datetime.now(timezonetash)
    db.commit()
    db.refresh(query)
    updated_data = query.update_time or {}
    updated_data[str(status)] = str(datetime.now(tz=timezonetash))
    query.update_time= updated_data
    db.query(models.Requests).filter(models.Requests.id==id).update({'update_time':updated_data})
    db.commit()
    return query


def get_brigada_id(db:Session,id):
    query = db.query(models.Brigada).filter(models.Brigada.id==id).first()
    return query


def get_user_tel_id(db:Session,id):
    query = db.query(models.Users).filter(models.Users.telegram_id==id).first()
    return query


def create_user(db:Session,full_name,telegram_id,sphere_status,phone_number,username):
    db_add_request = models.Users(full_name=full_name,telegram_id=telegram_id,phone_number=phone_number,sphere_status=sphere_status,username=username)
    db.add(db_add_request)
    db.commit()
    db.refresh(db_add_request)
    return db_add_request



#origin is the thing just like a if sklad or bar something like this if it type is 1 it is arc elif somthing like thi
def get_branch_list(db:Session,sphere_status):
    return db.query(models.ParentFillials).join(models.Fillials).filter(models.ParentFillials.status==1,models.Fillials.origin==sphere_status).order_by(models.ParentFillials.name).all()



def getfillialchildfabrica(db:Session,offset):
    query = db.query(models.Fillials).join(models.ParentFillials).filter(models.ParentFillials.is_fabrica==1).limit(70).offset(offset).all()
    return query


def get_branch_list_location(db:Session):
    return db.query(models.ParentFillials).filter(models.ParentFillials.status==1).order_by(models.ParentFillials.name).all()


def get_category_list(db:Session,sphere_status,department,sub_id:Optional[int]=None):
    query = db.query(models.Category)
    if sphere_status is not None:
        query = query.filter(models.Category.sphere_status==sphere_status)
    if sub_id is not None:
        query  = query.filter(models.Category.sub_id==sub_id)
    query = query.filter(models.Category.parent_id==None)
    
    query = query.filter(models.Category.status==1,models.Category.department==department).order_by(models.Category.name).all()
    return query



def getcategoryname(db:Session,name,department:Optional[int]=None):
    query = db.query(models.Category).filter(models.Category.name==name)
    if department is not None:
        query = query.filter(models.Category.department==department)
    return query.first()


def getchildbranch(db:Session,fillial,type,factory):
    query = db.query(models.Fillials).join(models.ParentFillials)
    if factory == 1:
        if type==1:
            query = query.filter(models.ParentFillials.name.like(f"%{fillial}%"),models.Fillials.origin==1)
        else:
            query = query.filter(models.ParentFillials.name.like(f"%{fillial}%"))
        query = query.first()
    elif factory==2:
        query = query.filter(models.Fillials.name.like(f"%{fillial}%")).first()
    return query

def add_request(db:Session,category_id,fillial_id,description,user_id,is_bot,product:Optional[str]=None):
    db_add_request = models.Requests(category_id=category_id,description=description,fillial_id = fillial_id,product=product,user_id=user_id,is_bot=is_bot,update_time = {'0':str(datetime.now(tz=timezonetash))})
    db.add(db_add_request)
    db.commit()
    db.refresh(db_add_request)
    return db_add_request


def add_car_request(db:Session,category_id,fillial_id,user_id,size,time_delivery,comment,location):
    db_add_request = models.Requests(category_id=category_id,fillial_id=fillial_id,arrival_date=time_delivery,user_id=user_id,size=size,is_bot=1,description=comment,location=location,update_time = {'0':str(datetime.now(tz=timezonetash))})
    db.add(db_add_request)
    db.commit()
    db.refresh(db_add_request)
    return db_add_request



def add_it_request(db:Session,category_id,fillial_id,user_id,size,finishing_time,comment):
    db_add_request = models.Requests(category_id=category_id,fillial_id=fillial_id,user_id=user_id,size=size,is_bot=1,finishing_time=finishing_time,description=comment,update_time = {'0':str(datetime.now(tz=timezonetash))})
    db.add(db_add_request)
    db.commit()
    db.refresh(db_add_request)
    return db_add_request



def add_meal_request(db:Session,fillial_id,user_id,meal_size,bread_size,time_delivery,category_id):
    db_add_request = models.Requests(category_id=category_id,fillial_id=fillial_id,user_id=user_id,arrival_date=time_delivery,bread_size=bread_size,size=meal_size,update_time ={'0':str(datetime.now(tz=timezonetash))})
    db.add(db_add_request)
    db.commit()
    db.refresh(db_add_request)
    return db_add_request


def create_files(db:Session,request_id,filename,status:Optional[int]=0):
    db_add_file = models.Files(request_id=request_id,url=filename,status=status)
    db.add(db_add_file)
    db.commit()
    db.refresh(db_add_file)
    return db_add_file



def tg_get_request_list(db:Session,brigada_id):
    query = db.query(models.Requests).filter(and_(models.Requests.brigada_id==brigada_id,models.Requests.status.in_([1,2]))).all()
    return query


def get_request_id(db:Session,id):
    return db.query(models.Requests).filter(models.Requests.id==id).first()


def tg_update_requst_st(db:Session,requestid,status):
    query = db.query(models.Requests).filter(models.Requests.id==requestid).first()
    if status == 3 or status == 6:
        query.finished_at = datetime.now(timezonetash)
    query.status = status
    db.commit() 
    db.refresh(query)
    updated_data = query.update_time or {}
    updated_data[str(status)] = str(datetime.now(tz=timezonetash))
    db.query(models.Requests).filter(models.Requests.id==query.id).update({'update_time':updated_data})
    db.commit()
    return query


def getfillialname(db:Session,name):
    query = db.query(models.ParentFillials).filter(models.ParentFillials.name==name).first()
    return query


def update_user_sphere(db:Session,tel_id,sphere_status):
    query = db.query(models.Users).filter(models.Users.telegram_id==tel_id).first()
    query.sphere_status=sphere_status
    db.commit()
    db.refresh(query)
    return query

def addcomment(db:Session,user_id,comment,request_id):
    query = models.Comments(user_id=user_id,request_id=request_id,comment=comment)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_work_time(db:Session):
    query = db.query(models.Working).first()
    return query

def get_category_department(db:Session,department_id):
    query = db.query(models.Category).filter(models.Category.department==department_id).first()
    return query

def get_user_role(db:Session,telegram_id):
    query = db.query(models.Groups).join(models.Users).join(models.Roles).filter(models.Users.telegram_id==telegram_id,models.Roles.page_id==64).first()
    return query

def get_products(db:Session,category):
    query = db.query(models.Products).join(models.Category).filter(models.Category.name.ilike(f"%{category}%")).all()
    return query

def get_product_by_name(db:Session,name):
    query = db.query(models.Products).filter(models.Products.name.ilike(f"%{name}%")).first()
    return query
def create_order_product(db:Session,product_id,amount,order_id):
    query = models.OrderProducts(product_id=product_id,amount=amount,request_id=order_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def add_comment_request(db:Session,comment,category_id,name,user_id,fillial_id):
    query = models.Requests(description=comment,category_id=category_id,product=name,user_id=user_id,fillial_id=fillial_id)
    db.add(query)
    db.commit()
    db.refresh(query)
    return query



def add_video_request(db:Session,comment, category_id,fillial_id, user_id,vidfrom,vidto):
    query = models.Requests(description=comment,category_id=category_id,user_id=user_id,fillial_id=fillial_id,update_time={'vidfrom':vidfrom,'vidto':vidto})
    db.add(query)
    db.commit()
    db.refresh(query)
    return query

def get_child_categories(db:Session,category_id):
    query = db.query(models.Category).filter(models.Category.parent_id==category_id,models.Category.status==1).order_by(models.Category.name).all()
    return query


#def get_category_sphere(db:Session,name,sphere_status):
#    query = db.query(models.Category).filter(models.Category.name.ilike(f"%{name}%"),models.Category.sphere_status==sphere_status).first()
#    return query
