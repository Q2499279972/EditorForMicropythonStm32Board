class Line:
	def __init__(self,str=""):
		self.s = str
		self.n = None
		self.p = None

class LineList(object):
	def __init__(self):
		self.h = None
		self.t = None
	def add(self,a):
		nd = Line(a)
		if(self.h == None):
			self.h = nd;
		if(self.t != None):
			self.t.n = nd;
		nd.p = self.t;
		nd.n = None;
		self.t = nd;
	def insert(self,a,b):
		nd = Line(b)
		if(a.n == None):
			self.add(b);
		else:
			c=a.n;
			nd.p = a;
			nd.n = c;
			a.n = nd;
			c.p = nd;
	def erase(self,a):
		if(a.p == None):
			self.h = a.n;
		elif(a.n == None):
			self.t = a.p;
		else:
			a1 = a.p;
			a2 = a.n;
			a1.n = a2;
			a2.p = a1;
	def isBegin(self,a):
		if(self.h == a):
			return True;
		else:
			return False;
	def isEnd(self,a):
		if(self.t == a):
			return True;
		else:
			return False;

