import mysql.connector as ms
import time as t
from tabulate import tabulate as tab
import random as r
X=ms.connect(host='localhost',user='root',passwd='shailu@121109',database='shailesh_project')
cur=X.cursor()
print("="*55)
print("Welcome To FEASTFLOW🚚 📦".center(55))
print("="*55)
access=[]
ans=['0','1','2','3','4']
al=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
num=['1','2','3','4','5','6','7','8','9','0']

def getcourse():
    time=t.localtime()
    h=time.tm_hour
    if 7 < h < 13:
        return "Breakfast", "Desserts"
    elif h<16:
        return "Lunch","Starters","Desserts"
    return "Dinner","Starters","Desserts"

def view_menu(hname,hid):
    print("="*55)
    print(f"{hname}".center(55))
    print("="*55)
    cur.execute(f'select Food,Price from menus.`{hid}` where course in %s'%(getcourse(),))
    data=cur.fetchall()
    new_data=[(i,*value) for i,value in enumerate(data,start=1)]
    print(tab(new_data,headers=['S.No','Food Name','Price'],tablefmt='grid'))

def get_menu(hid):
    cur.execute(f'select Food,Price from menus.`{hid}` where course in %s'%(getcourse(),))
    data=cur.fetchall()
    return data

def show_cart(details):
    cur.execute('select food_items,price,quantity from cart where customername=%s',(details[0],))
    print("Heres Your Current Cart:")
    print(tab(cur.fetchall(),headers=['Food_Item','Price','Quantity'],tablefmt='grid'))

def check_district(d):
    while True:
        cur.execute('select distinct district from district_list where district=%s',(d,))
        if cur.fetchone() is None:
            print("Oops We Dont Operate In That District")
            print("Please Try A Nearby District")
            d=input("Please Enter Another District: ")
        else:
            return d

def check_city(c):
    while True:
        cur.execute('select distinct city from district_list where city=%s',(c,))
        if cur.fetchone() is None:
            print("Oops We Dont Operate In That City/Town")
            print("Please Try A Nearby City/Town")
            c=input("Please Enter A Valid City: ")
        else:
            return c
    

def returntologin(n=5):
    print("Returning To Login Page")
    i=0
    while i<n:
        print("■",end="")
        t.sleep(0.5)
        i+=1
    print()
    print('='*55)

def loadanimation(c='.',n=5):
    i=0
    while i<n:
        print(c,end='')
        t.sleep(0.5)
        i+=1
    print()
    

def checklogin(table,col_name,unique_value,passwd,msg,delete=True,login=True):
    cur.execute(f"select passwd from {table} where {col_name}=%s",(unique_value,))
    i=cur.fetchone()
    if i is None:
        return False
    else:
        if passwd==i[0]:
            return True
        else:
            k=3
            while True:
                if k==0:
                    print("[Attempts Exhausted]".center(55,'='))
                    print(msg)
                    if delete:
                        cur.execute(f'delete from {table} where {col_name}=%s',(unique_value,))
                    return False
                print(f"[Invalid Password: {k} attempts remaining]".center(55,'='))
                pwd=input("Enter The Correct Password(press f if forgotten): ")
                if pwd=='f':
                    k=0
                elif pwd==i[0]:
                    print("[Correct Password Had Been Entered]".center(55,'='))
                    if login:
                        print("Loging In ",end="")
                        i=0
                        while i<3:
                            print("■ ",end="")
                            t.sleep(0.75)
                            i+=1
                        print()
                    return True
                k-=1

def userlogin():
    global em
    print("\t1.===>Login In To Customer Account")
    print("\t2.===>Register A New User Account")
    print('='*55)
    c=input("Please Enter Your Choice(press f to return to main login): ")
    while c not in ('1','2','f'):
        print("[ERROR:Invalid Choice]".center(55,'='))
        c=input("Please Enter A Valid Choice (1/2)(press f to return to login): ")
    if c=='1':
        em=input("Please Enter Your Email: ").lower()
        while not em.endswith(".com"):
            em=input("Please Enter A Valid Email: ").lower()
        pwd=input("Enter The Password Of Ur Account: ")
        if checklogin('c_details','email',em,pwd,"Please Contact An Admin To Resolve The Issue Or Create A New Account"):
            print("="*55)
            print("LOGIN SUCCESSFULL".center(55))
            print('='*55)
            access.append('u')
            return
        else:
            print("[LOGIN FAILED: User not found]".center(55,'='))
            print("Please Try To Create A New Account")
            returntologin(5)
            userlogin()
    elif c=='2':
        useradd()
    elif c=='f':
        returntologin()
        login()
        return
    
def useradd():
    print("[NEW USER REGISTRATION]".center(55,'='))
    em=input("Please Enter Your Email: ").lower()
    while not em.endswith(".com"):
        em=input("Please Enter A Valid Email: ").lower()
    name=input("Please Enter Your Name: ").title()
    dis=input("Enter Your District: ").title()
    dis=check_district(dis)
    city=input("Enter The Major City/Town In Which U Live: ").title()
    city=check_city(city)
    pwd=input("Enter The Password Of Ur Account: ")
    cur.execute('insert into c_details values(%s,%s,%s,%s,%s)',(name,dis,city,em,pwd))
    X.commit()
    print('='*55)
    print("NEW ACCOUNT REGISTERED".center(55))
    print('='*55)
    returntologin(5)
    userlogin()
    return

def user_term():
    em='shailu.devam@gmail.com'
    cur.execute('select * from c_details where email=%s',(em,))
    details=cur.fetchone()
    print(f"Ok So What We Doing Today {details[0]}?")
    print("\t1--->Order Food")
    print("\t2--->Update Credentials")
    print('\t3--->Check Order Status')
    print("\t4--->Log Out")
    print("="*55)
    choice=input("Please Enter Your Choice(1/2/3/4): ")
    while choice not in "1234":
        choice=input("Please Enter A Valid Choice: ")
    if choice=='1':
        cur.execute('select H_Name,District,city from h_details where district=%s',(details[1],))
        data=cur.fetchall()
        print('Alright Found Some Hotels from Hotels In Your Area')
        print(tab(data,headers=['Hotel Name','District','City'],tablefmt='grid'))
        hname=input("Enter The Name Of The Hotel You Wish To Order From: ").title()
        cur.execute('select h_id from h_details where h_name="%s"'%(hname,))
        d=cur.fetchone()
        while d is None:
            print("It Seems You Have Made Mistake")
            hname=input("Enter The Name Of The Hotel You Wish To Order From: ")
            print('select h_id from h_details where h_name=%s',(hname,))
            cur.execute('select h_id from h_details where h_name=%s',(hname,))
            d = cur.fetchone()
        hid=d[0]
        print("Lets Look At The Menu Now Shall We?")
        view_menu(hname,hid)
        c1=input("Enter The Serial Number Of The Food You Wish To Order: ")
        while c1!='f':
            if c1.isdigit():
                menu=get_menu(hid)
                q=int(input(f"How Many {menu[int(c1)-1][0]} would u like: "))
                cur.execute(f'insert into cart values %s'%((details[0],menu[int(c1)-1][0],menu[int(c1)-1][1],q),))
                X.commit()
            elif c1=='c':
                show_cart(details)
            c1=input("Anything Else?(f to stop/c to check cart): ")
            if c1=='f':
                cur.execute('Select SUM(price*quantity) from cart where customername=%s',(details[0],))
                tp=cur.fetchone()[0]
                show_cart(details)
                print("Your Total Price Comes Out To Be:",tp)
                c2=input("Would U Like To Place An Order[y/a(to add more)/c(to clear cart)]: ").lower()
                if c2=='y':
                    cur.execute('select * from cart where customername=%s',(details[0],))
                    order=[i+(hid,) for i in cur.fetchall()]
                    for i in order:
                        cur.execute('insert into orders(customername,food_items,price,quantity,h_id) values %s'%(i,))
                    cur.execute('delete from cart where customername=%s',(details[0],))
                    X.commit()
                    print("Order Has Been Placed")
                    print("Approximate Waiting Time:45 mins")
                    print("Returning To Main Terminal", end='')
                    loadanimation()
                    print('='*55)
                    user_term()
                    return
                elif c2=='a':
                    print("Lets Have A Look At The Menu Again Now Shall We?")
                    view_menu(hname,hid)
                    c1=input("What Other Item Would U Like: ")
                else:
                    cur.execute("delete from cart where customername=%s",(details[0],))
                    X.commit()
                    print("Cart Has Been Cleared")
                    print("Returning To Main Terminal",end='')
                    loadanimation()
                    print('=' * 55)
                    user_term()
                    return

    elif choice=='2':
        print('So Want To Update Some Details Huh?')
        print('='*55)
        print("But First What Do You Wish To Update")
        print('\t1.--->Name')
        print('\t2.--->Location')
        print('\t3.--->Credentials')
        print('=' * 55)
        choice2=input("Enter Your Choice(1/2/3): ")
        while choice2 not in ('1','2','3'):
            choice2=input("Please Enter A Valid Choice(1/2/3): ")
        if choice2=='1':
            print("Lets Change That Old Name Shall We?")
            cname=input('Enter Your New Name: ').title()
            cur.execute('update c_details set name=%s where email=%s',(cname,details[3]))
            cur.execute('update cart set customername=%s where customername=%s', (cname, details[0]))
            cur.execute('update orders set customername=%s where customername=%s', (cname, details[0]))
            X.commit()
            print(f"Well Welcome {cname} Lets Get Going")
            print("Returning to Terminal", end='')
            loadanimation()
            print('='*55)
            user_term()
            return
        elif choice2=='2':
            print("Moved Locations Huh? Well Lets Update That")
            dis=input("Enter Your New District:").title()
            dis=check_district(dis)
            city=input("Enter Your City:").title()
            city=check_city(city)
            cur.execute('update c_details set district=%s, city=%s where email=%s',(dis,city,details[3]))
            X.commit()
            print("Location Has Been Updated")
            print('='*55)
            print("Returning to Terminal",end='')
            loadanimation()
            print('='*55)
            user_term()
            return
        elif choice2=='3':
            print("Now That's A Big Change")
            pwd=input("Lets Confirm Your Password: ")
            if checklogin('c_details','email',em,pwd,"Well You Seem To Be An Intruder",False,False):
                newem=input("Enter Your New Email Address: ").title()
                pwd=input("Please Enter Your New Password: ")
                cur.execute('update c_details set passwd=%s, email=%s where email=%s',(pwd,newem,em))
                print("Lets Continue And Don't Forget Your Password")
                X.commit()
                print("Returning to Terminal", end='')
                loadanimation()
                print('=' * 55)
                user_term()
                return
            else:
                print("Logging You Out")
                returntologin(5)
                login()
                return

    elif choice=='3':
        print("Alright Lets Check On That Order Shall We?")
        print('='*55)
        cur.execute("select Food_items,price,quantity from orders where customername=%s",(details[0],))
        cart=cur.fetchall()
        if len(cart)==0:
            print("It Seems You Have Yet To Place An Order.Please Try Again")
        else:
            cur.execute('select sum(price*quantity) from orders where customername=%s',(details[0],))
            tp=cur.fetchone()[0]
            cur.execute('select distinct status from orders where customername=%s',(details[0],))
            status=cur.fetchone()[0]
            print("This Is Your Current Orer:")
            print(tab(cart,headers=['Food Items','Price','Quantity'],tablefmt='grid'))
            print(f"Your Order Costs {tp} and It's Current Status Is:'{status}'")
            if status=='Order Placed':
                print("Estimated Time Of Arrival: 45 mins")
            elif status=='Order Accepted':
                print("Estimated Time Of Arrival: 30 mins")
            elif status=='Out For Delivery':
                print("Estimated Time Of Arrival: 15 mins")
            print("Returning to Terminal", end='')
            loadanimation()
            print('=' * 55)
            user_term()
            return

    elif choice=='4':
        print("Well Hope We Helped On Your Journey")
        print("Logging You Out")
        returntologin(5)
        login()
        return


def dellogin():
    print("\t1.===>Login In To Delivery Account")
    print("\t2.===>Register A New Delivery Account")
    print('='*55)
    c=input("Please Enter Your Choice(press f to return to main login page): ")
    while c not in ('1','2','f'):
        c=input("Please Enter A Valid Choice(1/2)(press f to return to login page): ")
    if c=='1':
        did=input("Enter Your Delivery ID(6 Characters): ").upper()
        while len(did)!=6:
            did=input("Please Enter a Valid 6 Character Delivery ID: ").upper()
        pwd=input("Enter The Password: ").title()
        if checklogin('d_cred','d_id',did,pwd,"Please Contact An Admin To Resolve The Issue Or Create A New Account"):
            print("="*55)
            print("LOGIN SUCCESSFULL".center(55))
            print('='*55)
            access.append('d')
            return
        else:
            print("[LOGIN FAILED: ID not found]".center(55,'='))
            print("Please Try To Create A New Account")
            returntologin(5)
            dellogin()
            return
    elif c=='2':
        deladd()
    elif c=='f':
        returntologin(5)
        login()
        return

def deladd():
    print("[NEW DELIVERY REGISTRATION]".center(55,'='))
    name=input("Please Enter Your Name: ").title()
    dis=input("Enter Your District: ").title()
    dis=check_district(dis)
    city=input("Enter The Major City/Town In Which U Live: ").title()
    city=check_city(city)
    while True:
        l=[r.choice(al)]+r.choices(al+num,k=5)
        did=''
        for i in l:
            did+=i
        cur.execute('select * from d_cred where D_ID=%s',(did,))
        if cur.fetchone() is None:
            break
        else:
            continue
    print(f"Your 6 Character Deliver ID is: {did}")
    pwd=input("Enter A Strong Password For Your Account: ")
    print("="*55)
    cur.execute("insert into d_cred values(%s,%s)",(did,pwd))
    cur.execute("insert into d_details(d_id,name,district,city) values(%s,%s,%s,%s)",(did,name,dis,city))
    print("NEW ACCOUNT REGISTERED".center(55))
    print("="*55)
    X.commit()
    returntologin(5)
    dellogin()
    return
    
def hotellog():
    print("\t1.===>Login In To Hotel Account")
    print("\t2.===>Register A New Hotel Into The App")
    print("\t3.===>View Registration Status")
    print('='*55)
    c2=input("Please Input Ur Choice(f to return to main login page): ")
    while c2 not in ('1','2','3','f'):
        c2=input("Please Enter A Valid Choice: ")
    if c2=='f':
        returntologin()
        login()
        return
    elif c2=='1':
        hid="HTL-"+input("Please Enter Your 6 Character Hotel ID: ").upper()
        while len(hid)!=10:
            hid="HTL-"+input("Please Input A Valid '6' Character Hotel ID: ").upper()
        pwd=input("Please Input Your Respective Passwords: ")
        if checklogin('h_cred','hotel_id',hid,pwd,"Please Contact An Admin To Resolve The Issue",False):
            print("="*55)
            print("LOGIN SUCCESSFULL".center(55))
            print('='*55)
            access.append('h')
            return
        else:
            print("[LOGIN FAILED: Hotel not found]".center(55,'='))
            print("Please Try To Create A New Account")
            returntologin(5)
            hotellog()
            return
    elif c2=='2':
        print("[NEW HOTEL REGISTRATION]".center(55,'='))
        hoteladd()
    elif c2=='3':
        hname=input("Please Enter The Hotel Name That You Have Registered With: ").title()
        cur.execute("select exists(select dis,city,approval from h_app where hname=%s)",(hname,))
        if cur.fetchone()[0]==1:
            cur.execute("select dis,city,approval from h_app where hname=%s",(hname,))
            d=cur.fetchone()
            if d[2] is None:
                print("Its Seems Your Registrations Hasn't Been Reviewed Yet")
                print("Please Try Later")
                returntologin(5)
                login()
                return
            elif d[2]=='y':
                print("Its Seems Your Registrations Has Been Accepted!!!")
                while True:
                    l=[r.choice(al)]+r.choices(al+num,k=5)
                    hid=''
                    for i in l:
                        hid+=i
                    cur.execute('select * from h_cred where hotel_id=%s',('HTL-'+hid,))
                    if cur.fetchone() is None:
                        break
                    else:
                        continue
                print("="*55)
                print(f"Your Hotel ID is: {hid}".center(55))
                print("="*55)
                print("Dont Forget This ID. It Will Be Used For Logging In")
                pwd=input("Please Enter A STRONG Password For Your Account: ")
                cur.execute("insert into h_cred values(%s,%s)",('HTL-'+hid,pwd))
                cur.execute("insert into h_details values(%s,%s,%s,%s)",('HTL-'+hid,hname,d[0],d[1]))
                cur.execute("delete from h_app where hname=%s",(hname,))
                X.commit()  
                print("[REGISTRATION SUCCESSFULL]".center(55,'='))
            elif d[2]=='n':
                print("Sad To Be The Bearer Of Bad News But Your Registration Has Been Rejected")
                print("Try Again If You Would Like")
                cur.execute("delete from h_app where hname=%s",(hname,))
                returntologin(5)
                login()
                return
        else:
            print("="*55)
            print("Invalid Hotel Name")
            print("Maybe Try Again")
            returntologin()
            hotellog()

def hoteladd():
    print("Please Be Patient Until Our Admins Review Your Registration")
    print("So Lets Get Your Details")
    hname=input("Please Enter The Name Of Your Restaurant: ").title()
    dis=input("Please Enter The District In Which The Restaurant Is Located: ").title()
    dis=check_district(dis)
    city=input("Please Enter The Major City/Town Nearest To Your Restaurant: ").title()
    city=check_city(city)
    print('='*55)
    cur.execute("insert into h_app(hname,dis,city) values(%s,%s,%s)",(hname,dis,city))
    X.commit()
    print("Please Check The Registration After An Admin Has Reviewed Your Registration")
    returntologin(5)
    hotellog()
           
def alogin():
    aid=input("Please Enter Your Admin ID: ")
    pwd=input("Please Enter Your Respective Password: ")
    if checklogin('a_cred','adm_id',aid,pwd,"Please Contact Another Admin To Resolve The Issue",False):
        print("="*55)
        print("LOGIN SUCCESSFULL".center(55))
        print('='*55)
        access.append('a')
        return
    else:
        print('='*55)
        print("Invalid Admin ID.Please Contact Another Admin To Resolve The Issue")
        returntologin(5)
        login()
    
        
def aterminal():
    print("[ADMIN TERMINAL]".center(55,'='))
    print('\t1.===>View Hotel Registrations')
    print("="*55)
    c=input("Please Input Your Required Choice(1/2/3/4): ")
    if c=='1':
        while True:
            cur.execute("Select hname,dis,city from h_app where approval is NULL") 
            data=cur.fetchall()
            if not any(data):
                print("No Current Registrations")
                a=input("Press s To Search Again/Press f To Return To Terminal: ").lower()
                if a.lower()=='f':
                    aterminal()
                    return
                elif a.lower()=='s':
                    continue
                else:
                    print("Invalid Choice. Searching Again")
            else:
                print("Alright Found Some Registrations To Approve/Reject")
                print("Lets Go Through Them One By One")
                h=['Hotel Name','District','City']
                for i in range(len(data)):
                    print(data[i][0])
                    print(tab([data[i]],headers=h,tablefmt='grid'))
                    ch=input("So What Do You Think(approve/reject)?: ").lower()
                    while ch not in ('approve','a','app','reject','r','rej'):
                        ch=input("I Think You have Made A Mistake.Please Input A Valid Option: ")
                    if ch in ('approve','a','app'):
                        print("Alright Someone Would Be Happy To Hear That")
                        print("Lets Move On To The Next")
                        cur.execute("update h_app set approval='y' where hname=%s",(data[i][0],))
                        X.commit()
                    elif ch in ('reject','r','rej'):
                        print("Well It Is What It Is")
                        print("Moving On")
                        cur.execute("update h_app set approval='n' where hname=%s",(data[i][0],))
                        X.commit()
                print("Well Thats All The Registrations There Is To Be Reviewed")
                print("Lets Go Back To The Terminal")
                aterminal()

def terminal():
    if any(access):
        print("Loading Details.Please Stanby")
        loadanimation('▰ ')
        print('='*55)
        if access[0]=='u':
            user_term()
                 
def login():
    access.clear()
    print("Lets Log You In To Your Account")
    print("Whats Your Access Level?")
    print("="*55)
    print("These Are Your Options:")
    print("\t1.----->User Login")
    print("\t2.----->Delivery Login")
    print("\t3.----->Hotel Login")
    print("\t4.----->Admin Login")
    print("="*55)
    c=input("Enter Your Choice (1/2/3/4): ")
    if c=='1':
        print("Excellent Now Lets Get Your Credentials")
        print('='*55)
        userlogin()
    elif c=='2':
        print("Ahoy!! Its Time For The Journey To Begin!!")
        print("But Before That")
        print('='*55)
        dellogin()
    elif c=='3':
        print("Alright Lets Get The Business Booming Shall We?")
        print("But Credentials First")
        print('='*55)
        hotellog()
    elif c=='4':
        print("Its Coding Time")
        print("But Verification First")
        print('='*55)
        #alogin()
        aterminal()
    terminal()

                
                
                





            


user_term() #Delete em statement too
#login()
X.close() 
