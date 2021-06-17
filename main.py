# main.py
import os
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from camera import VideoCamera
import cv2
import shutil
import PIL.Image
from PIL import Image
import datetime
import imagehash
import urllib.request
import urllib.parse
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  charset="utf8",
  database="face_mask"

)
app = Flask(__name__)


@app.route('/')
def index():
    shutil.copy('f1.jpg', 'faces/f1.jpg')
    shutil.copy('f2.jpg', 'faces/f2.jpg')
    shutil.copy('f3.jpg', 'faces/f3.jpg')
    shutil.copy('f4.jpg', 'faces/f4.jpg')
    
      
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    msg=""
    shutil.copy('f1.jpg', 'faces/f1.jpg')
    shutil.copy('f2.jpg', 'faces/f2.jpg')
    shutil.copy('f3.jpg', 'faces/f3.jpg')
    shutil.copy('f4.jpg', 'faces/f4.jpg')
    
    if request.method=='POST':
        uname=request.form['uname']
        pwd=request.form['pass']
        cursor = mydb.cursor()
        cursor.execute('SELECT * FROM admin WHERE username = %s AND password = %s', (uname, pwd))
        account = cursor.fetchone()
        if account:
            #session['loggedin'] = True
            #session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('login.html',msg=msg)


@app.route('/home', methods=['GET', 'POST'])
def home():

        
    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM register')
    data = cursor.fetchall()
    if request.method=='GET':
        act = request.args.get('act')
        did = request.args.get('did')
        if act=="del":
            fn=did+".jpg"
            #os.remove("static/photo/"+fn)
            cursor1 = mydb.cursor()
            cursor1.execute('delete FROM register WHERE regno = %s', (did, ))
            mydb.commit()   
            return redirect(url_for('home',data=data))
    return render_template('home.html',data=data)

@app.route('/register', methods=['GET', 'POST'])
def register():
    
    msg=""
    if request.method=='POST':
        name=request.form['name']
        regno=request.form['regno']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        cursor = mydb.cursor()
        sql = "INSERT INTO register(regno,name,mobile,email,address,fimg) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (regno,name,mobile,email,address,'')
        cursor.execute(sql, val)
        mydb.commit()            
        print(cursor.rowcount, "Registered Success")
        result="sucess"
        if cursor.rowcount==1:
            return redirect(url_for('home'))
        else:
            msg='Already Exist'
    return render_template('register.html',msg=msg)

@app.route('/capture', methods=['GET', 'POST'])
def capture():
    msg=""
    regno=request.args.get('regno')
    if request.method=='POST':
        regno=request.form['regno']
        mask_st=request.form['mask_st']
        fimg=""+regno+".jpg"
        cursor = mydb.cursor()

        cursor.execute("SELECT max(id)+1 FROM st_face")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        vface=""+regno+"_"+str(maxid)+".jpg"
        sql = "INSERT INTO st_face(id, regno, vface, mask_st) VALUES (%s, %s, %s, %s)"
        val = (maxid, regno, vface, mask_st)
        print(val)
        cursor.execute(sql,val)
        mydb.commit()
        cursor.execute('update register set fimg=%s WHERE regno = %s', (vface, regno))
        mydb.commit()
       
        shutil.copy('faces/f1.jpg', 'static/photo/'+vface)
        return redirect(url_for('home'))
    
                
    return render_template('capture.html',regno=regno)

@app.route('/report', methods=['GET', 'POST'])
def report():

    cursor = mydb.cursor()
    cursor.execute('SELECT * FROM details')
    data = cursor.fetchall()

    return render_template('report.html',data=data)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    return render_template('login.html')

@app.route('/monitor', methods=['GET', 'POST'])
def monitor():
    msg=""
    regno=""
    famt=0
    act="0"
    mst=""
    st="1"
    cnt=0
    nn=0
    pr=0
    rcnt=0
    period=0
    cutoff=10
    now = datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    
   
        
    cursor11 = mydb.cursor()
    cursor11.execute('SELECT * FROM st_face')
    srow = cursor11.fetchall()
    for sr in srow:
        
        regno=sr[1]
        #print(regno)
        img=sr[2]
        #sr[0]+".jpg"

        hash0 = imagehash.average_hash(Image.open("static/photo/"+img)) 
        hash1 = imagehash.average_hash(Image.open("faces/f1.jpg"))
        cc1=hash0 - hash1
        if cc1<=cutoff:
            mst=sr[3]
            if mst=="1":
                msg="Mask weared"+regno
            elif mst=="2":
                msg="Mask not weared"+regno
            else:
                msg=""

    if mst=="1" or mst=="2":
       
        cursor = mydb.cursor()

        cursor.execute("SELECT max(id)+1 FROM details")
        maxid = cursor.fetchone()[0]
        if maxid is None:
            maxid=1
        if mst=="2":
            famt=200
        else:
            famt=0
        
        vface=""+regno+"_"+str(maxid)+".jpg"
        sql = "INSERT INTO details(id, regno, face_st, fine_amt) VALUES (%s, %s, %s, %s)"
        val = (maxid, regno, mst, famt)
        print(val)
        cursor.execute(sql,val)
        mydb.commit()
        
            

##        hash20 = imagehash.average_hash(Image.open("static/photo/"+img)) 
##        hash21 = imagehash.average_hash(Image.open("faces/f2.jpg"))
##        cc2=hash20 - hash21
##
##        hash30 = imagehash.average_hash(Image.open("static/photo/"+img)) 
##        hash31 = imagehash.average_hash(Image.open("faces/f3.jpg"))
##        cc3=hash30 - hash31
##
##        hash40 = imagehash.average_hash(Image.open("static/photo/"+img)) 
##        hash41 = imagehash.average_hash(Image.open("faces/f4.jpg"))
##        cc4=hash40 - hash41

##        if cc1<=cutoff or cc2<=cutoff or cc3<=cutoff or cc4<=cutoff:
##            print(str(cc1)+" "+str(cc2))
                        
            
                
##        mess="Name:"+srow2[1]+", Regno:"+rg+" has absent"
##        params = urllib.parse.urlencode({'token': 'b81edee36bcef4ddbaa6ef535f8db03e', 'credit': 2, 'sender': 'NoTSMS', 'message':mess, 'number':mob})
##        url = "http://pay4sms.in/sendsms/?%s" % params
##        with urllib.request.urlopen(url) as f:
##            print(f.read().decode('utf-8'))
##        ay+=1
        mess=""
        cursor11.execute('SELECT * FROM admin')
        srow3 = cursor11.fetchone()
        mob=srow3[3]
                    
        
                
                
            
            
            
            #return redirect(url_for('monitor',act=act))
    return render_template('monitor.html', act=act, st=st, msg=msg)

def DCNN():
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)
    X_train = X_train.astype('float32')
    X_test = X_test.astype('float32')

    # normalizing the data to help with the training
    X_train /= 255
    X_test /= 255

    # one-hot encoding using keras' numpy-related utilities
    n_classes = 10
    print("Shape before one-hot encoding: ", y_train.shape)
    Y_train = np_utils.to_categorical(y_train, n_classes)
    Y_test = np_utils.to_categorical(y_test, n_classes)
    print("Shape after one-hot encoding: ", Y_train.shape)

    # building a linear stack of layers with the sequential model
    model = Sequential()
    # hidden layer
    model.add(Dense(100, input_shape=(784,), activation='relu'))
    # output layer
    model.add(Dense(10, activation='softmax'))

    # looking at the model summary
    model.summary()
    # compiling the sequential model
    model.compile(loss='categorical_crossentropy', metrics=['accuracy'], optimizer='adam')
    # training the model for 10 epochs
    model.fit(X_train, Y_train, batch_size=128, epochs=10, validation_data=(X_test, Y_test))

def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
    
@app.route('/video_feed')
        

def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
