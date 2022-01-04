
from sqlalchemy.sql.expression import column
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine 
from sqlalchemy.orm import sessionmaker 
from sqlalchemy.ext.declarative import declarative_base 

# inicializar la BD
engine = create_engine('sqlite:///database/JM_Place.db', connect_args={'check_same_thread': False}) 
Session = sessionmaker(bind=engine) 
session = Session() 
Base = declarative_base()

#Creacion de clases y objetos.
class User (Base):
    __tablename__ ='Users'

    id = Column (Integer,primary_key=True,autoincrement=True)
    name = Column(String(50), nullable=False) 
    surnames = Column(String(50), nullable=False)
    sex = Column(String)
    phone = Column (String (50))
    province = Column (String(100))
    email = Column(String(50), nullable=False)
    password = Column (String(8))
    type = Column (String(50))
    name_buyed= Column (String(50))
    num_buyed = Column (Integer)
    total_buyed = Column (Integer)


    def __init__ (self,name,surnames,sex,phone,province,email,password,type,name_buyed='',num_buyed=0,total_buyed=0 ):
        self.name = name
        self.surnames = surnames
        self.sex = sex
        self.phone = phone
        self.province = province
        self.email = email
        self.password = password
        self.type = type # could be suplier, client,admin
        self.name_buyed = name_buyed #nombre producto comprado
        self.num_buyed=num_buyed #cantidad producto comprado
        self.total_buyed=total_buyed

class Product (Base): ############# OJOOOOO FALTARIA FOTOOO###########

    __tablename__='Product'

    id = Column (Integer,primary_key=True,autoincrement=True)
    reference = Column (String)
    name = Column(String(100), nullable=False) 
    price = Column (Integer) 
    description = Column(String(50), nullable=False)
    numItems = Column(Integer)
    warehouse_place = Column (String(50))
    id_suplier = Column (Integer)
    category_id = Column(Integer, ForeignKey('Category.id'), nullable=False)
     
    def __init__ (self,reference,name,price,description,numItems,warehouse_place,id_suplier, category_id):
        self.reference = reference
        self.name = name
        self.price = price
        self.description = description
        self.numItems = numItems
        self.warehouse_place = warehouse_place
        self.id_suplier = id_suplier
        self.category_id = category_id
        
class Category (Base): 

    __tablename__='Category'

    id = Column (Integer,primary_key=True,autoincrement=True)
    name = Column (String)

    products = relationship("Product", backref="Category")
     
    def __init__ (self,name):
        self.name = name

class Carrito (Base): ############# OJOOOOO FALTARIA FOTOOO###########

    __tablename__='Carrito'

    idC = Column (Integer,primary_key=True,autoincrement=True)
    referenceC= Column (String(50))
    nameC = Column (String(50))
    priceC = Column(Integer)
    cantidadC = Column (Integer)

    def __init__ (self,referenceC='',nameC='',priceC=int,cantidadC=int):
        self.referenceC=referenceC
        self.nameC=nameC
        self.priceC=priceC
        self.cantidadC=cantidadC

class Buyed (Base): ############# OJOOOOO FALTARIA FOTOOO###########

    __tablename__='elements_bought'
    id = Column (Integer,primary_key=True,autoincrement=True)
    ref_PBuyed = Column (String (1000))
    data= Column (String(100))
    cuantity_PBuyed = Column (Integer)


    def __init__ (self,ref_PBuyed,data,cuantity_PBuyed):
        self.ref_PBuyed = ref_PBuyed
        self.data = data
        self.cuantity_PBuyed =cuantity_PBuyed


