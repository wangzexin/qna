import webapp2
import re
import os
import jinja2
import random
import string
import datetime

from google.appengine.api import users
from google.appengine.ext import db

template_dir=os.path.join(os.path.dirname(__file__),'templates')
jinja_env=jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir),
                             autoescape=True)

def getname(st):
   email=st.split('@')[0]
   if len(email.split('.'))==2:
      return email.split('.')[0]+' '+email.split('.')[1]
   else:
      return email

class Answer(db.Model):
   answerer=db.StringProperty()
   content=db.TextProperty()
   aid=db.IntegerProperty()
   created_time=db.DateTimeProperty()

Answers=Answer.all()

class Question(db.Model):
   questioner=db.UserProperty()
   qid=db.IntegerProperty()
   sid=db.StringProperty()
   title=db.StringProperty()
   description=db.TextProperty()
   content=db.TextProperty()
   created_time=db.DateTimeProperty()
   answers=db.ListProperty(int)

Questions=Question.all()

class Person(db.Model):
   name=db.StringProperty()
   achievements=db.IntegerProperty()
   keyword=db.StringProperty()
   questions=db.ListProperty(int)

Persons=Person.all()
Anonymous=Person()

class ZhidaoHandler(webapp2.RequestHandler):
    def write(self,*a,**kw):
        self.response.out.write(*a,**kw)

    def render_str(self,template,**params):
        params['user']=self.user
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template,**kw):
        self.write(self.render_str(template,**kw))

    def read_secure_cookie(self,name):
        cookie_val=self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self,user):
        self.set_secure_cookie('user_id',str(user.key().id()))

    def logout(self):
        self.response.headers.add_header(
            'Set-Cookie',
            'user_id=; Path=/')

    def initialize(self,*a,**kw):
        webapp2.RequestHandler.initialize(self,*a,**kw)
        uid=self.read_secure_cookie('user_id')
        self.user=uid and User.by_id(int(uid))

class Index(ZhidaoHandler):
   def get(self):
      u=users.get_current_user()
      if u:
         query=None
         for s in Persons:
            if s.name==getname(str(u)):
               query=s
               break
         if query==None:
            p=Person()
            p.name=getname(str(u))
            p.keyword=''
            p.achievements=0
            p.questions=[]
            p.put()
         else:
            p=query
         username=p.name
         k=0
         questions=[]
         for q in Questions:
            if '' in q.title:
               questions.append(q)
               k+=1
            if k==8:
               break
         self.render('index.html', username=username, questions=questions)
      else:
         greeting = ("<a href=\"%s\">Please sign in your google account</a>." % users.create_login_url("/"))
         self.response.out.write("<html><body>%s</body></html>" % greeting)

   def post(self):
      keyword=self.request.get('keyword')
      u=users.get_current_user()
      if u:
         for s in Persons:
            if s.name==getname(str(u)):
               p=s
               break
         username=p.name
         p.keyword=keyword
         p.put()
      else:
         username='Anonymous user'
         keyword=''
      k=0
      questions=[]
      for i in Questions:
         if keyword in i.title:
            k+=1
            questions.append(i)
         if k==8:
            break
      self.render('index.html', keyword=keyword, username=username, questions=questions)

class Post(ZhidaoHandler):
   def get(self):
      u=users.get_current_user()
      if u:
         self.render('post.html')
      else:
         greeting = ("<a href=\"%s\">Please sign in your google account</a>." % users.create_login_url("/"))
         self.response.out.write("<html><body>%s</body></html>" % greeting)

   def post(self):
      title=self.request.get('title')
      description=self.request.get('description')
      content=self.request.get('content')
      f=False
      u=users.get_current_user()
      for q in Questions:
         if q.title==title:
            f=True
            break
      if not(u):
         error='Please sign in your google account.'
         self.render('post.html',error=error)
      elif title=='':
         error='Please enter a title for your question.'
         self.render('post.html',error=error)
      elif f:
         error='Please enter an alternate title, this one has been posted already.'
         self.render('post.html',error=error)
      else:
         qid=0
         for s in Questions:
            if qid<s.qid:
               qid=s.qid
         q=Question()
         q.title=title
         q.description=description
         q.content=content
         q.created_time=datetime.datetime.now()
         q.answerer=u
         q.qid=qid+1
         q.sid=str(q.qid)
         q.put()
         if u:
            for p in Persons:
               if p.name==str(u).split('@')[0]:
                  p.questions.append(q.qid)
                  p.put()
                  break
         self.redirect('/')

class Viewquestion(ZhidaoHandler):
   def get(self,sid):
      u=users.get_current_user()
      if u:
         qq=None
         for q in Questions:
            if sid==q.sid:
               qq=q
               break
         if qq:
            title=qq.title
            description=qq.description
            content=qq.content
            answers=[]
            for a in q.answers:
               for aa in Answers:
                  if aa.aid==a:
                     answers.append(aa.content)
                     break
            self.render('view.html', title=title, description=description, content=content, answers=answers)
      else:
         greeting = ("<a href=\"%s\">Please sign in your google account</a>." % users.create_login_url("/"))
         self.response.out.write("<html><body>%s</body></html>" % greeting)

   def post(self,sid):
      u=users.get_current_user()
      acontent=self.request.get('solution')
      time=datetime.datetime.now()
      username=getname(str(u))
      if (acontent!=''):
         aid=0
         for s in Answers:
            if s.aid>aid:
               aid=s.aid
         a=Answer()
         a.content=acontent
         a.created_time=time
         a.answerer=username
         a.aid=aid+1
         for s in Questions:
            if s.sid==sid:
               q=s
               break
         q.answers.append(a.aid)
         q.put()
         a.put()
         self.redirect('/')

class Delete(ZhidaoHandler):
   def get(self):
      u=users.get_current_user()
      if u:
         for p in Persons:
            if p.name==getname(str(u)):
               pp=p
         questions=[]
         for q in Questions:
            if q.qid in pp.questions:
               questions.append(q.title)
         self.render('delete.html', questions=questions)
      else:
         greeting = ("<a href=\"%s\">Please sign in your google account</a>." % users.create_login_url("/"))
         self.response.out.write("<html><body>%s</body></html>" % greeting)

   def post(self):
      choice=self.request.get('choice')
      container=[]
      for q in Questions:
         if q.title in choice:
            container.append(q)
      db.delete(container)
      self.redirect('/')

app=webapp2.WSGIApplication([('/',Index),
                             ('/post',Post),
                             ('/view/(.*)',Viewquestion),
                             ('/delete',Delete)],
                            debug=True)
