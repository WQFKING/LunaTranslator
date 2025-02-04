  
import functools 
from PyQt5.QtWidgets import   QWidget, QTableView,  QLabel, QVBoxLayout,QHBoxLayout,QHeaderView

from PyQt5.QtWidgets import  QWidget,QLabel ,QLineEdit,QSpinBox,QPushButton,QTextEdit

from PyQt5.QtGui import QStandardItem, QStandardItemModel
import qtawesome 
from traceback import print_exc
from utils.config import globalconfig ,postprocessconfig,noundictconfig,transerrorfixdictconfig
from PyQt5.QtWidgets import  QWidget,QLabel  
import functools
from PyQt5.QtWidgets import QDialog ,QSpinBox,QVBoxLayout,QLineEdit,QGridLayout
from PyQt5.QtCore import QSize,Qt
from utils.config import globalconfig ,_TR,_TRL
import qtawesome 
 
from gui.inputdialog import getsomepath1
import gui.switchbutton
import gui.attachprocessdialog  
import gui.selecthook  
import os

def setTab7(self) :   
        grids=[
            [('文本预处理',6),'','',('调整执行顺序',6)]
        ] 
        sortlist=globalconfig['postprocess_rank']
        savelist=[]
        savelay=[]
        def _openfile():
            if os.path.exists('./LunaTranslator/postprocess/mypost.py'):
                os.startfile( os.path.abspath('./LunaTranslator/postprocess/mypost.py'))
            elif os.path.exists('./postprocess/mypost.py'):
                os.startfile( os.path.abspath('./postprocess/mypost.py'))
        def changerank( item,up):

            ii=sortlist.index(item)
            if up and ii==0:
                return
            if up==False and ii==len(sortlist)-1:
                return
           
            toexchangei=ii+(-1 if up else 1)
            sortlist[ii],sortlist[toexchangei]=sortlist[toexchangei],sortlist[ii] 
            for i,ww in enumerate(savelist[ii+1]):

                w1=(savelay[0].indexOf(ww))
                w2=savelay[0].indexOf(savelist[toexchangei+1][i])
                p1=savelay[0].getItemPosition(w1)
                p2=savelay[0].getItemPosition(w2) 
                savelay[0].removeWidget(ww)
                savelay[0].removeWidget(savelist[toexchangei+1][i])
                 
                savelay[0].addWidget(savelist[toexchangei+1][i],*p1)
                savelay[0].addWidget(ww,*p2)
            savelist[ii+1],savelist[toexchangei+1]=savelist[toexchangei+1],savelist[ii+1] 
        for i,post in enumerate(sortlist): 
            if post=='_11':
                config=(self.getcolorbutton(globalconfig,'',callback= _openfile,icon='fa.gear',constcolor="#FF69B4")) 
            else:
                if 'args' in postprocessconfig[post]:
                    
                    config=(self.getcolorbutton(globalconfig,'',callback= functools.partial( postconfigdialog,self,postprocessconfig[post]['args'],postprocessconfig[post]['name']+'设置'),icon='fa.gear',constcolor="#FF69B4")) 
                else:
                    config=('')
             
            button_up=(self.getcolorbutton(globalconfig,'',callback= functools.partial(changerank, post,True),icon='fa.arrow-up',constcolor="#FF69B4"))
            button_down=(self.getcolorbutton(globalconfig,'',callback= functools.partial(changerank, post,False),icon='fa.arrow-down',constcolor="#FF69B4")) 
             
            l=[((postprocessconfig[post]['name'] ),6),
                self.getsimpleswitch(postprocessconfig[post],'use'),
                config,
                button_up,
                button_down
            ]
            grids.append(l)
         

        grids.append([''])
        def __(x):
            globalconfig['gongxiangcishu'].__setitem__('use',x)
            self.object.loadvnrshareddict()
        grids+=[
            [('翻译优化',6)],
            [(('使用专有名词翻译' ),6),
                self.getsimpleswitch(noundictconfig,'use'),
                self.getcolorbutton(globalconfig,'',callback=lambda x:  noundictconfigdialog(self,noundictconfig,'专有名词翻译设置(游戏ID 0表示全局)'),icon='fa.gear',constcolor="#FF69B4")],
            [(('使用翻译结果修正' ),6),
                self.getsimpleswitch(transerrorfixdictconfig,'use'),
                self.getcolorbutton(globalconfig,'',callback=lambda x:  noundictconfigdialog1(self,transerrorfixdictconfig,'翻译结果替换设置',['翻译','替换'],'./userconfig/transerrorfixdictconfig.json'),icon='fa.gear',constcolor="#FF69B4")],
            [(('使用VNR共享辞书' ),6),
                self.getsimpleswitch(globalconfig['gongxiangcishu'],'use',callback =lambda x:__(x)),
                self.getcolorbutton(globalconfig,'',callback=lambda x:  getsomepath1(self,'共享辞书',globalconfig['gongxiangcishu'],'path','共享辞书',self.object.loadvnrshareddict,False,'*.xml') ,icon='fa.gear',constcolor="#FF69B4"),'','','','','',''],
            
        ]  
        self.yitiaolong("翻译优化",grids,True,savelist,savelay )
def noundictconfigdialog1(object,configdict,title,label=[  '日文','翻译'],fname='./userconfig/noundictconfig.json'):
    dialog = QDialog(object,Qt.WindowCloseButtonHint)  # 自定义一个dialog
    dialog.setWindowTitle(_TR(title))
    #dialog.setWindowModality(Qt.ApplicationModal)
    
    formLayout = QVBoxLayout(dialog)  # 配置layout
        
    model=QStandardItemModel(len(list(configdict['dict'].keys())),1 , dialog)
    row=0
    for key in  (configdict['dict']):                                   # 2
            
            item = QStandardItem( key )
            model.setItem(row, 0, item)
            item = QStandardItem(configdict['dict'][key] )
            model.setItem(row, 1, item)
            row+=1
    model.setHorizontalHeaderLabels(_TRL(label))
    table = QTableView(dialog)
    table.setModel(model)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
    #table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #table.clicked.connect(self.show_info)
    button=QPushButton(dialog)
    button.setText(_TR('添加行'))
    def clicked1(): 
        model.insertRow(0,[ QStandardItem(''),QStandardItem('')]) 
    button.clicked.connect(clicked1)
    button2=QPushButton(dialog)
    button2.setText(_TR('删除选中行'))
    def clicked2():
        
        model.removeRow(table.currentIndex().row())
    button2.clicked.connect(clicked2)
    button3=QPushButton(dialog)
    button3.setText(_TR('保存并关闭'))
    def clicked3():
        rows=model.rowCount() 
        newdict={}
        for row in range(rows):
            if model.item(row,0).text()=="":
                continue
            newdict[model.item(row,0).text()]=model.item(row,1).text()
        configdict['dict']=newdict
        with open(fname,'w',encoding='utf-8') as ff:
            import json
            ff.write(json.dumps(configdict,ensure_ascii=False,sort_keys=False, indent=6))
        dialog.close()
    button3.clicked.connect(clicked3)
    formLayout.addWidget(table)
    formLayout.addWidget(button)
    formLayout.addWidget(button2)
    formLayout.addWidget(button3)
    dialog.resize(QSize(600,400))
    dialog.show()
def noundictconfigdialog(object,configdict,title,label=['游戏ID MD5' ,'日文','翻译'],fname='./userconfig/noundictconfig.json'):
    dialog = QDialog(object,Qt.WindowCloseButtonHint)  # 自定义一个dialog
    dialog.setWindowTitle(_TR(title))
    #dialog.setWindowModality(Qt.ApplicationModal)
    
    formLayout = QVBoxLayout(dialog)  # 配置layout
        
    model=QStandardItemModel(len(list(configdict['dict'].keys())),1 , dialog)
    row=0
    for key in  (configdict['dict']):                                   # 2
            if type(configdict['dict'][key])==str:
                configdict['dict'][key]=["0",configdict['dict'][key]]
            item = QStandardItem( configdict['dict'][key][0] )
            model.setItem(row, 0, item)
            item = QStandardItem(key  )
            model.setItem(row, 1, item)
            item = QStandardItem( configdict['dict'][key][1] )
            model.setItem(row, 2, item)
            row+=1
    model.setHorizontalHeaderLabels(_TRL(label))
    table = QTableView(dialog)
    table.setModel(model)
    table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
    #table.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #table.clicked.connect(self.show_info)
    button=QPushButton(dialog)
    button.setText(_TR('添加行'))
    def clicked1(): 
        try:
            md5=object.object.textsource.md5
            model.insertRow(0,[QStandardItem(md5),QStandardItem(''),QStandardItem('')]) 
        except:
            print_exc()
            model.insertRow(0,[QStandardItem('0'),QStandardItem(''),QStandardItem('')]) 
    button.clicked.connect(clicked1)
    button2=QPushButton(dialog)
    button2.setText(_TR('删除选中行'))
    def clicked2():
        
        model.removeRow(table.currentIndex().row())
    button2.clicked.connect(clicked2)
    button5=QPushButton(dialog)
    button5.setText(_TR('设置所有词条为全局词条'))
    def clicked5():
        rows=model.rowCount()  
        for row in range(rows):
            model.item(row,0).setText('0')
    button5.clicked.connect(clicked5)
    button3=QPushButton(dialog)
    button3.setText(_TR('保存并关闭'))
    def clicked3():
        rows=model.rowCount() 
        newdict={}
        for row in range(rows):
            if model.item(row,1).text()=="":
                continue
            newdict[model.item(row,1).text()]=[model.item(row,0).text(),model.item(row,2).text()]
        configdict['dict']=newdict
        with open(fname,'w',encoding='utf-8') as ff:
            import json
            ff.write(json.dumps(configdict,ensure_ascii=False,sort_keys=False, indent=6))
        dialog.close()
    button3.clicked.connect(clicked3)
    search=QHBoxLayout()
    searchcontent=QLineEdit()
    search.addWidget(searchcontent)
    button4=QPushButton()
    button4.setText(_TR('搜索'))
    def clicked4():
        text=searchcontent.text()
         
        rows=model.rowCount() 
        cols=model.columnCount()
        for row in range(rows):
            ishide=True
            for c in range(cols):
                if text in model.item(row,c).text(): 
                    ishide=False
                    break 
            table.setRowHidden(row,ishide)

             
    button4.clicked.connect(clicked4)
    search.addWidget(button4)
    
    formLayout.addWidget(table)
    formLayout.addLayout(search)
    formLayout.addWidget(button)
    formLayout.addWidget(button2)
    formLayout.addWidget(button5)
    formLayout.addWidget(button3)
    
    dialog.resize(QSize(600,400))
    dialog.show()
  
def postconfigdialog(object,configdict,title):
    dialog = QDialog(object,Qt.WindowCloseButtonHint)  # 自定义一个dialog
    dialog.setWindowTitle(_TR(title))
    #dialog.setWindowModality(Qt.ApplicationModal)
    
    formLayout = QVBoxLayout(dialog)  # 配置layout
     
    key=list(configdict.keys())[0]
    lb=QLabel(dialog)
    lb.setText(_TR(key) )
    formLayout.addWidget(lb) 
    if type(configdict[key])==type(1): 
        spin=QSpinBox(dialog)
        spin.setMinimum(1)
        spin.setMaximum(100)
        spin.setValue(configdict[key])
        spin.valueChanged.connect(lambda x:configdict.__setitem__(key,x))
        formLayout.addWidget(spin)
        dialog.resize(QSize(600,1))
     
    elif type(configdict[key])==type({}): 
        # lines=QTextEdit(dialog)
        # lines.setPlainText('\n'.join(configdict[key]))
        # lines.textChanged.connect(lambda   :configdict.__setitem__(key,lines.toPlainText().split('\n')))
        # formLayout.addWidget(lines)
        model=QStandardItemModel(len(configdict[key]),1 , dialog)
        row=0
         
        for key1  in  ( (configdict[key])):                                   # 2
             
                item = QStandardItem(key1)
                model.setItem(row, 0, item)
                
                item = QStandardItem(configdict[key][key1])
                model.setItem(row, 1, item)
                row+=1
        model.setHorizontalHeaderLabels(_TRL([ '原文内容','替换为']))
        table = QTableView(dialog)
        table.setModel(model)
        table.setWordWrap(False) 
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        #table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #table.clicked.connect(self.show_info)
        button=QPushButton(dialog)
        button.setText(_TR('添加行'))
        def clicked1(): 
            model.insertRow(0,[QStandardItem(''),QStandardItem('')])   
        button.clicked.connect(clicked1)
        button2=QPushButton(dialog)
        button2.setText(_TR('删除选中行'))
        def clicked2():
            
            model.removeRow(table.currentIndex().row())
        button2.clicked.connect(clicked2)
        button3=QPushButton(dialog)
        button3.setText(_TR('保存并关闭'))
        def clicked3():
            rows=model.rowCount() 
            newdict={}
            for row in range(rows):
                if model.item(row,0).text()=="":
                    continue
                newdict[(model.item(row,0).text())]=(model.item(row,1).text())
            configdict[key]=newdict
            dialog.close()
        button3.clicked.connect(clicked3)
        formLayout.addWidget(table)
        formLayout.addWidget(button)
        formLayout.addWidget(button2)
        formLayout.addWidget(button3)
        dialog.resize(QSize(600,400))
    dialog.show()
 