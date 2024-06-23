from .workers import celery
from models import *
from datetime import datetime, timedelta
from .mailer import send_email_text,send_email_html
from celery.schedules import crontab
from models import *
from flask import render_template
import base64
import os

@celery.on_after_finalize.connect
def setup_periodic_task(sender, **kwargs):
    # sender.add_periodic_task(30, daily_remainder.s(), name="Every 30 secconds")
    sender.add_periodic_task(crontab(hour=2,minute=14), daily_remainder.s(), name ="Every day at 6PM")
    # sender.add_periodic_task(crontab(hour=10,minute=0), daily_remainder.s(), name="Every day at 10AM")
    sender.add_periodic_task(crontab(hour=2,minute=14,day_of_month=27), monthly_remainder.s(), name="Every month at 00:00")



@celery.task
def test(to):
    send_email_text(to=to,subject='Test', body='Test')
    return "success"



@celery.task
def monthly_remainder():
    creators = User.query.filter(User.role == 'creator').all()
    for creator in creators:
        s = Songs.query.filter(Songs.user == creator.id).all()
        a = Album.query.filter(Album.user == creator.id).all()
        l=[]
        m=[]
        avg = 0
        for gana in s:
            avg+=gana.rating
            l.append(gana)
        for album in a:
            m.append(album)
        
        avg=avg/len(l)
        avg =round(avg,2)

        html_content = render_template('monthly_remainder.html',song = s,album=len(m),rating=avg,username=creator.username)

        send_email_html(to=creator.email, subject='Reminder: monthly_report', html=html_content)
        return "success"



@celery.task
def daily_remainder():
    #evening time
    # previous_evening = datetime.now().replace(hour=18, minute=0, second=0, microsecond=0) - timedelta(days=1)
   
    image_url = "https://lh3.googleusercontent.com/pw/AP1GczOEdYN6N2ILBuy-L1-s_LDnFlMjqCYRv66pLttg5_pB7KmOSgat77Vyl2dUhAZb8aPOqDtYXeOqkK0iR9_CI3CuqqDWNfbyZFLJqhoHrzmARgfmdqJOu7VIgfajCv3ZHWBGY5WLubRHj3fq-3L3ofR7uMOhHpfxC6rnjd2iNFTCWF4m0w8em6a8I-N7Vl7cr19JKNuUDsrjtFcn133UXdZOqooRgu9egOiXWfnvGiZz1J0u4yi0_d6zu7TjUaArGxT04U-QFp1QsdOiXcMh9cpYS7V9mtd-_5gaF8qC5ZgAwEOlmGJjBVRX963SLb6zTKtf5Ns3z6If9S4zh75AhY9tuJYra7wf1PWmLzKBXCCgBp9VOoekMC_v0asi3tTAhdJAQtE_RE7gyKBDcUstb2zb4LYL-CfgEFnhEClC7MrGHemi4xU6CBkN3Bb9dNszR3RNmP_qxhdfY6ANaJ37NllVAqqIyFVxXjUa1cFoXtxyFTvRg_aILPGh3_SPmf4XePjjZC3wl8TyEgtOpjXSrPSsJmlZcAZ3JfdZsqTxhTcHbJAoESxTlkLjSvmE14SUPkkDaP207iIQVEK-xFFQzYy_retXAqKRxGgnIBlgWKeEZcH5cyn8hMevT105X8SXVgRMhC6Wr24Pm--6ZtE3bdsx-K90m6BRxW9ff0o_FmpdJcK3XV0HbOGFZqa7GFtwydlR3Q8d0_5zGf3HidQ6GktzA6joo6sOOozxH_tOJRgTcWMbTcd-YfXBnqh7VzEajPyJQQfNf1fDU43vvR532fGhQnyje0ek2kGvlYUSs1QTnxaB7dyXpKsQznk-AmbTPrIA2wn-W6BaNqAfeLtL5_tkFTtZU4wwlTpmEonAzKmVvSpLeiN7M1ueWtkswAqyxLfqOxTp_6MVYVZHbxZ2MnMh=w890-h890-s-no-gm?authuser=0"
    
    # users_to_remind = User.query.filter(User.last_visit_time < previous_evening,User.role == "User").all()
    html_content = render_template('daily_remainder.html',image_url=image_url)
    # # Send reminders to users who haven't visited
    
    # for user in users_to_remind:
    #     send_email_html(to=user.email, subject='Reminder: Visit Our Website', html=html_content)
  
    # return "Success"

    all_users = User.query.all()
    # Send reminders to all users
    for user in all_users:
        send_email_html(to=user.email, subject='Reminder: Visit Our Website', html=html_content)
    return "Success"