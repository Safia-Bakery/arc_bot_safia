from sqlalchemy.orm import Session
import models
import pytz
from typing import Optional
import requests
from sqlalchemy.sql import func
from sqlalchemy import or_,and_,Date,cast
from datetime import datetime, timedelta
from database import SessionLocal
timezonetash = pytz.timezone("Asia/Tashkent")


class CommitDb():
    def insert_data(self,db:Session,data):
        try:
            db.add(data)
            db.commit()
            db.refresh(data)
            return data
        except Exception as e:
            print(e)
            db.rollback()
            return False

    def update_data(self,db:Session,data):
        try:
            db.commit()
            db.refresh(data)
            return data
        except Exception as e:
            # print(e)
            db.rollback()
            return False

    def delete_data(self,db:Session,data):

        try:
            db.delete(data)
            db.commit()
            return data
        except:
            db.rollback()
            return False

    def get_data(self,db:Session,data):
        try:
            return data
        except:
            return False
        finally:
            #db.close()
            return True



def update_expenditures(request_id):
    with SessionLocal() as db:
        query = db.query(models.Expanditure).filter(models.Expanditure.request_id == request_id).all()
        for exp in query:
            exp.status = 0
            db.commit()


def create_expanditure(amount, tool_id, request_id, status: Optional[int] = 0):
    with SessionLocal() as db:
        query = models.Expanditure(
            amount=amount,
            tool_id=tool_id,
            request_id=request_id,
            status=status
        )
        db.add(query)
        db.commit()
        db.refresh(query)

    return query


def getlistbrigada(sphere_status,department):
    with SessionLocal() as db:
        query = db.query(models.Brigada).filter(models.Brigada.status==1,models.Brigada.department==department)
        if sphere_status is not None:
            query = query.filter(models.Brigada.sphere_status==sphere_status)
        query = query.all()
        CommitDb().get_data(db,query)
        return query


def get_request(id):
    with SessionLocal() as db:
        query = db.query(models.Requests).filter(models.Requests.id==id).first()
        CommitDb().get_data(db,query)
        query.category_sphere_status = query.category.sphere_status
        query.category_department = query.category.department
        query.category_name = query.category.name
        query.fillial_name = query.fillial.name
        query.parentfillial_name = query.fillial.parentfillial.name
        query.expanditures = query.expanditure
        query.user_telegram_id = query.user.telegram_id
        query.user_full_name = query.user.full_name

        return query

def accept_request(id,brigada_id,user_manager):
    with SessionLocal() as db:

        query = db.query(models.Requests).filter(models.Requests.id==id).first()
        if query:
            query.status=1
            query.brigada_id = brigada_id
            query.started_at = datetime.now(timezonetash)
            query.user_manager=user_manager
            CommitDb().update_data(db,query)
            query.user_telegram_id = query.user.telegram_id
            query.user_fullname = query.user.full_name
            query.brigada_name = query.brigada.name
            query.brigada_telegram_id = query.brigada.user[0].telegram_id
            query.brigada_id = query.brigada.id
            query.parentfillial_name = query.fillial.parentfillial.name
            query.fillial_name = query.fillial.name
            query.category_department = query.category.department
            with SessionLocal() as db:
                updated_data = query.update_time or {}
                updated_data[str(1)] = str(datetime.now(tz=timezonetash))
                query.update_time= updated_data
                db.query(models.Requests).filter(models.Requests.id==id).update({'update_time':updated_data})
                CommitDb().update_data(db,query)

            return query
        else:
            return False


def reject_request(status,id):
    with SessionLocal() as db:
        query = db.query(models.Requests).filter(models.Requests.id==id).first()
        query.status=status
        query.finished_at = datetime.now(timezonetash)
        CommitDb().update_data(db,query)
        query.user_telegram_id = query.user.telegram_id

        with SessionLocal() as db:
            updated_data = query.update_time or {}
            updated_data[str(status)] = str(datetime.now(tz=timezonetash))
            query.update_time= updated_data
            db.query(models.Requests).filter(models.Requests.id==id).update({'update_time':updated_data})
            CommitDb().update_data(db,query)

            return query




def get_brigada_id(id):
    with SessionLocal() as db:
        query = db.query(models.Brigada).filter(models.Brigada.id==id).first()
        CommitDb().get_data(db,query)
        return query


def get_user_tel_id(id):
    with SessionLocal() as db:
        query = db.query(models.Users).filter(models.Users.telegram_id==id).first()
        CommitDb().get_data(db,query)
        if query:
            if query.brigada_id:
                query.brigada_name = query.brigader.name

        return query


def create_user(full_name,telegram_id,sphere_status,phone_number,username):
    with SessionLocal() as db:

        db_add_request = models.Users(full_name=full_name,telegram_id=telegram_id,phone_number=phone_number,sphere_status=sphere_status,username=username)
        CommitDb().insert_data(db,db_add_request)
        return db_add_request




#origin is the thing just like a if sklad or bar something like this if it type is 1 it is arc elif somthing like thi
def get_branch_list(sphere_status):
    with SessionLocal() as db:
        query =db.query(models.ParentFillials).join(models.Fillials).filter(models.ParentFillials.status==1,models.Fillials.origin==sphere_status).order_by(models.ParentFillials.name).all()
        CommitDb().get_data(db,query)
        return query



def getfillialchildfabrica(offset):
    with SessionLocal() as db:
        query = db.query(models.Fillials).join(models.ParentFillials).filter(models.ParentFillials.is_fabrica==1).limit(70).offset(offset).all()
        CommitDb().get_data(db,query)
        return query


def get_branch_list_location():
    with SessionLocal() as db:
        query = db.query(models.ParentFillials).join(models.Fillials).filter(models.ParentFillials.status==1).order_by(models.ParentFillials.name).all()
        CommitDb().get_data(db,query)
        return query



def get_category_list(department,sub_id:Optional[int]=None,sphere_status:Optional[int]=None):
    with SessionLocal() as db:
        query = db.query(models.Category)
        if sphere_status is not None:
            query = query.filter(models.Category.sphere_status==sphere_status)
        if sub_id is not None:
            query  = query.filter(models.Category.sub_id==sub_id)
        query = query.filter(models.Category.parent_id==None)

        query = query.filter(models.Category.status==1,models.Category.department==department).order_by(models.Category.name).all()
        CommitDb().get_data(db,query)
        return query


def get_child_category(parent_id):
    with SessionLocal() as db:
        parent = db.query(models.Category).filter(models.Category.id == parent_id)
        childs = db.query(models.Category).filter(models.Category.parent_id == parent_id).filter(models.Category.status == 1)
        if len(childs.all()) > 0:
            result = parent.union(childs).all()
            CommitDb().get_data(db, result)
            return result
        return False


def getcategoryname(name,department:Optional[int]=None):
    with SessionLocal() as db:
        query = db.query(models.Category).filter(models.Category.name==name)
        if department is not None:
            query = query.filter(models.Category.department==department)
        query = query.filter(models.Category.status==1).first()
        CommitDb().get_data(db,query)
        return query


def getchildbranch(fillial,type,factory):
    with SessionLocal() as db:
        query = db.query(models.Fillials).join(models.ParentFillials)
        if factory == 1:
            if type==1:
                query = query.filter(models.ParentFillials.name.like(f"%{fillial}%"),models.Fillials.origin==1)
            else:
                query = query.filter(models.ParentFillials.name.like(f"%{fillial}%"))
            query = query.first()
        elif factory==2:
            query = query.filter(models.Fillials.name.like(f"%{fillial}%")).first()
        CommitDb().get_data(db,query)
        query.name = query.name
        query.parent_fillial = query.parentfillial.name
        return query

def add_request(category_id,fillial_id,description,user_id,is_bot,product:Optional[str]=None,phone_number:Optional[str]=None,finishing_time:Optional[datetime]=None):
    with SessionLocal() as db:

        db_add_request = models.Requests(phone_number=phone_number,category_id=category_id,description=description,fillial_id = fillial_id,product=product,user_id=user_id,is_bot=is_bot,finishing_time=finishing_time,update_time = {'0':str(datetime.now(tz=timezonetash))})
        query = CommitDb().insert_data(db,db_add_request)
        query.category_sphere_status  = query.category.sphere_status
        query.category_department = query.category.department
        query.category_name = query.category.name
        query.fillial_name = query.fillial.name
        query.parentfillial_name = query.fillial.parentfillial.name
        query.manager_name = query.fillial.manager.name if query.fillial.manager else ' '
        query.client_name = query.user.full_name
        query.sla = query.category.ftime
        if query.category.telegram:

            query.category_telegram = query.category.telegram.chat_id
        else:
            query.category_telegram = None
        return query


def add_car_request(category_id,fillial_id,user_id,size,time_delivery,comment,location):
    with SessionLocal() as db:
        db_add_request = models.Requests(category_id=category_id,fillial_id=fillial_id,arrival_date=time_delivery,user_id=user_id,size=size,is_bot=1,description=comment,location=location,update_time = {'0':str(datetime.now(tz=timezonetash))})
        CommitDb().insert_data(db,db_add_request)
        db_add_request.user_phonenumber = db_add_request.user.phone_number
        db_add_request.user_fullname = db_add_request.user.full_name
        db_add_request.category_name = db_add_request.category.name
        if db_add_request.fillial:
            db_add_request.fillial_name = db_add_request.fillial.name
            db_add_request.parentfillial_name = db_add_request.fillial.parentfillial.name

        return db_add_request



def add_it_request(category_id,fillial_id,user_id,size,finishing_time,comment,phone_number):
    with SessionLocal() as db:
        db_add_request = models.Requests(
            category_id=category_id,
            fillial_id=fillial_id,
            user_id=user_id,
            size=size,
            is_bot=1,
            finishing_time=finishing_time,
            phone_number=phone_number,
            description=comment,
            update_time={'0': str(datetime.now(tz=timezonetash))}
        )
        db_add_request = CommitDb().insert_data(db,db_add_request)
        db_add_request.user_phonenumber = db_add_request.user.phone_number
        db_add_request.user_fullname = db_add_request.user.full_name
        db_add_request.category_name = db_add_request.category.name
        if db_add_request.fillial:
            db_add_request.fillial_name = db_add_request.fillial.name
        if db_add_request.category.telegram is not None:
            db_add_request.chat_id =db_add_request.category.telegram.chat_id
        else:
            db_add_request.chat_id = None
        return db_add_request


def update_it_request(
        id,
        message_id: Optional[int] = None,
        brigada_id: Optional[int] = None,
        status: Optional[int] = None,
        deny_reason: Optional[str] = None,
        category_id: Optional[int] = None
    ):
    with SessionLocal() as db:
        query = db.query(models.Requests).filter(models.Requests.id == id).first()
        if message_id is not None:
            query.tg_message_id = message_id
        if brigada_id is not None:
            query.brigada_id = brigada_id

        now = datetime.now(tz=timezonetash)
        if status is not None:
            query.status = status
            updated_data = query.update_time or {}
            updated_data[str(status)] = str(now)
            query.update_time = updated_data
            if status == 1:
                query.started_at = now
            elif status in [4, 6, 8]:
                query.finished_at = now
            db.query(models.Requests).filter(models.Requests.id == id).update({"update_time": updated_data})
        if deny_reason is not None:
            query.deny_reason = deny_reason
        if category_id is not None:
            db.query(models.Requests).filter(models.Requests.id == id).update({"category_id": category_id})
            query.finishing_time = (query.created_at + timedelta(hours=query.category.ftime)) if query.category.ftime is not None else None

        query = CommitDb().update_data(db, query)
        user_of_brigada = db.query(models.Users).filter(models.Users.brigada_id == query.brigada_id).first()
        if status is not None:
            create_log(request_id=id, status=status, user_id=user_of_brigada.id)

        query.category_name = query.category.name if query.category else None
        query.fillial_name = query.fillial.name if query.fillial else None
        query.parentfillial_name = query.fillial.parentfillial.name if query.fillial else None
        query.category_department = query.category.department if query.category else None
        query.category_sphere_status = query.category.sphere_status if query.category else None
        query.user_full_name = query.user.full_name if query.user else None
        query.user_phone_number = query.user.phone_number if query.user else None
        query.user_telegram_id = query.user.telegram_id if query.user else None
        query.user_id = query.user.id if query.user else None
        query.category_sub_id = query.category.sub_id if query.category else None
        query.sla = query.category.ftime if query.category else None
        query.brigada_name = query.brigada.name if query.brigada else None
        query.file_url = query.file[0].url if query.file else None
        query.topic_id = query.brigada.topic_id if query.brigada else None

        return query


def add_meal_request(fillial_id,user_id,meal_size,bread_size,time_delivery,category_id):
    with SessionLocal() as db:
        db_add_request = models.Requests(category_id=category_id,fillial_id=fillial_id,user_id=user_id,arrival_date=time_delivery,bread_size=bread_size,size=meal_size,update_time ={'0':str(datetime.now(tz=timezonetash))})
        CommitDb().insert_data(db,db_add_request)
        return db_add_request


def create_files(request_id,filename,status:Optional[int]=0):
    with SessionLocal() as db:
        db_add_file = models.Files(request_id=request_id,url=filename,status=status)
        CommitDb().insert_data(db,db_add_file)
        return db_add_file



def tg_get_request_list(brigada_id):
    db = SessionLocal()
    query = db.query(models.Requests).filter(and_(models.Requests.brigada_id==brigada_id,models.Requests.status.in_([1,2]))).all()
    CommitDb().get_data(db,query)
    return query


def get_request_id(id):
    with SessionLocal() as db:
        query = db.query(models.Requests).filter(models.Requests.id==id).first()
        CommitDb().get_data(db,query)
        query.category_name = query.category.name if query.category else None
        query.fillial_name = query.fillial.name if query.fillial else None
        query.parentfillial_name = query.fillial.parentfillial.name if query.fillial else None
        query.category_department = query.category.department if query.category else None
        query.category_sphere_status = query.category.sphere_status if query.category else None
        query.user_full_name = query.user.full_name if query.user else None
        query.user_phone_number = query.user.phone_number if query.user else None
        query.user_telegram_id = query.user.telegram_id if query.user else None
        query.user_id = query.user.id if query.user else None
        query.category_sub_id = query.category.sub_id if query.category else None
        query.sla = query.category.ftime if query.category else None
        query.brigada_name = query.brigada.name if query.brigada else None
        query.file_url = query.file[0].url if query.file else None
        query.topic_id = query.brigada.topic_id if query.brigada else None

        return query


def tg_update_requst_st(requestid,status):
    with SessionLocal() as db:
        query = db.query(models.Requests).filter(models.Requests.id==requestid).first()
        if status == 3 or status == 6:
            query.finished_at = datetime.now(timezonetash)
        query.status = status
        CommitDb().update_data(db,query)
        query.category_name = query.category.name
        query.category_department = query.category.department
        query.category_sphere_status = query.category.sphere_status
        query.user_id = query.user.id
        query.category_sub_id = query.category.sub_id
        query.user_full_name = query.user.full_name
        query.user_telegram_id = query.user.telegram_id
        query.parentfillial_name = query.fillial.parentfillial.name if query.fillial else None
        query.user_phone_number = query.user.phone_number if query.user else None
        query.sla = query.category.ftime if query.category else None
        with SessionLocal() as db:
            user_of_brigada = db.query(models.Users).filter(models.Users.brigada_id == query.brigada_id).first()
            if status is not None:
                create_log( request_id=query.id, status=status, user_id=user_of_brigada.id)
            updated_data = query.update_time or {}
            updated_data[str(status)] = str(datetime.now(tz=timezonetash))
            db.query(models.Requests).filter(models.Requests.id==query.id).update({'update_time':updated_data})
            CommitDb().update_data(db,query)
            return query

def tg_update_only_status(requestid,status):
    with SessionLocal() as db:
        query = db.query(models.Requests).filter(models.Requests.id == requestid).first()
        query.status = status
        CommitDb().update_data(db, query)
        query.category_name = query.category.name
        query.category_department = query.category.department
        query.category_sphere_status = query.category.sphere_status
        query.user_id = query.user.id
        query.category_sub_id = query.category.sub_id
        query.user_full_name = query.user.full_name
        query.user_telegram_id = query.user.telegram_id
        with SessionLocal() as db:
            updated_data = query.update_time or {}
            updated_data[str(status)] = str(datetime.now(tz=timezonetash))
            db.query(models.Requests).filter(models.Requests.id == query.id).update({'update_time': updated_data})
            CommitDb().update_data(db, query)
            return query


def getfillialname(name):
    with SessionLocal() as db:
        query = db.query(models.ParentFillials).filter(models.ParentFillials.name==name).first()
        CommitDb().get_data(db,query)
        return query


def update_user_sphere(tel_id,sphere_status):
    with SessionLocal() as db:
        query = db.query(models.Users).filter(models.Users.telegram_id==tel_id).first()
        query.sphere_status=sphere_status
        CommitDb().update_data(db,query)
        return query

def addcomment(user_id,comment,request_id):
    with SessionLocal() as db:
        query = models.Comments(user_id=user_id,request_id=request_id,comment=comment)
        CommitDb().insert_data(db,query)
        return query

def get_work_time():
    with SessionLocal() as db:
        query = db.query(models.Working).first()
        CommitDb().get_data(db,query)
        return query

def get_category_department(department_id):
    with SessionLocal() as db:
        query = db.query(models.Category).filter(
            and_(
                models.Category.status == 1,
                models.Category.department==department_id
            )
        ).first()
        CommitDb().get_data(db,query)
        return query

def get_user_role(telegram_id):
    with SessionLocal() as db:
        query = db.query(models.Groups).join(models.Users).join(models.Roles).filter(models.Users.telegram_id==telegram_id,models.Roles.page_id==64).first()
        CommitDb().get_data(db,query)
        return query

def get_products(category):
    with SessionLocal() as db:
        query = db.query(models.Products).join(models.Category).filter(models.Category.name.ilike(f"%{category}%")).all()
        CommitDb().get_data(db,query)
        return query

def get_product_by_name(name,category):
    with SessionLocal() as db:
        query = db.query(models.Products).filter(models.Products.name.ilike(f"%{name}%")).filter(models.Products.category_id==category).first()
        CommitDb().get_data(db,query)
        return query
def create_order_product(product_id,amount,order_id):
    with SessionLocal() as db:
        query = models.OrderProducts(product_id=product_id,amount=amount,request_id=order_id)
        CommitDb().insert_data(db,query)
        return query

def add_comment_request(comment,category_id,name,user_id,fillial_id):
    with SessionLocal() as db:
        query = models.Requests(description=comment,category_id=category_id,product=name,user_id=user_id,fillial_id=fillial_id)
        CommitDb().insert_data(db,query)
        return query



def add_video_request(comment, category_id,fillial_id, user_id,vidfrom,vidto):
    with SessionLocal() as db:
        query = models.Requests(description=comment,category_id=category_id,user_id=user_id,fillial_id=fillial_id,update_time={'vidfrom':vidfrom,'vidto':vidto})
        query = CommitDb().insert_data(db,query)
        if query.fillial:
            query.fillial_name = query.fillial.name
            query.parentfillial_name = query.fillial.parentfillial.name
        else:
            query.fillial_name = None
            query.parentfillial_name = None
        return query


def get_child_categories(category_id):
    with SessionLocal() as db:
        query = db.query(models.Category).filter(
            models.Category.parent_id == category_id,
            models.Category.status == 1
        ).order_by(models.Category.name).all()

        return query


def add_uniform_request(category_id,fillial_id,user_id,description,total_cum):
    with SessionLocal() as db:
        query = models.Requests(category_id=category_id,fillial_id=fillial_id,user_id=user_id,description=description,price=total_cum)
        CommitDb().insert_data(db,query)
        return query


def delete_request(id):
    with SessionLocal() as db:
        query = db.query(models.Requests).filter(models.Requests.id==id).first()
        CommitDb().delete_data(db,query)
        return query


def add_uniform_product(product_id,amount,request_id):
    with SessionLocal() as db:
        query = models.OrderProducts(product_id=product_id,amount=amount,request_id=request_id)
        CommitDb().insert_data(db,query)
        return query



#def get_category_sphere(name,sphere_status):
#    query = db.query(models.Category).filter(models.Category.name.ilike(f"%{name}%"),models.Category.sphere_status==sphere_status).first()
#    return query


def add_general_comment(comment,user_id):
    with SessionLocal() as db:
        query = models.Comments(comment=comment,user_id=user_id)
        CommitDb().insert_data(db,query)
        return query


def create_log(request_id, status, user_id):
    with SessionLocal() as db:

        query = models.Logs(
            request_id=request_id,
            user_id=user_id,
            status=status
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query


def get_arc_factory_managers(name: Optional[str] = None):
    with SessionLocal() as db:
        query = db.query(models.Managers)
        if name is not None:
            query = query.filter(models.Managers.name.ilike(f"%{name}%"))

        return query.filter(models.Managers.status==1).all()


def get_manager_divisions(manager_id):
    with SessionLocal() as db:
        query = db.query(models.Fillials).filter(models.Fillials.manager_id == manager_id).all()
        return query


def get_manager_division_by_name(name,manager_id):
    with SessionLocal() as db:
        query = db.query(models.Fillials).filter(models.Fillials.name.ilike(f"%{name}%")).first()
        return query


def create_coint_request(user_id,branch_id,amount,description,category):
    with SessionLocal() as db:
        query = models.Requests(
            fillial_id=branch_id,
            price=amount,
            description=description,
            user_id=user_id,
            category_id=category
        )
        db.add(query)
        db.commit()
        db.refresh(query)
        return query



