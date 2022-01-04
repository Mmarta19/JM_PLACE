from db_models import Carrito, Category, Product,User,Buyed,session

""" User queries"""
def createUser(user):
    session.add(user)
    session.commit()

def getUserById (userid):
    return session.query(User).filter_by(id=int(userid)).first()
    
def getAllUsers ():
    return session.query(User).all()

def getAllUserByType (userType):
    return session.query(User).filter_by(type = userType).all()

def deleteUserById (userid):
    session.query(User).filter_by(id=int(userid)).delete()
    session.commit()
def deleteProductByIdSuplier(suplier_id):
    session.query(Product).filter_by(id_suplier=int(suplier_id)).delete()
    session.commit()

""" Product queries"""

def getAllProducts ():
    return session.query(Product).all()

def getProductById(productId):
    return session.query(Product).filter_by(id=int(productId)).first()

def getProductsBySuplierID (suplierId):
    return session.query(Product).filter_by(id_suplier=int(suplierId))

def getAllProductsBySuplierId (suplierId):
    return session.query(Product).filter_by(id_suplier = suplierId).all()

def getProductsByCategoryId (categoryId):
    return session.query(Product).filter_by(category_id=int(categoryId))

def deleteProductById (productId):
    session.query(Product).filter_by(id=int(productId)).delete()
    session.commit()

def getAllCategories():
    return session.query(Category).all()

def createProduct(product):
    session.add(product)
    session.commit()

def addItemBought(item_bought):
    session.add(item_bought)
    session.commit()

"""Buyed queries"""

def getBuyedByReference (reference):
    return session.query(Buyed).filter_by(ref_PBuyed = reference)

def getAllBuyed ():
    return session.query(Buyed).all()

"""Carrito queries"""

def getCarritoByReference (reference):
    return session.query(Carrito).filter_by(referenceC=reference).first()

def getAllCarrito ():
    return session.query(Carrito).all()

def deleteCarritoByReference (reference):
    return session.query(Carrito).filter_by(referenceC=reference).delete()

def delAllCarrito ():
    session.query(Carrito).delete()

def addCarrito (carrito):
    session.add(carrito)
    session.commit()

"""Other queries"""
def doCommit():
    session.commit()