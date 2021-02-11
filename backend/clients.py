# Hanchai Nonprasart

import os

class authentation:
	def __init__(self):
		self.__data={os.getenv("ADMIN_USR"):{'pwd':os.getenv("ADMIN_PWD"),'role':{'admin':-1,'user':-1}}} # assume we use this for now, we have to develop to better datablas system later
	def signup(self,usr,pwd):
		if usr in self.__data:
			return False
		self.__data[usr]={'pwd':pwd,'role':{'user':-1}}
		return True
	def login(self,usr,pwd):
		return (usr,pwd,self.__data[usr]['role']) if (usr in self.__data and self.__data[usr]['pwd']==pwd) else None
	def role(self,usr):
		return tuple(self.__data[usr]['role'].keys())
	def join(self,usr,pwd,role,iden):
		if not self.login(usr,pwd) or role in self.__data[usr]['role']:
			return False
		self.__data[usr]['role'][role]=iden
		return True
	def leave(self,usr,pwd,role):
		if not self.login(usr,pwd) or role not in self.__data[usr]['role']:
			return False
		del self.__data[usr]['role'][role]
		return True
	def delete(self,user,usr,pwd):
		if self.login(usr,pwd) and (user==usr or 'admin' in self.role(usr)):
			del self.__data[usr]
			return True
		return False
	def update(self,usr,pwd,usr_,pwd_):
		self.__data[usr_]['pwd']=pwd
		self.__data[usr]=self.__data[usr_].copy()
		self.delete(usr_,usr_,pwd_)
	def view(self,usr,pwd):
		if self.login(usr,pwd) and any(role in self.role(usr) for role in ['admin']):
			return self.__data
		raise(Exception('No access'))
	def setdata(self,usr,data):
		if usr in self.__data:
			self.__data[usr]['data'].update(data)
	def getdata(self,user,data,usr,pwd):
		if self.login(usr,pwd) and (user==usr or 'admin' in self.role(usr)):
			return self.__data[user]['data'][data]
		raise(Exception('No access'))