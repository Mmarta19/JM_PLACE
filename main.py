from flask import Flask, render_template,request,redirect,url_for
from sqlalchemy.sql.elements import Null
import controller
from db_models import Base,engine

import model
app = Flask (__name__)


@app.route ('/')
@app.route ('/home')
def home ():
    return render_template("home.html")

@app.route ('/login')
def login ():
    return render_template("login.html")

@app.route ('/signup')
def signup ():
    return render_template("signup.html")

@app.route('/admin/home/<id>')
def admin_home(id):
    todos_los_productos = model.getAllProducts()
    user = model.getUserById(id)
    all_sellers,list_num_products_seller, all_buyers,list_sold_all, list_value_sold_all,max_all = controller.doAdminLogin (user,todos_los_productos)
    return render_template('admin.html',user_obj=user,obj_all_users_sellers=all_sellers,num_products=list_num_products_seller, obj_all_users_buyers=all_buyers,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all)


@app.route('/seller/<id>')
def seller_home (id):
    user = model.getUserById(id)
    todos_los_productos = model.getAllProducts()
    list_prods, maxi,list_sold, list_value_sold,list_sold_all, list_value_sold_all,max_all = controller.doVendedorLogin(user,todos_los_productos)
    categories = controller.getAllCategories()
    products_seller_ = controller.replaceCategoryIdToName(list_prods)
    return render_template('seller.html', user_obj=user, all_products=products_seller_, maxi=maxi, labels=list_sold, values=list_value_sold,labels_all=list_sold_all, values_all=list_value_sold_all,max_all=max_all, categories=categories) 

@app.route('/buyer/<id>')
def buyer_home (id):
    user = model.getUserById(id)
    todos_los_productos = model.getAllProducts()
    return render_template('shop.html',user_obj=user,lista_de_productos=todos_los_productos)

@app.route ('/close_sesion/<id>', methods = ['POST'])
def close_sesion (id):
    controller.closeSessionByUserId(id)
    return redirect(url_for('home'))
    
@app.route('/sign_up',methods = ['POST'])
def sign_up():
    email = request.form ['email']
    password = request.form ['password']
    name = request.form ['name'] 
    surnames = request.form ['surnames']
    sex = request.form ['cont_sex']
    phone=request.form ['phone']
    province = request.form ['province']
    type = request.form ['type']
    controller.create_new_client(email,password,name,surnames,sex,phone,province,type)
    return doLogin(email, password)

def doLogin(email, password):
    all_users= model.getAllUsers ()
    for user in all_users:
        if user.email == email and user.password == password: 
            if user.type == 'Comprador': 
                return redirect(url_for('buyer_home', id=user.id)) 
            if user.type == 'Vendedor':
                return redirect(url_for('seller_home', id=user.id)) 
            if user.type == 'Administrador':
                return redirect(url_for('admin_home', id=user.id)) 
    return render_template('wrong_login.html')

@app.route('/login',methods = ['POST'])
def do_login():
    return doLogin( request.form ['email'], request.form ['password'])

@app.route ('/delete_item/<referenceC>/<userid>/<num_buyed>',methods = ['POST'])
def delete_item(referenceC,userid,num_buyed):
    userid,num_buyed = controller.deleteItem(referenceC,userid,num_buyed)
    return redirect(url_for('cesta',id=userid,num_buyed=num_buyed))

@app.route ('/cesta/<id>/<num_buyed>')
def cesta (id,num_buyed):
    all_products_carrito = model.getAllCarrito ()
    user = model.getUserById(id)

    return render_template('cesta.html',all_products=all_products_carrito, obj_user=user,num_buyed=num_buyed)

@app.route ('/confirm_buy/<id>',methods=['POST'])
def confirm_buy (id):
    user=controller.confirmBuy (id)
    return render_template('buyDone.html', user_obj=user)

@app.route ('/buy_product/<id>/<userid>/<reference>',methods = ['POST'])
def buy_product(id,userid,reference):
    _,_,_= controller.buyProduct (id,userid,reference)
    return redirect(url_for('buyer_home', id=userid))
    
@app.route('/add_product/<user_id>',methods = ['POST'])
def add_product (user_id):
    reference = request.form ['reference'] 
    name = request.form ['name']
    price = request.form ['price']
    numItems=request.form ['numItems']
    warehouse_place = request.form ['warehouse_place']
    description=request.form ['description']
    id_suplier=user_id
    category_id=request.form['category_id']
    print (type(user_id))
    controller.create_new_product(reference,name, price,numItems,warehouse_place,description,id_suplier,category_id) 
    return redirect(url_for('seller_home', id=user_id))
   
@app.route ('/product/update/<product_id>/<user_id>',methods=['POST'])
def product_update (product_id,user_id):
    product = model.getProductById(product_id) 
    user = model.getUserById(user_id)
    categories = controller.getAllCategories()
    return render_template('modify_product.html',product_obj=product,user_obj=user, categories=categories)

@app.route ('/product/delete/<product_id>/<user_id>', methods=['POST'])
def product_delete (product_id,user_id):
   model.deleteProductById (product_id)
   return redirect(url_for('seller_home', id=user_id)) 
   

@app.route ('/confirm_modify/<product_id>/<user_id>', methods = ['POST'])
def confirm_modify (product_id,user_id):
    name = request.form ['new_name']
    description = request.form ['new_description']
    price = request.form ['new_price']
    reference = request.form ['new_ref']
    numItems = request.form ['new_NumItem']
    warehouse_place = request.form ['new_warehouse_place']
    category_id = request.form ['new_category_id']
    controller.modify_product(product_id,name,description,price,reference,numItems,warehouse_place,category_id)

    return redirect(url_for('seller_home', id=user_id)) 
   
    

@app.route ('/seller/<user_id>/<admin_id>', methods=['POST'])
def seller (user_id,admin_id):
    user = model.getUserById(user_id)
    list_products = model.getAllProductsBySuplierId (user_id)
    return render_template ('admin_seller.html',obj_user=user,all_products=list_products,admin_id=admin_id)


@app.route ('/user/update/<user_id>/<admin_id>', methods=['POST'])
def user_update (user_id,admin_id):
    user = model.getUserById(user_id)
    return render_template ('modify_seller.html',obj_user=user,admin_id=admin_id)

@app.route ('/confirm_modfy_seller/<user_id>/<admin_id>/<user_type>', methods=['POST'])
def confirm_modfy_seller (user_id,admin_id,user_type):
    name = request.form ['new_name']
    surnames = request.form ['new_surnames']
    sex = request.form ['new_sex']
    phone = request.form ['new_phone']
    province = request.form ['new_province']
    email = request.form ['new_email']
    password = request.form ['new_password']
    type = user_type

    user = model.getUserById(user_id)
    controller.modify_seller (user,name,surnames,sex,phone,province,email,password,type)
    
    
    list_products = model.getAllProductsBySuplierId (user_id)
    return render_template ('admin_seller.html',obj_user=user,all_products=list_products,admin_id=admin_id)

@app.route ('/delete_user/<user_id>/<admin_id>', methods=['POST'])
def delete_user (user_id,admin_id):
    controller.deleteUser(user_id,admin_id)
    return redirect(url_for('admin_home', id=admin_id)) 

@app.route ('/buyer/<user_id>/<admin_id>', methods=['POST'])
def buyer (user_id,admin_id):
    user = model.getUserById(user_id)
    return render_template ('admin_buyer.html',obj_user=user,admin_id=admin_id)


""" Inizialice backend, to start the web"""
if __name__=='__main__':
    Base.metadata.create_all(engine)
    app.run (debug=True, port=5000)