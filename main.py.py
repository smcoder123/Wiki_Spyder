import os
import re
import requests
from bs4 import BeautifulSoup
from xml.etree.ElementTree import Element,SubElement,Comment,tostring,XML,ElementTree

os.chdir("Directory name")    
f = open('user_info.txt', 'r',encoding="utf8")
data=[]
kera=[]

for line in f:
    data.append(line) 
    v = line.split('::')[1]
    kera.append(v)

       
link=[]
link2=[]
for ii in range(len(kera)):
    link2.append((kera[ii].replace("\n","")))
    link.append(link2[ii]+'/main_edits')


print("Creation of the directory will begin after a moment")



#Directory is created now its time for the file creation.

for k in range(40341,len(link2)):
  os.chdir("DIrectory")
  try:
    os.makedirs(link[k])  
  except:
     print("The file is already present")
    
  print("directory is already present")
  print(link2[k])
  url="https://en.wikipedia.org/w/index.php?limit=500&title=Special%3AContributions&contribs=user&target="+link2[k]+"&namespace=&tagfilter=&start=&end="
  try:
     rr1=requests.get(url)
  except requests.exceptions.ConnectionError:
     url.status_code="Connection refused" 
      
  soup=BeautifulSoup(rr1.text,'lxml')


#extracting the name of the user part.
  user=[]
  for a in soup.find_all('a',class_='mw-contributions-title'):
      user.append(a.text)
  

#Exrtracting the timestamps of the pages
  Timestamp=[]
  for  b in soup.find_all('a',class_="mw-changeslist-date"):
    Timestamp.append(b.text)

#Extraction of the urls of the diff of different users.
  diff_links=soup.find_all('a',class_='mw-changeslist-diff')
  lists=""
  for linkk in diff_links:
     lists=lists+("mmxxhttps://en.wikipedia.org"+linkk.get('href'))
    
     #creation of list of the talk pages of the users ie list_talkusers
     list_diff=lists.split('mmxx')   
     list_diff.pop(0)

#Checking reverted or not.
  rev=[]
  for revv in soup.find_all('span',class_="comment comment--without-parentheses"):
         rev.append(revv.text)


#Extraction of that timestamps in the form of a list.
  timestamps=soup.find_all('a',class_='mw-changeslist-date')
  time=[]
  for io in timestamps:
    #print(i.text)
    time.append(io.text)
#print(time)#jst writing the main part
  i=0
  for i in range(len(list_diff)):
   try:
    txt =user[i]
    x = re.search("^Talk",txt)
    y = re.search("^User",txt)
    z = re.search("^Wikipedia",txt)
  

    if (x):
      pass
    elif(y):
      pass
    elif(z):
      pass
    else:
      URL1=list_diff[i]
      rr=requests.get(URL1)
      soup=BeautifulSoup(rr.text,'html.parser')
      page_main_heading=soup.find('h1')
      
      #creation of one 4 lists
      wrong_text=[]
      corrected_text=[]
      list_wrong=[]
      list_correct=[]
      jj=-1
      for l in soup.find_all('td',class_='diff-context'):
          jj+=1
          if jj%2==0: 
             wrong_text.append(l.text)   
          else:
              corrected_text.append(l.text)
      for m in soup.find_all('td',class_='diff-deletedline'):
          list_wrong.append(m.text)
      for n in soup.find_all('td',class_='diff-addedline'):
          list_correct.append(n.text)
      for m in soup.find_all('td',class_='diff-deletedline'):
          list_wrong.append(m.text)
      for n in soup.find_all('td',class_='diff-addedline'):
          list_correct.append(n.text)
        
      
      
      #Creation of that etree.
      top=Element('edit')
     
      tree=ElementTree(top)
      filename1="Generated for edit"+str(i)
      comment=Comment(filename1)
      top.append(comment)
      try:
         timestamp=SubElement(top,'timestamp')
         timestamp.text=time[i]
      except:
          pass
        # try:
#        reverted=SubElement(top,'reverted')
#        reverted.text=rev[i]
#      except:
#        pass
      prevtext=SubElement(top,'prevtext')
      
      
      for kk in  range(len(wrong_text)):
        try: 
          if wrong_text[kk]!='':  
            line=SubElement(prevtext,'line')
            line.text=wrong_text[kk].replace("[[","<ahref>").replace("]]","</ahref>").replace('<ins class="diffchange diffchange-inline"',"<BLUE>").replace("</ins>","</BLUE>").replace("Image","<Image>").replace(".jpg",".jpg</Image>").replace("&lt;ahref&gt","<ahref>").replace("&lt;/ahref&gt","</ahref>").replace("&lt;ref&gt","<ref>").replace("&lt;/ref&gt","</ref>")
        except:
          pass
      for xx in range(len(list_wrong)):
        try:  
          if list_wrong[xx]!='':
                Minus=SubElement(prevtext,'Minus')
                Minus.text=list_wrong[xx].replace("[[","<ahref>").replace("]]","</ahref>").replace('<ins class="diffchange diffchange-inline"',"<BLUE>").replace("</ins>","</BLUE>").replace("Image","<Image>").replace(".jpg",".jpg</Image>").replace("&lt;ahref&gt","<ahref>").replace("&lt;/ahref&gt","</ahref>").replace("&lt;ref&gt","<ref>").replace("&lt;/ref&gt","</ref>")
        except:
          pass
      current_text=SubElement(top,'current_text')
      for zz in range(len(corrected_text)):
          if wrong_text[zz]!='': 
            lines=SubElement(current_text,'lines')
            lines.text=corrected_text[zz].replace("[[","<ahref>").replace("]]","</ahref>").replace('<ins class="diffchange diffchange-inline"',"<BLUE>").replace("</ins>","</BLUE>").replace("Image","<Image>").replace(".jpg",".jpg</Image>").replace("&lt;ahref&gt","<ahref>").replace("&lt;/ahref&gt","</ahref>").replace("&lt;ref&gt","<ref>").replace("&lt;/ref&gt","</ref>")
    
      for w in range(len(list_correct)):
         try:
          if list_correct[w]!='':
              plus=SubElement(current_text,'plus')
              plus.text=list_correct[w].replace("[[","<ahref>").replace("]]","</ahref>").replace('<ins class="diffchange diffchange-inline"',"<BLUE>").replace("</ins>","</BLUE>").replace("Image","<Image>").replace(".jpg",".jpg</Image>").replace("&lt;ahref&gt","<ahref>").replace("&lt;/ahref&gt","</ahref>").replace("&lt;ref&gt","<ref>").replace("&lt;/ref&gt","</ref>")
         except:
              pass
      

      #try:
      os.chdir("\\Directory\\"+link2[k]+"\\main_edits")      
      filename="edit"+str(i)+".xml"
      tree.write(filename)
      bb = open(filename,'r').read()
      bs = BeautifulSoup(bb, 'xml')
      pp=bs.prettify()
      
       
     
      with open(filename,'w',encoding='utf-8') as file:
            file.write(pp)
      file.close
 
       ##  print("The file was not created")
    
    print(i)
    print(k)
   except:
       print("The user ws missed")

  #%%PART @2  
#for k in range(len(link2)): 
 #try: 
  url="https://en.wikipedia.org/w/index.php?limit=500&title=Special%3AContributions&contribs=user&target="+link2[k]+"&namespace=&tagfilter=&start=&end="
  rr11=requests.get(url)
  soup=BeautifulSoup(rr11.text,'html.parser')
 # extracting the name of the user part.
  user=[]
  for a in soup.find_all('a',class_='mw-contributions-title'):
      user.append(a.text)
  

#Exrtracting the timestamps of the pages
  Timestamp=[]
  for  b in soup.find_all('a',class_="mw-changeslist-date"):
      Timestamp.append(b.text)
  #using that of the regular expression for the work.

  topname='Edit_Article'
  top=Element(topname)
  tree=ElementTree(top)
  for i in range(len(user)):
#    text_to_search=user[i]
#    pattern=re.compile(r'^User')
#    matches=pattern.finditer(text_to_search)
#    for match in matches:
#      print(matches)
#    

    txt =user[i]
    x = re.search("^Talk",txt)
#  topname='edit'
#  top=Element(topname)
#  tree=ElementTree(top)
    if (x):
      
        filename1="Generated for Talk_Article"+str(i)
        comment=Comment(filename1)
        top.append(comment)
        timestamp=SubElement(top,'timestamp')
        try:
            timestamp.text=Timestamp[i]
        except:
            pass
        Username=SubElement(top,'Username')
        Username.text=user[i]
    
    
#  filename="UserTalk"+str(i)+".xml"
#  tree.write(filename)
#      
#      bb = open(filename,'r').read()
#      bs = BeautifulSoup(bb, 'xml')

      
    else:
      print("No match")
      continue
  
  filename="Talk_Article"+".xml"
  os.chdir("Directory\\"+link2[k])
  tree.write(filename)
      
  bb = open(filename,'r').read()
  bs = BeautifulSoup(bb, 'xml')
  rr=bs.prettify()
      

      
  with open(filename,'w',encoding='utf-8') as file:
          file.write(rr)
  file.close
  print("Talk Article file is created for the user")
  print(k)
#%%PART 3      
#for k in range(len(link2)):  
 #try: 
  url="https://en.wikipedia.org/w/index.php?limit=500&title=Special%3AContributions&contribs=user&target="+link2[k]+"&namespace=&tagfilter=&start=&end="
  rr67=requests.get(url)
  soup=BeautifulSoup(rr67.text,'html.parser')
      
      
  user=[]
  for a in soup.find_all('a',class_='mw-contributions-title'):
      user.append(a.text)

#Exrtracting the timestamps of the pages
  Timestamp=[]
  for  b in soup.find_all('a',class_="mw-changeslist-date"):
          Timestamp.append(b.text)
#using that of the regular expression for the work.

  topname='Administrators'
  top=Element(topname)
  tree=ElementTree(top)
  for i in range(len(user)):
#    text_to_search=user[i]
#    pattern=re.compile(r'^User')
#    matches=pattern.finditer(text_to_search)
#    for match in matches:
#      print(matches)
#    

    txt =user[i]
    x = re.search("^Wikipedia",txt)
#  topname='edit'
#  top=Element(topname)
#  tree=ElementTree(top)
    if (x):
      
        filename1="Generated for Wikipedia Administrator"+str(i)
        comment=Comment(filename1)
        top.append(comment)
        try:  
          timestamp=SubElement(top,'timestamp')
          timestamp.text=Timestamp[i]
        except:
          pass
        Username=SubElement(top,'Username')
        Username.text=user[i]
        
     
    else:
      print("No match")
      continue
  #os.chdir("main_directory_link"+link2[k])
  filename="file for Administrators"+".xml"
      
  tree.write(filename)
      
  bb = open(filename,'r').read()
  bs = BeautifulSoup(bb, 'xml')
  rr=bs.prettify()
     

  with open(filename,'w',encoding='utf-8') as file:
       file.write(rr)
  file.close
#extracting the name of the user part.
 #%%Part4
#for k in range(len(link2)):    
# try: 
  url="https://en.wikipedia.org/w/index.php?limit=500&title=Special%3AContributions&contribs=user&target="+link2[k]+"&namespace=&tagfilter=&start=&end="
  rr78=requests.get(url)
  soup=BeautifulSoup(rr78.text,'html.parser')
  user=[]
  for a in soup.find_all('a',class_='mw-contributions-title'):
     user.append(a.text)
  

#Exrtracting the timestamps of the pages
  Timestamp=[]
  for  b in soup.find_all('a',class_="mw-changeslist-date"):
     Timestamp.append(b.text)
      #using that of the regular expression for the work.

  topname='edit'
  top=Element(topname)
  tree=ElementTree(top)
  for i in range(len(user)):

   txt =user[i]
   x = re.search("^User",txt)
   if (x):
            filename='usertalk'+str(i)+'.xml'
            filename1="Generated for edit"+str(i)
            comment=Comment(filename1)
            top.append(comment)
            try:   
               timestamp=SubElement(top,'timestamp')
               
               timestamp.text=Timestamp[i]
            except:
                pass
            #print("\n")
            Username=SubElement(top,'Username')
            Username.text=user[i]
        
     
   else:
          print("No match")
          continue
  filename="UserTalk"+".xml"
  tree.write(filename)
      
  bb = open(filename,'r').read()
  bs = BeautifulSoup(bb, 'xml')
  rr=bs.prettify()
    
  with open(filename,'w',encoding='utf-8') as file:
              file.write(rr)
  file.close

  print(k)

print("The Program was terminated")
######################################################################################           
