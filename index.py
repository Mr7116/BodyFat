from flask import Flask, render_template ,redirect, url_for, request,flash
from werkzeug.security import generate_password_hash, check_password_hash
from myDB import DataBase_Bodyfat

app = Flask(__name__)
db = DataBase_Bodyfat()

def genpassword(password):
    hashed_value = generate_password_hash(password, method='sha256')
    return hashed_value

def checkpassword(pwhash,password):
    dehash_value = check_password_hash(pwhash,password)
    return dehash_value


@app.route('/', methods=['GET', 'POST'])
def Home():
  return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
# def Home():
#   return render_template('index.html')
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
             username = request.form['username']
             password = request.form['password']
             check_username = db.check_username(username)
             if len(check_username) > 0 :
                 list_user = db.checktologin(username)       
                 print('',list_user)
                 check_password = checkpassword(list_user["password"],password) 
                 if(check_password):
                     return redirect(url_for('Main'))
                 else:
                     error = 'Password incorrect.'
             else:
                 error = 'Username isn\'t in the system.'
             

        else:
            return redirect(url_for('login'))
    return render_template('login.html', error=error)

@app.route('/register', methods=['GET', 'POST'])

def register():
    messages = None
    error = None    
    if request.method == 'POST':
        if request.form['submit_button'] == "ย้อนกลับ":
            return redirect(url_for('login'))
        elif request.form['submit_button'] == "ยืนยัน":
             username = request.form['username']
             password = request.form['password']
             confirm_password = request.form['confirm_password']
             check_username = db.check_username(username)
             if len(check_username) > 0 :
                 error = 'Username already exist'
             else:
                 if password == confirm_password :
                    hashed_password = genpassword(password)               
                    register_count = db.register(username,hashed_password)
                    print(register_count)        
                    return redirect(url_for('login'))     
                 else :
                      error = 'Password Not Match'         

    return render_template('register.html', error=error)


@app.route('/Main', methods=['GET', 'POST'])
def Main():
    error = None
    check_radio_male = None
    check_radio_female = None
    bmi = None
    bmi_text = None
    fat_percentage = None
    body_fat = None
    showResult = ''
    if request.method == 'POST':
        if request.form['weight'] == "" or request.form['tallness'] == "" or request.form['age'] == "":
            error = 'กรุณากรอกข้อมูลครบถ้วน'
        else:
            weight = int(request.form['weight'])
            tallness = int(request.form['tallness']) /100
            age = int(request.form['age'])
            gender = request.form['gender']          
            if gender == 'male':
                check_radio_male = 'checked'
            else:
                check_radio_female = 'checked'
            bmi = round(weight/(tallness**2),8)
            if bmi > 30 :
                bmi_text = 'คุณอ้วนมาก ควรลดน้ำหนัก'
            elif bmi >= 25 :
                bmi_text = 'คุณเริ่มอ้วน ควรออกกำลังกาย'
            elif bmi >= 18.6 :
                bmi_text = 'คุณอยู่ในเกณฑ์ปกติ'
            elif bmi <= 18.5 :
                bmi_text = 'คุณผอมเกินไป ควรเพิ่มน้ำหนัก'
            if gender == 'male':
                fat_percentage = round((((1.2) * bmi ) + (0.23 * age)) - 16.2, 2) 
                body_fat = round((weight * fat_percentage) /100,2)
            else : 
                fat_percentage = round((((1.2) * bmi ) + (0.23 * age)) - 5.4, 2) 
                body_fat = round((weight * fat_percentage) /100,2)
            print(weight,tallness,age,gender,bmi,bmi_text,fat_percentage,body_fat,)
            showResult = 'succeedful'
    return render_template('main_page.html', error=error,check_radio_male=check_radio_male,check_radio_female=check_radio_female,bmi=bmi,bmi_text=bmi_text,fat_percentage=fat_percentage,body_fat=body_fat,showResult=showResult)

def Insert_Data() :
    error = None
    check_radio_male = None
    check_radio_female = None
    bmi = None
    bmi_text = None
    fat_percentage = None
    body_fat = None
    showResult = ''
    print("new pageeeeeee")
    return render_template('main_page.html', error=error,check_radio_male=check_radio_male,check_radio_female=check_radio_female,bmi=bmi,bmi_text=bmi_text,fat_percentage=fat_percentage,body_fat=body_fat,showResult=showResult)




if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000)