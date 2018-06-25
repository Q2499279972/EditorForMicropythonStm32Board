from linelist import *
from console import *
class FileIo:
	def __init__(self):
		self.f=None
	def open(self,s,opt):
		self.f=open(s,opt)
	def load(self):
		self.f.seek(0)
		return self.f.readlines()
	def seek(self,n):
		self.f.seek(n)
	def close(self):
		self.f.close()
	def write(self,s):
		self.f.write(s)
	def flush(self):
		self.f.flush()

class Editor:
	def __init__(self):
		self.w=50
		self.h=20
		self.path=None
		self.console = Console()
		self.cursor_x = 0
		self.cursor_y = 0
		self.cursorToStrIndex =0;
		self.curLine = None;
		self.firstDispLine = None
		self.lines = LineList()
		self.isModified=0
		self.enableDebug=0
	def edit(self,s):
		self.console.ClearScreen()
		self.console.ClearSetting()
		self.path=s
		self.lines.h = None
		self.lines.t = None
		file = FileIo()
		file.open(s,"r")
		buf=file.load()
		for i in range(len(buf)):
			self.lines.add(buf[i])
		file.close()
		self.lines.add("")
		self.curLine = self.lines.h;
		self.firstDispLine = self.lines.h;
		self.updateTitle()
		self.updateEdit()
		self.cursor_x = 0
		self.cursor_y = 1
		self.cursorToStrIndex =0;
		self.console.SetCursor(self.cursor_y,self.cursor_x)
		self.isModified=0
		self.loop()
	def doSave(self):
		#RENAME(SAVE AS) NOT SUPPORT
		file = FileIo()
		file.open(self.path,"w")
		file.seek(0)
		it = self.lines.h
		while (it is not None):
			file.write(it.s)
			it = it.n
		file.flush()
		file.close()
		self.isModified=0
		self.updateTitle()
		self.dbgPrint("file saved")
	def updateTitle(self):
		if(self.isModified==0):
			self.updateLine(0,0,self.path)
		else:
			self.updateLine(0,0,self.path+"*")
	def updateEdit(self):
		it = self.firstDispLine
		linenumber=0
		while (it is not None):
			self.updateLine(linenumber+1,0,it.s)
			it = it.n
			linenumber+=1;
			if(linenumber==self.h):
				break
			
	def updateLine(self,y,x,s):
		self.console.SetCursor(y,x)
		self.console.ClearToEnd()
		cursor_pos=x
		str_pos=0
		while(str_pos<len(s) and cursor_pos<self.w):
			c=s[str_pos]
			if(c=='\r'):
				self.console.SetColor(30,47)
				self.console.Write('r');
				self.console.SetColor(37,40)
				str_pos+=1
				cursor_pos+=1
			elif(c=='\n'):
				self.console.SetColor(30,47)
				self.console.Write('n');
				self.console.SetColor(37,40)
				str_pos+=1
				cursor_pos+=1
			elif(c=='\t'):
				n=self.w-cursor_pos
				nn=0
				self.console.SetColor(93,47)
				while(n>0 and nn<4):
					self.console.Write('.')
					cursor_pos+=1
					n-=1
					nn+=1;
				self.console.SetColor(37,40)
				str_pos+=1
			elif(c<'\x20' or c>'\x7e'):
				self.console.SetColor(30,47)
				self.console.Write('?');
				self.console.SetColor(37,40)
				str_pos+=1
				cursor_pos+=1
			else:
				self.console.Write(c);
				str_pos+=1
				cursor_pos+=1
	def dbgPrint(self,s,n=0):
		if(self.enableDebug):
			self.console.SetCursor(self.h+2+n,0)
			self.console.ClearToEnd()
			self.updateLine(self.h+2+n,0,s)
			self.console.SetCursor(self.cursor_y,self.cursor_x)
	def loop(self):
		state=0
		while(True):
			c=self.console.Read()
			if(state==0):
				if(c=='\033'):
					state=1
				elif(c=='\x7f'):
					self.dbgPrint("key Delete")
					self.KeyDelete()
				elif(c=='\x08'):
					self.dbgPrint("key Backspace")
				elif(c=='\x09'):
					self.dbgPrint("key Tab")
					self.KeyTab();
				elif(c=='\x0d'):
					self.dbgPrint("key Enter")
					self.KeyEnter()
				elif(c=='\x03'):
					self.dbgPrint("key Ctrl-C")
				elif(c=='\x13'):
					self.dbgPrint("key Ctrl-S")
					self.KeyCtrlS()
				elif(c=='\x18'):
					self.dbgPrint("key Ctrl-X")
					self.KeyCtrlX()
				elif(c>='\x20' and c<'\x7f'):
					self.KeyNormal(c)
			elif(state==1):
				if(c=='['):
					state=2
				else:
					state=0
			else:
				if(c=='A'):
					self.dbgPrint("key Up")
					self.KeyUp()
				if(c=='B'):
					self.dbgPrint("key Down")
					self.KeyDown()
				if(c=='C'):
					self.dbgPrint("key Right")
					self.KeyRight()
				if(c=='D'):
					self.dbgPrint("key Left")
					self.KeyLeft()
				if(c=='L'):
					self.dbgPrint("key Insert")
				if(c=='H'):
					self.dbgPrint("key Home")
				if(c=='I'):
					self.dbgPrint("key PageUp")
				if(c=='F'):
					self.dbgPrint("key End")
				if(c=='G'):
					self.dbgPrint("key PageDown")
				if(c=='M'):
					self.dbgPrint("key F1")
				if(c=='N'):
					self.dbgPrint("key F2")
				if(c=='O'):
					self.dbgPrint("key F3")
				if(c=='P'):
					self.dbgPrint("key F4")
				if(c=='Q'):
					self.dbgPrint("key F5")
				if(c=='R'):
					self.dbgPrint("key F6")
				if(c=='S'):
					self.dbgPrint("key F7")
				if(c=='T'):
					self.dbgPrint("key F8")
				if(c=='U'):
					self.dbgPrint("key F9")
				if(c=='V'):
					self.dbgPrint("key F10")
				if(c=='W'):
					self.dbgPrint("key F11")
				if(c=='X'):
					self.dbgPrint("key F12")
				state=0
	def KeyNormal(self,c):
		self.curLine.s=self.curLine.s[:self.cursorToStrIndex]+c+self.curLine.s[self.cursorToStrIndex:]
		if(self.isModified==0):
			self.isModified=1
			self.updateTitle()
		self.cursorToStrIndex+=1
		if(self.cursor_x==self.w-1):
			self.cursor_x=1
			self.updateLine(self.cursor_y,0,self.curLine.s[self.cursorToStrIndex-1:])
			self.console.SetCursor(self.cursor_y,self.cursor_x)
		else:
			self.cursor_x+=1
			self.updateLine(self.cursor_y,self.cursor_x-1,self.curLine.s[self.cursorToStrIndex-1:])
			self.console.SetCursor(self.cursor_y,self.cursor_x)
	def KeyTab(self):
		self.curLine.s=self.curLine.s[:self.cursorToStrIndex]+'\t'+self.curLine.s[self.cursorToStrIndex:]
		if(self.isModified==0):
			self.isModified=1
			self.updateTitle()
		self.cursorToStrIndex+=1
		if(self.cursor_x>=self.w-4):
			self.cursor_x=4
			self.updateLine(self.cursor_y,0,self.curLine.s[self.cursorToStrIndex-1:])
			self.console.SetCursor(self.cursor_y,self.cursor_x)
		else:
			self.cursor_x+=4
			self.updateLine(self.cursor_y,self.cursor_x-4,self.curLine.s[self.cursorToStrIndex-1:])
			self.console.SetCursor(self.cursor_y,self.cursor_x)
	def KeyLeft(self):
		if(self.cursorToStrIndex>=2):
			c1=self.curLine.s[self.cursorToStrIndex-1]
			c2=self.curLine.s[self.cursorToStrIndex-2]
			if(c1=='\t'):
				if(self.cursor_x<=4):
					if(c2=='\t'):
						self.cursor_x=4
					else:
						self.cursor_x=1
					self.updateLine(self.cursor_y,0,self.curLine.s[self.cursorToStrIndex-2:])
					self.console.SetCursor(self.cursor_y,self.cursor_x)
				else:
					self.cursor_x-=4
					self.console.SetCursor(self.cursor_y,self.cursor_x)
			else:
				if(self.cursor_x<=1):
					if(c2=='\t'):
						self.cursor_x=4
					else:
						self.cursor_x=1
					self.updateLine(self.cursor_y,0,self.curLine.s[self.cursorToStrIndex-2:])
					self.console.SetCursor(self.cursor_y,self.cursor_x)
				else:
					self.cursor_x-=1
					self.console.SetCursor(self.cursor_y,self.cursor_x)
			self.cursorToStrIndex-=1
		elif(self.cursorToStrIndex==1):
			self.cursor_x=0
			self.updateLine(self.cursor_y,0,self.curLine.s)
			self.console.SetCursor(self.cursor_y,self.cursor_x)
			self.cursorToStrIndex-=1
	def KeyRight(self):
		if(len(self.curLine.s)==0):
			return
		if(self.cursorToStrIndex<len(self.curLine.s)):
			c=self.curLine.s[self.cursorToStrIndex]
		else:
			return
		if(c=='\n'):# or c=='\r'): #NOTE!!
			return
		elif(c=='\t'):
			if(self.cursor_x+4>self.w-1):
				self.cursor_x = 4
				self.cursorToStrIndex+=1
				self.updateLine(self.cursor_y,0,self.curLine.s[self.cursorToStrIndex-1:])
				self.console.SetCursor(self.cursor_y,self.cursor_x)
			else:
				self.cursor_x+=4
				self.cursorToStrIndex+=1
				self.console.SetCursor(self.cursor_y,self.cursor_x)
		else:
			if(self.cursor_x+1>self.w-1):
				self.cursor_x = 1
				self.cursorToStrIndex+=1
				self.updateLine(self.cursor_y,0,self.curLine.s[self.cursorToStrIndex-1:])
				self.console.SetCursor(self.cursor_y,self.cursor_x)
			else:
				self.cursor_x+=1
				self.cursorToStrIndex+=1
				self.console.SetCursor(self.cursor_y,self.cursor_x)
	def KeyUp(self):
		if(self.curLine == self.lines.h):
			return
		else:
			if(self.cursor_y<=1):
				self.cursor_x=0
				self.cursorToStrIndex=0
				self.curLine=self.curLine.p
				self.firstDispLine = self.firstDispLine.p
				self.updateEdit()
				self.console.SetCursor(self.cursor_y,self.cursor_x)
			else:
				self.updateLine(self.cursor_y,0,self.curLine.s)
				self.cursor_y-=1
				self.cursor_x=0
				self.cursorToStrIndex=0
				self.curLine=self.curLine.p
				self.console.SetCursor(self.cursor_y,self.cursor_x)
	def KeyDown(self):
		if(self.curLine == self.lines.t):
			return
		else:
			if(self.cursor_y>=self.h):
				self.cursor_x=0
				self.cursorToStrIndex=0
				self.curLine=self.curLine.n
				self.firstDispLine = self.firstDispLine.n
				self.updateEdit()
				self.console.SetCursor(self.cursor_y,self.cursor_x)
			else:
				self.updateLine(self.cursor_y,0,self.curLine.s)
				self.cursor_y+=1
				self.cursor_x=0
				self.cursorToStrIndex=0
				self.curLine=self.curLine.n
				self.console.SetCursor(self.cursor_y,self.cursor_x)
	def KeyDelete(self):
		if(self.cursorToStrIndex<len(self.curLine.s)):
			c=self.curLine.s[self.cursorToStrIndex]
		else:
			return
		if(c!='\n'):
			self.curLine.s=self.curLine.s[:self.cursorToStrIndex]+self.curLine.s[1+self.cursorToStrIndex:]
			if(self.isModified==0):
				self.isModified=1
				self.updateTitle()
			self.updateLine(self.cursor_y,self.cursor_x,self.curLine.s[self.cursorToStrIndex:])
			self.console.SetCursor(self.cursor_y,self.cursor_x)
		else:
			self.curLine.s=self.curLine.s[:-1]
			if(self.isModified==0):
				self.isModified=1
				self.updateTitle()
			if(self.curLine.n!=None):
				self.curLine.s+=self.curLine.n.s
				self.lines.erase(self.curLine.n)
				self.updateLine(self.cursor_y,self.cursor_x,self.curLine.s[self.cursorToStrIndex:])
				it=self.curLine.n;
				y=self.cursor_y+1;
				while ((it is not None) and y<=self.h):
					self.updateLine(y,0,it.s)
					y+=1
					it = it.n
				while(y<=self.h):
					self.updateLine(y,0,"")
					y+=1
				self.console.SetCursor(self.cursor_y,self.cursor_x)
	def KeyEnter(self):
		a=self.curLine.s[:self.cursorToStrIndex]
		b=self.curLine.s[self.cursorToStrIndex:]
		a+='\x0a'#note!!
		self.curLine.s=a
		self.lines.insert(self.curLine,b)
		if(self.isModified==0):
			self.isModified=1
			self.updateTitle()
		if(self.cursor_y>=self.h):
			self.cursor_x=0
			self.cursorToStrIndex=0
			self.curLine=self.curLine.n
			self.firstDispLine = self.firstDispLine.n
			self.updateEdit()
			self.console.SetCursor(self.cursor_y,self.cursor_x)
		else:
			self.cursor_y+=1
			self.cursor_x=0
			self.cursorToStrIndex=0
			self.curLine=self.curLine.n
			self.updateEdit()
			self.console.SetCursor(self.cursor_y,self.cursor_x)
	def KeyCtrlS(self):
		if(self.isModified==1):
			self.doSave();
	def KeyCtrlX(self):
		self.console.ClearSetting()
		self.console.ClearScreen()
		self.console.SetCursor(0,0)
		import sys
		sys.exit(0)
def edit(s):
	editor = Editor()
	editor.edit(s)
def edit_debug(s):
	editor = Editor()
	editor.enableDebug=1
	editor.edit(s)


