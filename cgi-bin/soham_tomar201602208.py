#!/usr/bin/python
import mysql.connector
import cgi
import os 
import cgitb; cgitb.enable()

def costQuery(cursor,cost):
    query="SELECT DISTINCT(Suppliers.sname) FROM Suppliers,Catalog WHERE Suppliers.sid=Catalog.sid AND Catalog.cost>="+str(cost)
    cursor.execute(query)
    return cursor.fetchall()

def supplierQuery(cursor,pname,sid,sname,address,cost):
    list_c=[sid,sname,address,cost]
    query="select"
    for i,j in enumerate(list_c):
        if j=="on" and i==0:
            query=query+ " Suppliers.sid,"
        elif j=="on" and i==1:
            query=query+" Suppliers.sname,"
        elif j=="on" and i==2:
            query=query+ " Suppliers.address,"
        elif j=="on" and i==3:
            query=query+" Catalog.cost"
        else:
            query=query+""
    if query[-1]==",":
        query=query[:-1]
    final_query=query+" FROM Parts,Catalog,Suppliers WHERE Suppliers.sid=Catalog.sid AND Catalog.pid=Parts.pid AND Parts.pname='"+ str(pname)+"'"
    cursor.execute(final_query) 
    return cursor.fetchall()

def pidQuery(cursor,pid):
    final_query="SELECT Suppliers.sname, Suppliers.address, Catalog.cost FROM Catalog, Suppliers WHERE Catalog.sid=Suppliers.sid AND Catalog.cost=((SELECT MAX(C2.cost) FROM Catalog C2 where C2.pid='" +str(pid) +"'"")) AND Catalog.pid='" + str(pid)+"'" 
    cursor.execute(final_query)
    return cursor.fetchall()

def color_addressQuery(cursor,color,address):
    final_query="SELECT P.pname FROM Parts P WHERE NOT EXISTS (SELECT Suppliers.sid FROM Suppliers WHERE Suppliers.address='" + str(address) +"'" "AND Suppliers.sid NOT IN (SELECT C.sid FROM Catalog C WHERE C.pid=P.pid AND P.color='"+ str(color)+"'""))"
    cursor.execute(final_query)
    return cursor.fetchall()

def addressQuery(cursor,address):
    final_query="SELECT Suppliers.sid, Suppliers.sname FROM Suppliers WHERE Suppliers.address='" + str(address)+"'" "AND Suppliers.sid NOT IN (SELECT Catalog.sid FROM Catalog)"
    cursor.execute(final_query)
    return cursor.fetchall()                                              
    

def displayPage(res):
    temp='<table>'
    for i in res:
        temp+='<tr>'
        for j in i:
            temp+=f'<td>{j}</td>'
        temp+='</tr>'
    temp+='</table>'
    print(temp)


print('''Content-type: text/html \n\n
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>
</head>
<body>

''')


# Main Program

database=mysql.connector.connect(
    host="localhost",
    user="root",
    password='password',
    database='SupplyDB'
)

cursor = database.cursor()

method = os.getenv('REQUEST_METHOD')


if method == 'POST':
    form = cgi.FieldStorage()
    if 'query1' in form:
        cost=form.getvalue('cost')
        query1=costQuery(cursor,cost)
        displayPage(query1)
    if 'query2' in form:
        query2=supplierQuery(cursor,form.getvalue('pname'),form.getvalue('sid'),form.getvalue('sname'),form.getvalue('address'),form.getvalue('cost'))
        displayPage(query2)
    if 'query3' in form:
        query3=pidQuery(cursor,form.getvalue('pid'))
        displayPage(query3)
    if 'query4' in form:
        query4=color_addressQuery(cursor,form.getvalue('color'),form.getvalue('address'))
        displayPage(query4)
    if 'query5' in form:
        query5=addressQuery(cursor,form.getvalue('address'))
        displayPage(query5)
print('</body></html>')
