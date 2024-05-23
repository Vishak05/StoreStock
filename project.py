#import mysql.connector as sql
from cs50 import SQL

ur = SQL("sqlite:///av.db")
#con = sql.connect(host='localhost', user='root', password='mysql')
#ur = con.cursor()
#ur.execute('create database if not exists av')
#ur.execute('use av')
ur.execute('create table if not exists stock(itm_no int, name varchar(25), stock int, price int)')
#con.commit()


def insert_itm():
    ino = int(input("Enter item number: "))
    iname = input("Enter itam name: ")
    istock = int(input("Enter amount of item left: "))
    iprice = int(input("Enter price of item: "))
    query = "insert into stock values({}, '{}', '{}', {})".format(ino, iname, istock, iprice)
    ur.execute(query)
    #con.commit()
    print("STOCK UPDATED")


def display_itm():
    query = 'select * from stock order by price desc'
    result = ur.execute(query)
    print('%10s' % 'Item NO.', '%10s' % 'Name', '%10s' % 'Stock', "\t\t Price")
    for i in result:
        print('%10s' % i['itm_no'], '%10s' % i['name'], '%10s' % i['stock'], '\t\t', i['price'])


def update_stock(ino):
    query = 'select * from stock where itm_no = {}'.format(ino)
    result = ur.execute(query)

    if len(result) == 0:
        print("ITEM NOT FOUND!")
    else:
        print('\t\tItem No.', '\t\t Name', '\t\t Stock', '\tPrice')
        for i in result:
            print('\t\t', i['itm_no'], '\t\t', i['name'], '\t\t', i['stock'], '\t\t', i['price'])
            a = input("Do you want to continue?(y/n): ")
            if a.lower() == 'y':
                s = int(input("Enter new stock: "))
                query = 'update stock set stock = {}'.format(s)
                ur.execute(query)
                #con.commit()
                print("STOCK UPDATED")
            else:
                break


def sale():
    ans = 'y'
    while ans.lower() == 'y':
        total = 0
        ino = list(input("Enter item numbers being sold: "))
        for i in ino:
            quantity = int(input("Enter quantity of item: "))
            update_stock(i)
            r = ur.execute('select * from stock where itm_no = {}'.format(i))
            subtotal = r[0]['price'] * quantity
            total = total + subtotal

        print("Total amount: ", total)

option = 'yes'
while option != 0:
    print('1.Add Item',
          '2.Display Items',
          '3.Update Stock',
          '4.Sell',
          '0.Exit',
          sep='\n')
    option = int(input("Enter Option: "))
    if option == 1:
        insert_itm()
        option = input("Do you want to continue? (yes/no)")

    elif option == 2:
        display_itm()
        choice = input("Do you want to continue? (yes/no)")

    elif option == 3:
        ino = int(input("Enter item number to update: "))
        update_stock(ino)
        choice = input("Do you want to continue? (yes/no)")

    elif option == 4:
        sale()
        choice = input("Do you want to continue? (yes/no)")

    else:
        print("Program Exited")
