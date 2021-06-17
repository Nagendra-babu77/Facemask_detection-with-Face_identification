msg=""
if request.method=='POST':
    name=request.form['name']
    regno=request.form['regno']
    mobile=request.form['mobile']
    email=request.form['email']
    address=request.form['address']
    cursor = mydb.cursor()
    sql = "INSERT INTO student(regno,name,mobile,email,address) VALUES (%s, %s, %s, %s, %s)"
    val = (regno,name,mobile,email,address)
    cursor.execute(sql, val)
    mydb.commit()            
    print(cursor.rowcount, "Registered Success")
    result="sucess"
    if cursor.rowcount==1:
        return redirect(url_for('home'))
    else:
        msg='Already Exist'
