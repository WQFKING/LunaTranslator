from utils.config import globalconfig
import sqlite3
import Levenshtein,re
from utils.argsort import argsort
from traceback import print_exc
class edict():
    def __init__(self):
        self.sql=None
        try:
            self.sql=sqlite3.connect( (globalconfig['edict']['path'] ),check_same_thread=False)
        except:
            pass
    
    def search(self,word):
         
            try:
                x=self.sql.execute(f"select text, entry_id from surface where  text like '%{word}%'")
                exp=x.fetchall()
                dis=9999
                dis=[]
                for w,xx in exp: 
                    d=Levenshtein.distance(w,word)
                    dis.append(d)
                save=[]
                srt=argsort(dis)
                for ii in srt:
                    if exp[ii][1] not in save:
                        save.append(exp[ii][1])
                    if len(save)>=10:
                        break
                saveres=[]
                for _id in save:
                    x=self.sql.execute(f"select word, content from entry where  id ={_id}").fetchone()
                    saveres.append(x[0]+'<br>'+re.sub('/EntL.*/','', x[1][1:]))
                
                return '<hr>'.join(saveres)
            except: 
                return None
         