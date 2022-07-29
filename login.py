from flask import Flask, render_template,request,redirect,session
import sqlite3
import os


app=Flask(__name__)
app.secret_key="123"
con=sqlite3.connect('myimage.db')
con.execute("CREATE TABLE if not exists image(pid integer primary key,img text,name text,address text,contact integer,email text,password text)")
con.close()

app.config['upload_folder']="static\image"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/loginvalidation',methods=['POST'])
def loginvalidation():
    email=request.form['email']
    password=request.form['password']
    conn=sqlite3.connect('myimage.db')
    cur=conn.cursor()
    cur.execute(""" SELECT * FROM image WHERE email=? AND password=?""",(email,password))
    user=cur.fetchall()
    if len(user)>0:
        session['pid']=user[0][0]
        session['img']=user[0][1]
        session['name']=user[0][2]
        session['address']=user[0][3]
        session['contact']=user[0][4]
        session['email']=user[0][5]
        session['password']=user[0][6]

        return redirect('/home')
    else:
        return redirect('/register')
   


@app.route('/upload',methods=['GET','POST'])
def upload():
    if request.method=='POST':
        upload_image=request.files['upload_image']
        name=request.form['name']
        address=request.form['address']
        contact=request.form['contact']
        email=request.form['email']
        password=request.form['password']
        
        
        if upload_image.filename!='':
            filepath=os.path.join(app.config['upload_folder'],upload_image.filename)
            upload_image.save(filepath)
            con=sqlite3.connect('myimage.db')
            cur=con.cursor()
            cur.execute("INSERT INTO image(img,name,address,contact,email,password)VALUES(?,?,?,?,?,?)",(upload_image.filename,name,address,contact,email,password))
            con.commit()
            data=cur.fetchall()
            con.close()

            return render_template("index.html")
    return render_template("upload.html")
@app.route('/home')
def home():
    if 'pid' in session:
        img=session['img']
        name = session['name']
        address=session['address']
        contact=session['contact']
        mail=session['email']
        password=session['password']
        return render_template('home.html',userimg=img,username=name,useraddress=address,usercontact=contact,usermail=mail,userpassword=password)
    else:
        return redirect('/')

@app.route('/logout')
def logout():
    session.pop('pid')
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)

  