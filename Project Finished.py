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
            access.extend(['u',em])
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
    cur.execute('select * from c_details where name=%s',(name,))
    while cur.fetchone() is not None:
        name = input("Please Try Another Name As That One Is Already Taken Up: ").title()
        cur.execute('select * from c_details where name=%s', (name,))
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
    em=access[1]
    cur.execute('select * from c_details where email=%s',(em,))
    details=cur.fetchone()
    print('='*55)
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
        menu=get_menu(hid)
        while True:
            if c1.isdigit() and 1<=int(c1)<=len(menu):
                q=int(input(f"How Many {menu[int(c1)-1][0]} would u like: "))
                cur.execute(f'insert into cart values %s'%((details[0],menu[int(c1)-1][0],menu[int(c1)-1][1],q),))
                X.commit()
            elif c1=='c':
                show_cart(details)
            elif c1=='f':
                cur.execute('Select SUM(price*quantity) from cart where customername=%s',(details[0],))
                tp=cur.fetchone()[0]
                show_cart(details)
                print("Your Total Price Comes Out To Be:",tp)
                c2=input("Would U Like To Place An Order[y/a(to add more)/c(to clear cart)]: ").lower()
                if c2=='y':
                    cur.execute('select * from cart where customername=%s',(details[0],))
                    order=[i+(hid,) for i in cur.fetchall()]
                    for i in order:
                        cur.execute('insert into orders(customername,food_items,price,quantity,h_id,status) values %s'%(i+('Order Placed',),))
                    cur.execute('delete from cart where customername=%s',(details[0],))
                    X.commit()
                    print("Order Has Been Placed")
                    print("Approximate Waiting Time:45 mins")
                    break
                elif c2=='a':
                    print("Lets Have A Look At The Menu Again Now Shall We?")
                    view_menu(hname,hid)
                    c1=input("What Other Item Would U Like: ")
                    continue
                else:
                    cur.execute("delete from cart where customername=%s",(details[0],))
                    X.commit()
                    print("Cart Has Been Cleared")
                    break
            else:
                print("It Seems You Have Made A Mistake. Please Try Again")
            c1 = input("Anything Else?(f to stop/c to check cart): ")
        print("Returning To Main Terminal", end='')
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
            cur.execute('select * from c_details where name=%s', (cname,))
            while cur.fetchone() is not None:
                cname = input("Please Try Another Name As That One Is Already Taken Up: ").title()
                cur.execute('select * from c_details where name=%s', (cname,))
            cur.execute('update c_details set name=%s where email=%s',(cname,details[3]))
            cur.execute('update cart set customername=%s where customername=%s', (cname, details[0]))
            cur.execute('update orders set customername=%s where customername=%s', (cname, details[0]))
            X.commit()
            print(f"Well Welcome {cname} Lets Get Going")

        elif choice2=='2':
            print("Moved Locations Huh? Well Lets Update That")
            dis=input("Enter Your New District:").title()
            dis=check_district(dis)
            city=input("Enter Your City:").title()
            city=check_city(city)
            cur.execute('update c_details set district=%s, city=%s where email=%s',(dis,city,details[3]))
            X.commit()
            print("Location Has Been Updated")

        elif choice2=='3':
            print("Now That's A Big Change")
            pwd=input("Lets Confirm Your Password: ")
            if checklogin('c_details','email',em,pwd,"Well You Seem To Be An Intruder",False,False):
                newem=input("Enter Your New Email Address: ").lower()
                pwd=input("Please Enter Your New Password: ")
                cur.execute('update c_details set passwd=%s, email=%s where email=%s',(pwd,newem,em))
                access[1]=newem
                print("Lets Continue And Don't Forget Your Password")
                X.commit()
            else:
                print("Logging You Out")
                returntologin(5)
                login()
                return
        print('='*55)
        print("Returning to Terminal", end='')
        loadanimation()
        print('=' * 55)
        user_term()
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
            elif status=='Preparing Food':
                print("Estimated Time Of Arrival: 30 mins")
            elif status=='Order Ready':
                print("Estimated Time Of Arrival: 20 mins")
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
            access.extend(['d',did])
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

def del_term():
    did=access[1]
    cur.execute("select * from d_details where D_ID=%s",(did,))
    details=cur.fetchone()
    print('='*55)
    print("Alright So What Would You Like To Do:")
    print('\t1.--->Start Delivering')
    print('\t2.--->Update Status To Receive Deliveries')
    print('\t5.--->Check Payouts')
    print('\t3.--->Update Details')
    print("\t4.--->Log Out")
    print('='*55)
    c1=input("Please Enter Your Choice(1/2/3/4/5): ")
    while c1 not in ('1','2','3','4','5'):
        c1=input("Please Enter A Valid Choice(1/2/3/4): ")
    print('='*55)
    if c1=='1':
        while True:
            cur.execute('select customername,h_id from delivery where d_id=%s',(did,))
            orders=cur.fetchall()
            if any(orders):
                ord=[(i,*order) for i,order in enumerate(orders,start=1)]
                print("This Is Your Current List Of Pending Deliveries:")
                print(tab(ord,headers=['S.No','Customer_Name','Hotel_Name'],tablefmt='grid'))
                print("Well Lets Go Through Them One By One")
                print('='*55)
                for i in ord:
                    cur.execute('select status from distinct orders where customername=%s',(i[1],))
                    status=cur.fetchone()
                    if status[0]!='Preparing Food':
                        cur.execute('select * from h_details where h_id=%s',(i[2],))
                        h_details=cur.fetchone()
                        print(f"Current Order To Be Delivered Is From:{h_details[1]}, Located At:{h_details[3]}")
                        print(f"This Is {i[1]}'s Order:")
                        cur.execute('select food_items,quantity,price*quantity as Price,order_id from orders where customername=%s',(i[1],))
                        cor=[(i,*value) for i,value in enumerate(cur.fetchall(),start=1)]
                        print(tab(cor,headers=['s.No','Food_Name','Quantity','Price'],tablefmt='grid'))
                        ans=input("Press y After You Have Picked Up The Delivery: ").lower()
                        while ans!='y':
                            ans = input("Press y After You Have Picked Up The Delivery: ").lower()
                        print("Status Has Been Updated To Out For Delivery")
                        cur.execute('update orders set status="Out For Delivery" where customername=%s',(i[1],))
                        X.commit()
                        ans = input("Press y After You Have Delivered The Food: ").lower()
                        while ans != 'y':
                            ans = input("Press y After You Have Delivered The Food: ").lower()
                        print("Order Has Been Successfully Delivered")
                        cur.execute("update d_details set tot_dels=tot_dels+1 where d_id=%s",(did,))
                        cur.excute("update d_details set mon_dels=mon_dels+1 where d_id=%s", (did,))
                        cur.execute("update orders set status='Completed' where order_id=%s",(cor[0][4],))
                        cur.execute('delete from delivery where customername=%s',(i[1],))
                        ans=input("Press y To Move On To The Next Delivery(f To Return To Terminal): ").lower()
                        if ans=='f':
                            print('=' * 55)
                            print("Returning to Terminal", end='')
                            loadanimation()
                            print('=' * 55)
                            del_term()
                            return
                    else:
                        print("It Seems That Order Is In The Preparing Phase Lets Check The Next One")
                        continue
            else:
                print("It Seems That You Currently Dont Have Any Delivery Requests")
                ans=input("Press y To Check Again(f To Return To Terminal): ").lower()
                while ans not in ('y','f'):
                    ans=input("Please Enter A Valid Choice(y/f): ")
                if ans=='y':
                    continue
                else:
                    print('=' * 55)
                    print("Returning to Terminal", end='')
                    loadanimation()
                    print('=' * 55)
                    del_term()
                    return

    elif c1=='2':
        if details[4]=='n':
            print("You Are Currently Unavailable to Receive Deliveries")
            ans=input("Would You Like To Start Receiving Deliveries?(y/n): ").lower()
            while ans not in ('y','n'):
                print("Invalid Choice.Please Try Again")
                ans = input("Would You Like To Start Receiving Deliveries?(y/n): ").lower()
            if ans=='y':
                cur.execute('update d_details set availability="y" where d_id=%s',(did,))
                X.commit()
                print("Status Updated Successfully")
            else:
                print("Well If That's What You Want Sure")
        else:
            print("You Are Currently Available To Receive Deliveries")
            ans = input("Would You Like To Stop Receiving Deliveries?(y/n): ").lower()
            while ans not in ('y', 'n'):
                print("Invalid Choice.Please Try Again")
                ans = input("Would You Like To Stop Receiving Deliveries?(y/n): ").lower()
            if ans=='y':
                cur.execute('update d_details set availability="n" where d_id=%s',(did,))
                X.commit()
                print("Status Updated Successfully")
            else:
                print("Well Lets Continue Delivering Then")
        print('=' * 55)
        print("Returning to Terminal", end='')
        loadanimation()
        print('=' * 55)
        del_term()

    elif c1=='3':
        print("Let's Look At The Numbers Shall We?")
        cur.execute("select tot_dels,Mon_dels from d_details where d_id=%s",(did,))
        dels=cur.fetchone()
        print("="*55)
        print(f"Ok So U Have Made A Total Of {dels[0]} Deliveries")
        print(f"Out Of These {dels[1]} Has Been Made This Month!!!")
        print(f"And You Have Made A Total Of ₹{dels[0]*50} And Made ₹{dels[1]*50} This Month!")
        print('=' * 55)
        print("Heading Back To Terminal", end='')
        loadanimation()
        del_term()
        return
    elif c1=='4':
        print('So Want To Change Some Details Huh?')
        print('=' * 55)
        print("But First What Do You Wish To Update")
        print('\t1.--->Name')
        print('\t2.--->Location')
        print('\t3.--->Credentials')
        print('=' * 55)
        choice2 = input("Enter Your Choice(1/2/3): ")
        while choice2 not in ('1', '2', '3'):
            choice2 = input("Please Enter A Valid Choice(1/2/3): ")

        if choice2 == '1':
            print("Lets Change That Old Name Shall We?")
            dname = input('Enter Your New Name: ').title()
            cur.execute('update d_details set name=%s where d_id=%s', (dname, did))
            X.commit()
            print(f"Well Welcome {dname} Lets Get Going")

        elif choice2 == '2':
            print("Moved Locations Huh? Well Lets Update That")
            dis = input("Enter Your New District:").title()
            dis = check_district(dis)
            city = input("Enter Your City:").title()
            city = check_city(city)
            cur.execute('update d_details set district=%s, city=%s where d_id=%s', (dis, city, did))
            X.commit()
            print("Location Has Been Updated")

        elif choice2 == '3':
            print("Now That's A Big Change")
            pwd = input("Lets Confirm Your Password: ")
            if checklogin('d_details', 'd_id', em, pwd, "Well You Seem To Be An Intruder", False, False):
                print("This Is Your Delivery Id Just To Remember:")
                print('='*55)
                print(did.center(55))
                print('='*55)
                pwd = input("Please Enter Your New Password: ")
                cur.execute('update c_details set passwd=%s where d_id=%s', (pwd, did))
                print("Lets Continue And Don't Forget Your Password")
                X.commit()
            else:
                print("Logging You Out")
                returntologin(5)
                login()
                return
        print('=' * 55)
        print("Returning to Terminal", end='')
        loadanimation()
        print('=' * 55)
        del_term()
        return

    elif c1=='5':
        print("Well Hope To See You Again")
        print("Logging Out")
        loadanimation('■',5)
        login()
        return
    
def hotellog():
    print('='*55)
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
            access.extend(['h',hid])
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
        while True:
            cur.execute("select exists(select dis,city,approval from h_app where hname=%s)",(hname,))
            if cur.fetchone()[0]==1:
                cur.execute("select dis,city,approval from h_app where hname=%s",(hname,))
                d=cur.fetchone()
                if d[2] is None:
                    print("Its Seems Your Registrations Hasn't Been Reviewed Yet")
                    ans = input("Press y To Check Again(f To Return To Login): ").lower()
                    while ans not in ('y', 'f'):
                        ans = input("Please Enter A Valid Choice(y/f): ")
                    if ans=='y':
                        continue
                    else:
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

def hot_term():
    hid=access[1]
    cur.execute('select * from h_details where h_id=%s',(hid,))
    details=cur.fetchone()
    print('='*55)
    print('What Would U Like To Do:')
    print('\t1.--->Look At Orders')
    print('\t2.--->Update Order Status')
    print('\t3.--->Update Menu')
    print('\t4.--->Look At Earnings')
    print("\t5.--->Update Credentials")
    print('\t6.--->Log Out')
    print('='*55)
    c1=input('Enter Your Choice(1/2/3/4/5/6): ')
    while c1 not in ('1', '2', '3', '4','5','6'):
        c1=input('Please Enter A Valid Choice(1/2/3/4/5/6): ')
    print('='*55)
    if c1=='1':
        cur.execute('select distinct customername from orders where h_id=%s',(hid,))
        cname=cur.fetchall()
        if any(cname):
            print("Alright Seems Like You Have Some Orders")
            print("Lets Go Through Em One by One")
            for i in range(len(cname)):
                name=cname[i][0]
                cur.execute('select customername,food_items,quantity,food_items*quantity from orders where customername=%s ',(name,))
                ord=cur.fetchall()
                print(f"This is {name}'s order")
                print(tab(ord,headers=['Name','Food Name','Quantity','Total Price'],tablefmt='grid'))
                ans = input("Press y To Update Status To Preparing Food(f to return to Terminal): ")
                while ans not in 'yf':
                    ans=input("Please Press y To Update Status To Preparing Food(f to return to Terminal): ")
                if ans=='y':
                    cur.execute('select sum(price*quantity) from orders where customername=%s ',(name,))
                    tot=cur.fetchone()[0]
                    print('='*55)
                    cur.execute('update orders set status="Preparing Food" where customername=%s',(name,))
                    cur.execute('update h_details set tot_profit = tot_profit+%s where h_id=%s',(tot,hid))
                    cur.execute('update h_details set mon_proft = mon_proft+%s where h_id=%s', (tot, hid))
                    cur.execute('update h_details set tot_dels = tot_dels+1 where h_id=%s',(hid,))
                    cur.execute('update h_details set mon_dels = mon_dels+1 where h_id=%s', (hid,))
                    X.commit()
                    print("Lets Look At Delivery Guys To Deliver That Order")
                    cur.execute('select d_id from d_details where district=%s and availability="y"',(details[2],))
                    dg=cur.fetchall()
                    l=[]
                    for i in dg:
                        cur.execute('select count(*) from delivery where d_id=%s',(i[0],))
                        l.append(cur.fetchone()[0])
                    index=l.index(min(l))
                    deliveryguy=dg[index]
                    cur.execute('insert into delivery values%s'%((deliveryguy[0],name,hid),))
                    X.commit()
                    print("="*55)
                    print(f"Great So The One To Deliver The Food Will Be {deliveryguy[1]}")
                    print("You Can Update The Status Furthur From The 'Update Status' Option")
                    print("See You Soon")

    if c1=='2':
        cur.execute('select customername,food_item,status from orders where h_id=%s and status="Preparing Food"',(hid,))
        orders=cur.fetchall()
        if any(orders):
            print("Well It Seems That Some Orders Are Currently Under Preparation")
            ord=[(i,*value) for i,value in enumerate(orders,start=1)]
            print(tab(ord,headers=['S.No','Name','Food Item']))
            print("Lets Go Throught Them One by One")
            name=orders[0][0]
            for i in orders:
                if i[0]==name:
                    print(f"Is {i[0]}'s {i[1]} Ready?")
                    ans=input("Press y To Update Status(f to return to terminal): ").lower()
                else:
                    print('='*55)
                    name=i[0]
                    print("Moving On To The Next Order")
                    print(f"Is {i[0]}'s {i[1]} Ready?")
                    ans = input("Press y To Update Status(f to return to terminal): ").lower()
                    while ans not in ('y','f'):
                        ans=input("You Have Made A Mistake.Press y/f: ").lower()
                if ans=='y':
                    cur.execute('update order set status="Order Ready" where customername=%s and food_item=%s',(i[0],i[1]))
                    X.commit()
                    continue
                elif ans=='f':
                    print("Returning To Terminal",end='')
                    loadanimation()
                    hot_term()
                    return
        else:
            print("Seems You Got No Orders On Preparation Status")
            print("Returning To Terminal",end='')
            loadanimation()
            hot_term()
            return

    elif c1=='3':
        print("So You Would Like To Change The Menu")
        print("Lets Get Straight To It")
        print("=" * 55)
        print(f"{details[1]}".center(55))
        print("=" * 55)
        cur.execute(f'select Food,Price from menus.`{hid}`')
        data = cur.fetchall()
        new_data = [(i, *value) for i, value in enumerate(data, start=1)]
        print(tab(new_data, headers=['S.No', 'Food Name', 'Price'], tablefmt='grid'))
        print('='*55)
        print("What Would You Like To Do?")
        print('\t1.--->Add Item')
        print('\t2.--->Update Price')
        print('\t3.--->Delete Item')
        c2=input("Enter Your Choice(1/2/3)(f to return to terminal): ")
        while c2 not in ('1','2','3','f'):
            c2=input("Please Enter A Valid Choice(1/2/3)(f to return to terminal): ").lower()
        print('='*55)
        if c2=='1':
            ans='y'
            while ans=='y':
                fname=input("Enter The Food Name: ").title()
                course=input("Enter What Course Is The Item In?: ").title()
                while course not in ('Breakfast','Lunch','Dinner','Starters','Desserts'):
                    print("Course Refers To Whether The Food Is Breakfast,Lunch,etc Item")
                    course=input(f"Please Enter A Valid Course For {fname}: ").title()
                price=int(input(f"Enter The Price Of {fname}: "))
                cur.execute(f'insert into menus.`{hid}` values(%s,%s,%s)',(fname,price,course))
                X.commit()
                ans=input("Press y To Add More Items(anything else to return to terminal): ").lower()
            print("Returning To Terminal",end='')
            loadanimation()
            hot_term()
            return
        elif c2=='2':
            ans='y'
            while ans=='y':
                sno=int(input("Which Item's Price Do U Wish To Update(use serial no.): "))
                item=data[sno-1]
                np=int(input(f"Enter The New Price Of {item[0]}: "))
                cur.execute(f'update menus.`{hid}` set price=%s where food=%s',(np,item[0]))
                X.commit()
                ans=input("Press y To Update more Items(anything else to return to terminal): ").lower()
            print("Returning To Terminal",end='')
            loadanimation()
            hot_term()
            return
        elif c2=='3':
            ans = 'y'
            while ans == 'y':
                sno = int(input("Which Item's Price Do U Wish To Delete(use serial no.): "))
                fname=data[sno-1][0]
                print(f'Removing {fname} From The Menu')
                cur.execute(f'delete from menus.`{hid}` where food=%s',(fname,))
                X.commit()
                ans=input("Press y To Delete More Items(anything else to return to terminal): ").lower()
            print("Returning To Terminal",end='')
            loadanimation()
            hot_term()
            return

    elif c1=='4':
        print("Lets Have A Look At The Earning Now Shall We?")
        cur.execute('select Tot_dels,Mon_dels,tot_profit,mon_profit from h_details where h_id=%s',(hid,))
        data=cur.fetchone()
        print(f"So It Seem You Have Made A Total Of {data[0]} Deliveries")
        print(f'Out Of Which {data[1]} Were Made This Month')
        print(f"So The Net Profit Is ₹{data[2]} Out Of Which ₹{data[3]} Were Made This Month")
        print("Returning To Terminal", end='')
        loadanimation()
        hot_term()
        return

    elif c1=='5':
        print("The Only Thing You Can Update Through This Program Is Your Name")
        print("For Any Furthur Updation In Location/Hotel-Id/Password, Please Contact An Admin")
        ans=input("So Would You Like To Upadate The Hotel Name(y for yes/f to return to terminal): ").lower()
        while ans not in 'yf':
            ans=input("Please Enter A y/f: ")
        if ans=='y':
            new_name=input(f'So What Will Be New Name Of {details[1]}?: ')
            cur.execute("update h_details set h_name=%s where h_id=%s",(new_name,hid))
            X.commit()
        print("Returning To Terminal", end='')
        loadanimation()
        hot_term()
        return

    elif c1=='6':
        print("Well See You Another Time")
        returntologin(5)
        login()















def alogin():
    aid=input("Please Enter Your Admin ID: ")
    pwd=input("Please Enter Your Respective Password: ")
    if checklogin('a_cred','adm_id',aid,pwd,"Please Contact Another Admin To Resolve The Issue",False):
        print("="*55)
        print("LOGIN SUCCESSFULL".center(55))
        print('='*55)
        access.extend(['a',aid])
        return
    else:
        print('='*55)
        print("Invalid Admin ID.Please Contact Another Admin To Resolve The Issue")
        returntologin(5)
        login()
    
        
def aterminal():
    print("=" * 55)
    print("[FEASTFLOW ADMIN TERMINAL]".center(55))
    print("=" * 55)
    print("\t1. ---> Review Hotel Registrations")
    print("\t2. ---> View Registered Hotels")
    print("\t3. ---> View Current Orders")
    print("\t4. ---> View Delivery Partners")
    print("\t5. ---> View Project Statistics")
    print("\t6. ---> View Hotel Earnings")
    print("\t7. ---> Log Out")
    print("=" * 55)
    c=input("Please Input Your Required Choice(1/2/3/4/5/6/7): ")
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
    elif c == '2':
        cur.execute("SELECT h_id, h_name, district, city, tot_dels, mon_dels FROM h_details ORDER BY h_name")
        hotels = cur.fetchall()
        if hotels:
            print(tab(hotels, headers=["Hotel ID", "Hotel Name", "District", "City", "Total Deliveries","Monthly Deliveries"], tablefmt="grid"))
        else:
            print("No Registered Hotels Found.")
    elif c == '3':
        cur.execute(
            "SELECT o.customername, h.h_name, o.food_items, o.price, o.quantity, o.price*o.quantity, o.status FROM orders o LEFT JOIN h_details h ON o.h_id=h.h_id ORDER BY o.customername")
        orders = cur.fetchall()
        if orders:
            print(tab(orders,
                      headers=["Customer", "Hotel", "Food Item", "Unit Price", "Quantity", "Item Total", "Status"],
                      tablefmt="grid"))
        else:
            print("There Are No Current Orders.")
    elif c == '4':
        cur.execute("SELECT d_id, name, district, city, availability, tot_dels, mon_dels FROM d_details ORDER BY name")
        partners = cur.fetchall()
        if partners:
            print(tab(partners, headers=["Delivery ID", "Name", "District", "City", "Availability", "Total Deliveries","Monthly Deliveries"], tablefmt="grid"))
        else:
            print("No Delivery Partners Found.")
    elif c == '5':
        cur.execute("SELECT COUNT(*) FROM h_details")
        hotels = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM d_details")
        partners = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM h_app WHERE approval IS NULL")
        pending = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM orders")
        order_items = cur.fetchone()[0]
        cur.execute("SELECT COALESCE(SUM(price*quantity), 0) FROM orders")
        order_value = cur.fetchone()[0]
        print("=" * 55)
        print("FEASTFLOW PROJECT STATISTICS".center(55))
        print("=" * 55)
        print(f"Registered Hotels        : {hotels}")
        print(f"Delivery Partners        : {partners}")
        print(f"Pending Applications     : {pending}")
        print(f"Food Item Rows in Orders : {order_items}")
        print(f"Current Order Value      : Rs. {float(order_value):.2f}")
        print("=" * 55)
    elif c == '6':
        cur.execute("SELECT h_name, tot_profit, mon_profit, tot_dels, mon_dels FROM h_details ORDER BY tot_profit DESC")
        earnings = cur.fetchall()
        if earnings:
            print(tab(earnings,headers=["Hotel", "Total Earnings", "Monthly Earnings", "Total Deliveries", "Monthly Deliveries"],tablefmt="grid"))
        else:
            print("No Hotel Earnings Available.")
    elif c == '7':
        print("Logging Out Of Admin Account...")
        access.clear()
        login()
        return

def terminal():
    if any(access):
        print("Loading Details.Please Standby")
        loadanimation('▰ ')
        print('='*55)
        if access[0]=='u':
            em = acces[1]
            cur.execute('select * from c_details where email=%s', (em,))
            details = cur.fetchone()
            print(f"Ok So What We Doing Today {details[0]}?")
            user_term()
        if access[0]=='d':
            did = access[1]
            cur.execute("select * from d_details where D_ID=%s", (did,))
            details = cur.fetchone()
            print(f"Welcome {details[1]} Lets Start Earning and Delivering")
            del_term()
        elif access[0]=='h':
            hot_term()
        elif access[0]=='a':
            aterminal()
                 
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
        alogin()
    terminal()

                
                
                




#orders(customername,food_items,price,quantity,h_id,status)
#d_details(d_id,name,district,city,availability,Tot_dels,Mon_dels)
#delivery(d_id,customername,h_id)
#h_details(h_id,h_name,district,city,tot_dels,mon_dels,tot_profit,mon_profit)

#del_term()
#hot_term()
login()
X.close() 
