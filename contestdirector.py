#Contest Director Script 
#Pulls shows from Atlanta area venues that WREK regularly gets tickets from, 
#including the Terminal West, the Masquerade, Variety Playhouse, 529, and 
#the Earl

import urllib.request
from re import findall
from tkinter import *
import datetime
import os

class shows:

    def __init__(self):
        
        #open file to write everything in folder of script in .txt file named "WrekShows.txt"
        
        self.myfile = open("WrekShows.txt", "w")
        
        #call scrapfing functions for each venue
        #as of December 2017, Masquerade, 529, and The Earl are functional

        #twest access denied as of 03/05/17, need to implement urllib request instead
        #of normal access
        
        #self.twest()
        #fix variety
        #self.variety()
        #self.masq()


        self.five29()
        self.earl()
        
        print("file named Wrekshows.txt saved in directory")
        
        self.myfile.close()
        os.startfile("WrekShows.txt")
        
    def masq(self):
        self.myfile.write("Masquerade Shows"+'\n')
        
        #scrape masquerade show page
        response= urllib.request.urlopen('http://www.masqueradeatlanta.com/')
        html=response.read()
        text=html.decode()        
        
        #regex for all info 
        both2='''"grey_title">(.+)<span.+$[\n\t\s]+<a.+[\n\t\s]+.+break-word;".([A-Za-z0-9\s]+).+[\n\t\s]+.+artist".(.*)<...[\n\t\s]+<.+>[\n\t\s]+<p class="event_info">([:0-9AMPM\s]+)'''
        #format to regex across multiple lines is as follows:
        #this one doesn't match across multiple formats
        
        namesandsup=findall(both2,text,re.MULTILINE)
        response= urllib.request.urlopen('http://www.masqueradeatlanta.com/')
        html=response.read()
        page2=html.decode()
        response= urllib.request.urlopen('http://www.masqueradeatlanta.com/')
        html=response.read()
        page3=html.decode()

        #page 2 and 3, append lists to namesandsup
        page2info=findall(both2,page2,re.MULTILINE)
        
        page3info=findall(both2,page3,re.MULTILINE)
        allMasqShows=namesandsup
        
        #make into one list, filter list for correct format for page 2 and 3
        
        for each in page2info:
            allMasqShows.append(each)

        for each in page3info:
            allMasqShows.append(each)
            
        #fix appending list again for supported by
            
        masqInFormat=[]
        for i in allMasqShows:
            date=i[0][4:]
            time=i[3]
            name=i[1]
            #account for i[2] conditions

            #fix to account for multiple conditions with
            
            if i[2] != '':
                if '|' in i[2]:
                    bar=i[2].find('|')
                    if len(str(bar))==1:
                        supportedby='with ' + str(i[2][0:bar-6]) + 'and '+ str(i[2][bar+6:])
                    else:
                        supportedby='with ' + str(i[2][0:bar-6]) + 'and '+ str(i[2][bar+6:])
                else:
                    supportedby='with ' + i[2]
                

            else:
                supportedby=''
            masqInFormat.append([date,time,name,supportedby])
        masqInFormat.sort()
        
        #write to myfile
        
        for each in masqInFormat:
            self.myfile.write('\t'+ each[2]+' '+each[0]+' '+each[1]+'\n')
        print('\n')
        
    def twest(self):
        #scraping has been denied from this site
        #scrape twest site
        
        sites=['http://www.terminalwestatl.com/','http://www.terminalwestatl.com/page/2/','http://www.terminalwestatl.com/page/3/']
        twestshows3=[]
        
        for each in sites:
            response= urllib.request.urlopen(each)

            #make regex for twest
            
            regex='''title="(.+)"\s.><.a>[\n\s\t]+.+[\n\s\t]+.+"dates">....(.+)<.h2>[\s\n\t]+<h2.+[\s\n\t]+.+Show:\s([0-9:\spm]+)'''
            html=response.read()
            text=html.decode()
            regex2='''title=.(.+)".+[\s\d\t]+<.+[\s\d\t]+<h2\sclass=.+[\s\d\t]+<h2\sclass="supports description"><.+>(.+)<.a><.h2>[\s\d\t]+.+>....(.+)<.h2>[\s\d\t]+<h2.+[\s\d\t]+.+Doors:\s([0-9 pm:]+)+'''

            twestshows=findall(regex,text,re.MULTILINE)
            twestshows2=findall(regex2,text,re.MULTILINE)
        
            #twest shows 3=edited twest shows
            
            for each in twestshows2:
                lol="with " + str(each[1])
                twestshows3.append([each[0],lol,each[2],each[3]])
            self.twestshows3=twestshows3
            self.twestshows=twestshows

        #write shows to big file
        self.myfile.write("Terminal West Shows"+'\n\n')
    
        for each in range(len(self.twestshows3)):
            
            line=self.twestshows3[each][2]+' '+self.twestshows3[each][3]+' '+self.twestshows3[each][0]+' '+self.twestshows3[each][1]+ '\n'
            self.myfile.write(line)
        print('\n')
        
    def five29(self):
        self.myfile.write("529"+'\n\n')
        #scrape 529 show page
        
        response= urllib.request.urlopen('http://529atlanta.com/')
        html=response.read()
        text=html.decode()        
        index=text.find("Upcoming Shows")
        
        text=text[index:]
        
        #regex for people with support
        
        regex='''right..(.+)..span.[\t\n\s]+.....[\t\s\n]+.+[\t\s\n]+.+[\t\n\s]+.+name..(.+)..h1.[\t\s\n]+.+event-subname..(.+)..h4'''
        five29_1=findall(regex,text,re.MULTILINE)

        #regex for people without support
        
        regex2='''right..(.+)..span.[\t\n\s]+.....[\t\n\s]+.+[\t\s\n]+.+[\n\t\s]+.+h1 class.+name..(.+)..h1'''
        five29_2=findall(regex2,text,re.MULTILINE)

        five29list=[]
        datelist=[]

        for each in five29_1:
            line=each[0]+' 9:00 pm '+each[1]+' '+each[2]+'\n'
            five29list.append(line)
            datelist.append(each[0])

        for each in five29_2:
            if each[0] not in datelist:
                line=each[0]+' 9:00 pm '+each[1]+'\n'
                five29list.append(line)
        
    
        for each in five29list:
            self.myfile.write('\t'+ each)
        print('\n')
        
    def earl(self):
        self.myfile.write("The Earl"+'\n'+'\n')
        
        #scrape earl site
        
        response= urllib.request.urlopen('http://www.badearl.com/schedule')
        html=response.read()
        text=html.decode()

        #print earllist

        regex='schedule.show.date..(.+)..doors at.(.+)..div.[\s\t\n]+.+[\s\t\n]+.+[\n\t\s]+.+[\s\t\n]+.+[\t\s\n]+.+events.........+".(.+)..a'
        earllist=findall(regex,text,re.MULTILINE)

        for each in earllist:
            line=each[0]+' '+each[1]+' '+each[2]+'\n'
            self.myfile.write('\t'+line)
        print('\n')
        
    def variety(self):
        self.myfile.write("Variety Playhouse"+'\n')
        #scrape variety site
        
        response= urllib.request.urlopen('http://www.variety-playhouse.com/calendar')
        html=response.read()
        text=html.decode()

        print(text);
        
        #regex for site, gets some of the shows/whatever's on the coming soon part
    
        varreg='''<span class="date">...[\s\n\t](.....)<.span>...([^\t]+)'''
        varietyshowsraw=findall(varreg,text,re.MULTILINE)

        #get current year, add to variety shows
        
        now=datetime.datetime.now()
        year='/'+ str(now.year)
        
        for each in varietyshowsraw:
            ok=str(each[0]+year+' 09:00 pm '+' '+each[1]+'\n')
            print(ok)
            self.myfile.write('\t'+ok)
        print('\n')

shows()      


