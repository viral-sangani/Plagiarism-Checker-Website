from fuzzywuzzy import fuzz
import threading
from .models import assignment_submitted, Profile
import datetime
import smtplib



def init(userlist, last_assignment, s_user, title):
	now = datetime.datetime.now()
	count = 0
	ratio = 0
	if(len(userlist)==0):
		pass

	else:
		print('last_assignment >> ', last_assignment)
		for i in range(0,len(userlist)-1):
			count += 1
			ratio += fuzz.token_set_ratio(userlist[i].content,last_assignment.content)
		try:
			avg_ratio = ratio//count
		except:
			avg_ratio = 0

		s_class_obj = Profile.objects.filter(user__username=s_user)
		for c_obj in s_class_obj:
			s_class1 = c_obj.s_class
			s_fullname = c_obj.s_fullname
			s_email = c_obj.s_email
			print(s_email)
			print(avg_ratio)

		
		ass_submit_obj = assignment_submitted()
		ass_submit_obj.s_name = s_fullname
		ass_submit_obj.ass_title = title
		ass_submit_obj.submit_date = now.strftime("%Y-%m-%d")
		ass_submit_obj.plag_ratio = avg_ratio
		ass_submit_obj.s_class = s_class1
		ass_submit_obj.save()

		send_email(title,avg_ratio, s_email)


def send_email(title, ratio,s_email):
    server = smtplib.SMTP('smtp.mail.yahoo.com:587')
    server.starttls()
    server.login('studentgateway@yahoo.com','pass@123')
    message = 'Subject: Plagiarism Found in assignment.\n\nAssignment : {}\n\nPlagiarism Ratio is : {}'.format(title, ratio)
    server.sendmail('studentgateway@yahoo.com','viral.sangani2011@gmail.com',message)
    server.quit()
    print("Done")

