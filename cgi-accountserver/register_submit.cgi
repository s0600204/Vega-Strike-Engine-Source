#! /usr/bin/python

import cgi
import sys
import os
import string
import cgitb; cgitb.enable()


header = """
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">
<html>
<head>
  <title>Account Creation Results</title>
</head>
<body>
"""

footer = """
</body>
</html>
"""
errorvar="<br><a href=\"http://graphics.stanford.edu/cgi-bin/danielrh/register.cgi\">Return To Account Creation Form </a>"
def checkString(s):
  foundyet=False
  for c in s:
    if "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_-0123456789.".find(c)==-1:
        if not foundyet:
            print header
            foundyet=True
        print "Error: invalid character "+c+" in input "+s+"<br>"
  if s.find("..")!=-1 or s.find(".xml")!= -1 or s.find(".save")!=-1 or s.find("accounts")!=-1 or s.find("default")!=-1:
    if not foundyet:
        print header
        foundyet=True
    print "Error: invalid characters .. or .xml or .save in input "+s+"<br>"
  if foundyet:
    print errorvar
    print footer
    sys.exit(0)
def check_form(form):
    if not (form.has_key("type") and \
            form.has_key("username") and \
            form.has_key("faction") and \
            form.has_key("password") ):
        print header
        print "Error: please fill out all fields."
        print errorvar
        print footer
        sys.exit(0)
def write_abstract_page(f, presenter, title, abstract):
    #replace newlines with paragraph tags for nice html formatting.
    abstract = abstract.replace('\n','</p>\n<p>')
    
    f.write('<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN">\n<html>\n<head>\n')
    f.write('<title>%s: %s</title>\n' % (presenter, title))
    f.write('</head>\n')
    f.write('<body>\n')
    f.write('<h1>%s</h1>\n' % title)
    f.write('<h2>%s</h2>\n' % presenter)
    f.write('<p>%s</p>' % abstract)
    f.write('<hr> <a href="../index.html">GCafe lecture series</a></body></html>')


form = cgi.FieldStorage()
check_form(form)
username = form["username"].value
password = form["password"].value
faction = form["faction"].value
type = form["type"].value
checkString(username)
checkString(password)
checkString(type)
checkString(faction)
lok=-1
iter=100
import traceback
for i in range(iter):
  try:
    lok=os.open ("/u/danielrh/win/acctserver/lock",os.O_EXCL|os.O_CREAT)
    break
  except:
    pass
if 0 and lok==-1:
  lok=os.open ("/u/danielrh/win/acctserver/lock",os.O_EXCL|os.O_CREAT)
if lok==-1:
  print header
  print "Failed to write to database at this time... please retry"
  print errorvar
  print footer
  sys.exit(0)
s="BLAH"
try:
  f=open("/u/danielrh/win/acctserver/accounts/accounts.xml","rb")
  s=f.read()
  f.close()
  namstr='name="'+username+'"'
  passtr=' password="'+password+'"'
  success=False
  if s.find(namstr)!=-1:
      if s.find(namstr+passtr)!=-1:
           success=True
  else:
      where=s.rfind("</accounts>")
      if where!=-1:
          s=s[0:where]
      s+='<player '+namstr+passtr+' />\n'
      s+='</accounts>\n';
      success=True
  if success:
    f=open("/u/danielrh/win/acctserver/accounts/accounts.xml","wb")
    f.write(s)
    f.close()
except:
  os.close(lok)
  os.unlink("/u/danielrh/win/acctserver/lock")
  print header
  traceback.print_exc()
  print errorvar
  print footer
  sys.exit(0)
os.close(lok)
os.unlink("/u/danielrh/win/acctserver/lock")
if not success:
  print header
  print "Error password for username "+username+" does not match our records"
  print errorvar
  print footer
  sys.exit(0)




print header
f=open("/u/danielrh/win/acctserver/accounts/default.save","rb")
s=f.read()
f.close()
import random
o=open("/u/danielrh/win/acctserver/accounts/"+username+".save","wb")
s=s.replace("^llama.begin 0 0 0 neutral","^"+type+" "+str(random.uniform(-10000,10000))+" "+str(random.uniform(-10000,10000))+" "+str(random.uniform(-10000,10000))+" "+faction)
o.write(s)
o.close()
o=open("/u/danielrh/win/acctserver/accounts/"+username+".xml","wb")
unfp=open("/u/danielrh/win/acctserver/units/units.csv")
if not unfp:
  print header
  print "CRITICAL ERROR, not able to open units.csv"
  print footer
  sys.exit(0)
type_dat = unfp.readlines()
unfp.close()
if len(type_dat)>3:
    o.write(type_dat[0])
    o.write(type_dat[1])
    for line in type_dat[2:]:
        
        if (len(line) and line.find("turret")==-1):
           name=""
           if line.find("./weapons")!=-1:
               break
           if line[0]=='"':
               endl=line[1:].find('"')
               if endl!=-1:
                  name=line[1:1+endl] 
           else:
               endl=line.find(",")
               if endl!=-1:
                   name=line[:endl]
           if (len(name) and name.find("__")==-1 and name.find(".blank")==-1 and name!="beholder"):
               if name==type:
                   o.write(line)
                   break;
o.close()
# open the title/abstract page for writing
# if it already exists, it will be overwritten
#abstract_file = open("/usr/graphics/www/private/gcafe/abstracts/" + abstract_filename, 'w')
#write_abstract_page(abstract_file, presenter, title, abstract)
#abstract_file.close()

#update_gcafe_dat(presenter, title, abstract_filename)
#regenerate_gcafe_index()
def makeForm(s,v):
    print '<tr>'
    print '<td align= "right"></td>'
    print '<td><select name="'+s+'" size="1">'
    print '<option>'+v+'</option>'
    print '</select></td>'
    print '</tr>'
	
print '<h2>Account Created Successfully.</h2>\n'
print "<p>Username "+username+" in type: "+type+"</p>"
#print '<form name="type" action="http://graphics.stanford.edu/cgi-bin/danielrh/vegastrike.config" method="post">'
#makeForm("username",username);
#makeForm("password",password);
#print '<input value="Get matching vegastrike.config" type="submit">'
#print '</form>'
print '<br>'
print 'Download functional <a href="http://graphics.stanford.edu/cgi-bin/danielrh/vegastrike.config?username='+username+';password='+password+'">vegastrike.config</a> to put in your vegastrike folder that has your appropriate login and password<br>'
print footer