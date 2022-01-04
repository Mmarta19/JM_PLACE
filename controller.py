import model
from db_models import Carrito, Product,User,Buyed
from datetime import datetime,date,time, timedelta 


def closeSessionByUserId (userid):
    user= model.getUserById(userid)
    user.num_buyed =0
    user.name_buyed =''
    model.delAllCarrito ()
    model.doCommit()

def getUserAndAllProducts (userid):
    user= model.getUserById(userid)
    todos_los_productos = model.getAllProducts()
    return user,todos_los_productos

# create dict from list of categories objs
def cateogrymapping():
    dict_cat = {}
    for c in model.getAllCategories():
        dict_cat[c.id] = c.name
    return dict_cat

def replaceCategoryIdToName(list_products):
    categories = cateogrymapping()

    for p in list_products:
        cat_id = p.category_id
        print(cat_id)
        if cat_id in categories:
            p.category_id = categories[cat_id]
    print(list_products)
    return list_products

def doVendedorLogin (user,todos_los_productos):
    products_seller_ = model.getProductsBySuplierID(user.id)
    dic_sold ={}
    list_sold=[]
    list_value_sold=[]
    for a in products_seller_:
        value_sold= model.getBuyedByReference (a.reference)
        if a.name not in dic_sold:
            dic_sold [a.name]=0
        if value_sold == None:
            dic_sold[a.name]= 0                    
        else:
            for i in value_sold:
                dic_sold [a.name] += i.cuantity_PBuyed
        
    for name, value in dic_sold.items ():
        list_sold.append(name)
        list_value_sold.append(int(value))
    
    if list_value_sold==[]: #si la lista esta vacia te da un error a la hora de generar la grafica
        list_value_sold =[0] # intorducimos un valor para que no de errores
    maxi=max(list_value_sold)

    dic_sold_all ={}
    list_sold_all=[]
    list_value_sold_all=[] 
    pb_seller_all = model.getAllBuyed ()

    for product in todos_los_productos: #declarada al inicio
        if product.name not in dic_sold_all:
            dic_sold_all[product.name]=0
        for pb in pb_seller_all:
            if product.reference == pb.ref_PBuyed:
                dic_sold_all [product.name] += pb.cuantity_PBuyed

    for name_all, value_all in dic_sold_all.items ():
        list_sold_all.append(name_all)
        list_value_sold_all.append(int(value_all))

    if list_value_sold_all==[]: 
        list_value_sold_all =[0] 
    
    max_all= max (list_value_sold_all)
    return products_seller_, maxi,list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all

def doAdminLogin (user,todos_los_productos):
        all_sellers = model.getAllUserByType('Vendedor')
        list_num_products_seller= []
        for user1 in all_sellers:
            
            if user1.type == 'Vendedor':
                all_products_ = model.getAllProductsBySuplierId (user1.id) 
                num_products = len (all_products_)
                list_num_products_seller.append(num_products)

        all_buyers= model.getAllUserByType('Comprador')
        list_num_products_buyers= []
        for user_buyer in all_buyers:
            
            if user_buyer.type == 'Comprador':
                all_products_ = model.getAllProductsBySuplierId (user.id)
                num_products = len (all_products_)
                list_num_products_buyers.append(num_products) 
        
        dic_sold_all ={}
        list_sold_all=[]
        list_value_sold_all=[] 
        pb_seller_all = model.getAllBuyed ()

        for product in todos_los_productos: #declarada al inicio
            if product.name not in dic_sold_all:
                dic_sold_all[product.name]=0
            for pb in pb_seller_all:
                if product.reference == pb.ref_PBuyed:
                    dic_sold_all [product.name] += pb.cuantity_PBuyed

        for name_all, value_all in dic_sold_all.items ():
            list_sold_all.append(name_all)
            list_value_sold_all.append(int(value_all))

        if list_value_sold_all==[]: 
            list_value_sold_all =[0] 
        
        max_all= max (list_value_sold_all)
        print (list_value_sold_all)
        return all_sellers,list_num_products_seller, all_buyers,list_sold_all, list_value_sold_all,max_all

def getAllCategories():
    categories =  model.getAllCategories()
    if categories is None:
        categories = []
    return categories

def deleteItem (referenceC,userid,num_buyed):
    remove_cuantity = model.getCarritoByReference (referenceC)
    num_buyed=int(num_buyed) - remove_cuantity.cantidadC
    model.deleteCarritoByReference (referenceC)        
    user= model.getUserById(userid)
    user.num_buyed=num_buyed
    model.doCommit()
    return userid,user.num_buyed

def confirmBuy (id):
    all_products_carrito = model.getAllCarrito ()
    count =0 #contador de productos comprados por el usuario
    for products in all_products_carrito:
        count +=1 
        item_bought = Buyed (
            ref_PBuyed = products.referenceC,
            cuantity_PBuyed =products.cantidadC,
            data = datetime.now()
        )
        model.addItemBought(item_bought)
    
    model.delAllCarrito()
    user = model.getUserById(id)
    user.num_buyed = 0
    user.total_buyed +=count
    model.doCommit()
    return user

def buyProduct (id,userid,reference):
    product = model.getProductById(id) 
    product.numItems -= 1
    if product.numItems < 0:
        product.numItems = 0
    
    element_cesta = model.getCarritoByReference (reference)

    if element_cesta == None:
        carrito = Carrito(
        referenceC = product.reference,
        nameC = product.name, 
        priceC= product.price,
        cantidadC= 1  
        )
        model.addCarrito(carrito)
        model.doCommit()

    else:
        element_cesta.cantidadC +=1
        model.doCommit()

    all_users= model.getAllUsers ()
    for user in all_users:
        if user.id ==int(userid):
            todos_los_productos = model.getAllProducts()
            user.num_buyed+=1
            model.doCommit()

    return user.num_buyed, user,todos_los_productos

def deleteUser (user_id,admin_id):
    model.deleteUserById (user_id)
    model.deleteProductByIdSuplier (user_id)

def confirmModify (user_id):
    list_products = model.getProductsBySuplierID(user_id)
    user = model.getUserById(user_id)
    
    
    dic_sold ={}
    list_sold=[]
    list_value_sold=[]
    for a in list_products:
        value_sold= model.getBuyedByReference (a.reference)
        if a.name not in dic_sold:
            dic_sold [a.name]=0

        if value_sold == None:
            dic_sold[a.name]= 0                    
        else:
            for i in value_sold:
                dic_sold [a.name] += i.cuantity_PBuyed
        print (dic_sold)

    for name, value in dic_sold.items ():
        list_sold.append(name)
        list_value_sold.append(int(value))
    
    if list_value_sold==[]: 
        list_value_sold =[0]
         
    maxi=max(list_value_sold)

    dic_sold_all ={}
    list_sold_all=[]
    list_value_sold_all=[]
    
    pb_seller_all = model.getAllBuyed ()
    todos_los_productos = model.getAllProducts()
    for product in todos_los_productos: #declarada al inicio
        if product.name not in dic_sold_all:
            dic_sold_all[product.name]=0
        for pb in pb_seller_all:
            if product.reference == pb.ref_PBuyed:
                dic_sold_all [product.name] += pb.cuantity_PBuyed


    for name_all, value_all in dic_sold_all.items ():
        list_sold_all.append(name_all)
        list_value_sold_all.append(int(value_all))

    if list_value_sold_all==[]: 
        list_value_sold_all =[0] 
    
    max_all= max (list_value_sold_all)
    return user,list_products,maxi, list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all

def create_new_client(email,password,name,surnames,sex,phone,province,type):
    user = User (
        name = name,  
        surnames = surnames, 
        sex = sex,
        phone=phone,
        province = province,
        email=email,
        password=password,
        type = type,
        )
    model.createUser(user)

def create_new_product(reference,name, price,numItems,warehouse_place,description,id_suplier,category_id):
    product = Product (
        reference = reference,
        name = name, 
        price = price,
        numItems=numItems,
        warehouse_place = warehouse_place,
        description=description,
        id_suplier=id_suplier,
        category_id = category_id,
        )
    model.createProduct(product)

def modify_product (product_id,name,description,price,reference,numItems,warehouse_place,category_id):
    product = model.getProductById(product_id)

    product.name = name
    product.description = description
    product.price= price
    product.reference = reference
    product.numItems = numItems
    product.warehouse_place = warehouse_place
    product.category_id = category_id
    model.doCommit()

def modify_seller (user,name,surnames,sex,phone,province,email,password,type):

    user.name = name
    user.surnames = surnames
    user.sex = sex
    user.phone = phone
    user.province = province
    user.email = email
    user.password = password
    user.type = type
    model.doCommit()
