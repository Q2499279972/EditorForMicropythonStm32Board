import sys
class Console:
	def __init__(self):
		pass
	def SetColor(self,f,b):
		s="\033[%(fg)d;%(bg)dm"%{'fg':f,'bg':b}
		sys.stdout.write(s)
	def ClearSetting(self):
		s="\033[0m"
		sys.stdout.write(s)
	def ClearScreen(self):
		s="\033[2J"
		sys.stdout.write(s)
	def ClearToEnd(self):
		s="\033[K"
		sys.stdout.write(s)
	def HideCursor(self):
		s="\033[?25l"
		sys.stdout.write(s)
	def ShowCursor(self):
		s="\033[?25h"
		sys.stdout.write(s)
	def SetCursor(self,x,y):
		x=x+1
		y=y+1
		s="\033[%(x)d;%(y)dH"%{'x':x,'y':y}
		sys.stdout.write(s)
	def Write(self,s):
		sys.stdout.write(s)
	def Read(self):
		return sys.stdin.buffer.read(1).decode()
		#return sys.stdin.read(1)

