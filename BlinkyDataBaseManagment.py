import pyodbc

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-JQOUC01\SQLEXPRESS;'
                      'Database=BlinkyDB;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
loginFlag = 0

def userChecker(id, password):
    params = (id, password)
    sql = '''SELECT * FROM BlinkyDB.dbo.Admins WHERE id=? AND password=?'''
    cursor.execute(sql, params)
    for row in cursor:
        if row.id == id and row.password == password:
            print('Wellcome back Admin ' + row.id)
            return 1
    sql = '''SELECT * FROM BlinkyDB.dbo.Mentor WHERE mid=? AND password=?'''
    cursor.execute(sql, params)
    for row in cursor:
        if row.mid == id and row.password == password:
            print('Hello Mentor ' + row.mid)
            return 2
    sql = '''SELECT * FROM BlinkyDB.dbo.[User] WHERE uid=? AND password=?'''
    cursor.execute(sql, params)
    for row in cursor:
        if row.uid == id and row.password == password:
            print('Wellcome ' + row.uid)
            return 3
    return 0

def login(userid, password):
        userType = userChecker(userid, password)
        if userType == 1:
            # here do the transfer to admin page
            print("Admin login success!")
        elif userType == 2:
            # here do the transfer to mentor page
            print("Mentor login success!")
        elif userType == 3:
            # here do the transfer to user page
            print("User login success!")
        else:
            print("wrong id or password please try again!")

def loginMentor(userid, password):
    cursor.execute('SELECT * FROM BlinkyDB.dbo.[Mentor] WHERE id=? AND password=?', (userid, password))
    for data in cursor:
        if data.id == userid and data.password == password:
            print("login success!")
        else:
            print("wrong id or password please try again!")

def loginUser(userid, password):
    cursor.execute('SELECT * FROM BlinkyDB.dbo.[User] WHERE id=? AND password=?', (userid, password))
    for data in cursor:
        if data.id == userid and data.password == password:
            print("login success!")
        else:
            print("wrong id or password please try again!")

def midCheck(mid):
    sql = '''SELECT mid FROM BlinkyDB.dbo.Mentor WHERE mid=?'''
    cursor.execute(sql, mid)
    for row in cursor:
        if row.mid == mid:
            return False
    return True

def registerMentor(mid, password, conpassword, firstName, lastName, phone):
    if password != conpassword:
        print('password not match!, please repeat the password again.')
        return 1
    if midCheck(mid):
        sql1 = '''INSERT INTO BlinkyDB.dbo.Mentor (mid, password, firstName, lastName, phone) VALUES (?,?,?,?,?)'''
        params = (mid, password, firstName, lastName, phone)  # tuple containing parameter values
        cursor.execute(sql1, params)
        conn.commit()
        print('mentor register successfully!')
    else:
        print('mid already used by other mentor, please choose a different one!')

def uidCheck(uid):
    sql = '''SELECT uid FROM BlinkyDB.dbo.[User] WHERE uid=?'''
    cursor.execute(sql, uid)
    for row in cursor:
        if row.uid == uid:
            return False
    return True

def registerUser(uid, password, firstName, lastName, mid, age, gender, birthday, phone, address, contact1, contact2, medical, diet):
    if uidCheck(uid) and not midCheck(mid):
        sql1 = '''INSERT INTO BlinkyDB.dbo.[User] (uid, password, firstName, lastName, mid, age, gender, birthday, phone, address, contact1, contact2, medical, diet) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
        params = (uid, password, firstName, lastName, mid, age, gender, birthday, phone, address, contact1, contact2, medical, diet)  # tuple containing parameter values
        cursor.execute(sql1, params)
        conn.commit()
        sql2 = '''INSERT INTO BlinkyDB.dbo.Patients VALUES (?,?)'''
        params = (uid, mid)  # tuple containing parameter values
        cursor.execute(sql2, params)
        conn.commit()
        print('user register successfully!')
    elif(uidCheck(uid)==False):
        print('user id already used by other user, please choose a different one!')
    elif(midCheck(mid)==True):
        print('mentor id is not exist!, please provide a valid mentor.')

def patientsCheck(uid, mid):
    sql = '''SELECT uid, mid FROM BlinkyDB.dbo.Patients WHERE uid=? AND mid=?'''
    cursor.execute(sql, (uid, mid))
    for row in cursor:
        if row.uid == uid and row.mid == mid:
            return True
    return False

def imageCheck(imagesID):
    sql = '''SELECT imagesID FROM BlinkyDB.dbo.Images WHERE imagesID=?'''
    cursor.execute(sql, imagesID)
    for row in cursor:
        if row.imagesID == imagesID:
            return True
    return False

def uploadImage(imagesID, name, role, link, uid, mid):
    if not uidCheck(uid) and not midCheck(mid):
        if patientsCheck(uid, mid) and not imageCheck(imagesID):
            sql1 = '''INSERT INTO BlinkyDB.dbo.Images (imagesID, name, role, link, uid, mid) VALUES (?,?,?,?,?,?)'''
            params = (imagesID, name, role, link, uid, mid)  # tuple containing parameter values
            cursor.execute(sql1, params)
            conn.commit()
            print('image uploaded successfully!')
        else:
            print('please make sure that the user patient under the specific mentor.')
    else:
        print('please check user id and mentor id.')

def signPatient(uid, mid):
    if not uidCheck(uid) and not midCheck(mid) and not patientsCheck(uid, mid):
        sql1 = '''INSERT INTO BlinkyDB.dbo.Patients (uid, mid) VALUES (?,?)'''
        params = (uid, mid)  # tuple containing parameter values
        cursor.execute(sql1, params)
        conn.commit()
        sql2 = '''UPDATE BlinkyDB.dbo.[User] SET mid=?'''
        cursor.execute(sql2, mid)
        conn.commit()
        print('patient added successfully!')
    else:
        print('please check user id and mentor id.')

def titleCheck(titleID, uid):
    sql = '''SELECT titleID FROM BlinkyDB.dbo.[Titles] WHERE titleID=? AND uid=?'''
    cursor.execute(sql, (titleID, uid))
    for row in cursor:
        if row.titleID == titleID:
            return True
    return False

def uploadTitle(titleID, action, uid, mid, role):
    if not uidCheck(uid) and not midCheck(mid):
        if patientsCheck(uid, mid) and not titleCheck(titleID, uid):
            sql1 = '''INSERT INTO BlinkyDB.dbo.Titles (titleID, phrase, uid, mid, role) VALUES (?,?,?,?,?)'''
            params = (titleID, action, uid, mid, role)  # tuple containing parameter values
            cursor.execute(sql1, params)
            conn.commit()
            print('title uploaded successfully!')
        elif patientsCheck(uid, mid)== False:
            print('please make sure that the user patient under the specific mentor.')
        elif titleCheck(titleID, uid) == True:
            print('this title is already in use please ')
    else:
        print('please check user id and mentor id.')

def defaultTitleCheck(titleID):
    sql = '''SELECT titleID FROM BlinkyDB.dbo.[Titles] WHERE titleID=?'''
    cursor.execute(sql, titleID)
    for row in cursor:
        if row.titleID == titleID:
            return True
    return False

def uploadDefaultTitle(titleID, phrase):
    if not defaultTitleCheck(titleID):
        sql1 = '''INSERT INTO BlinkyDB.dbo.Titles (titleID, phrase) VALUES (?,?)'''
        params = (titleID, phrase)  # tuple containing parameter values
        cursor.execute(sql1, params)
        conn.commit()
        print('title uploaded successfully!')
    else:
        print('this title is already in use please ')

def uploadDefaultImage(imagesID, name, link):
    if not imageCheck(imagesID):
        sql1 = '''INSERT INTO BlinkyDB.dbo.Images (imagesID, name, link) VALUES (?,?,?)'''
        params = (imagesID, name, link)  # tuple containing parameter values
        cursor.execute(sql1, params)
        conn.commit()
        print('image uploaded successfully!')
    else:
        print('please make sure that the user patient under the specific mentor.')