import os
from flask import Flask, redirect, render_template, request, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
#from src.repositories.app_repository import db
from src.models import db, userprofile, post, friendlist, comments, chat, message, postlike, commentlike
from sqlalchemy import create_engine , delete
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import time 
import logging

#engine = create_engine("mysql://root:@localhost:3306/Kinetic")
#engine = create_engine("mysql://root:Beans8463@localhost:3306/Kinetic", pool_pre_ping=True)
#engine = create_engine("mysql+mysqlclient://root:Beans8463@localhost:3306/Kinetic", pool_pre_ping=True)
engine = create_engine("mysql+pymysql://root:Beans8463@localhost:3306/Kinetic", pool_pre_ping=True)


app = Flask(__name__)

#app.config['SQLALCHEMY_DATABASE_URI'] = \
#    'mysql://root:Beans8463@localhost:3306/Kinetic' 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Beans8463@localhost:3306/Kinetic'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    app.run()

app.secret_key = os.getenv('APP_SECRET')

@app.route('/', methods=['POST', 'GET'])
def index():

    return render_template('login.html')

@app.route('/about', methods=['POST', 'GET'])
def about():

    return render_template('about.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    
    password = request.form.get('password')
    fullName = request.form.get('FName')
    year = request.form.get('year')
    day = request.form.get('day')
    month = request.form.get('month')
    email = request.form.get('email')
    country = request.form.get('country')
    username = request.form.get('username')


    birthdate = year+"-"+month+"-"+day

    if not password or not fullName or not year or not day or not month or not email:
        abort(400)
    
    if 'profile' not in request.files:
        abort(400)
    
    profile_pic = request.files['profile']

    if profile_pic.filename == '' or profile_pic.filename.rsplit('.',1)[1] not in ['jpg','jpeg','png','gif']:
        abort(400)
    
    filename = f'{username}_{secure_filename(profile_pic.filename)}'
    profile_pic.save(os.path.join('static', 'profile-pics', filename))

    new_user = userprofile(user_password=password, email=email, birth_date=birthdate, full_name=fullName, country=country, username=username, profile_path=filename)
    try:
        db.session.add(new_user)
        db.session.commit()
    except:
        return 'There was a problem creating your account.'


    return redirect('/')

@app.route('/login', methods=['POST', 'GET'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    if not password or not email:
        abort(400)

    existing_user = userprofile.query.filter_by(email=email).first()

    if not existing_user:
        return redirect('/login')
    
    if not existing_user.user_password == password:
        return redirect('/login')
    session['user']  = {
        'email': email, 
        'profile_path': existing_user.profile_path,
        'idNum': existing_user.user_id
    }
    session['id'] = {
        'idNum': existing_user.user_id
    }
    session["full_name"] = {
        "full_name": existing_user.full_name
    }
    session["country"] = {
        "country": existing_user.country
    }
    session["birth"] = {
        "birth": existing_user.birth_date
    }
    session["profile_path"] = {
        "profile_path": existing_user.profile_path
    }
    return redirect('/home')
     
@app.route('/home', methods=['POST', 'GET'])
def home():
    if 'user' not in session:
        abort(401)

    y = session['id']
    x = y["idNum"]

    friendR = friendlist.query.filter_by(user_request=x).all() # list of relations where user_request = current user id
    friendA = friendlist.query.filter_by(user_accept=x).all()  # list of relations where user_accept = current user id
    listOfFriends = []

    if friendR != None:  #where you are the requesting party
        for friend in friendR:
        #logging.warning("See this message in Flask Debug Toolbar!")
            id = friend.user_accept
            user = userprofile.query.filter_by(user_id=id).first()
            listOfFriends.append(user)
    if friendA != None:   #where you are the accepting party
        for friend in friendA:
            id = friend.user_request
            user = userprofile.query.filter_by(user_id=id).first()
            listOfFriends.append(user)
    
    user = userprofile.query.filter_by(user_id=x).first()
    listOfFriends.append(user)
    posts = []
    for user in listOfFriends:
        userposts = post.query.filter_by(poster_id=user.user_id).all()
        for userpost in userposts:
            posts.append(userpost)

                                     #         likes                             likes
    postsandlikes = []    ## [ [post, [like,like,like], likedalready] , [post, [like,like,like], liked already] ]
    posts.sort(key=lambda x: x.post_datetime, reverse=True)
    for userpost in posts: 
        temp = []
        likes = postlike.query.filter_by(post_id=userpost.post_id).all() #likes = []
        tempProfile = userprofile.query.filter_by(user_id=userpost.poster_id).first()
        temp.append(userpost)
        if likes != None:
            alreadyLiked=False
            for like in likes:
                if like.liker_id == x:
                    alreadyLiked = True
                    break
            temp.append(likes)
            temp.append(alreadyLiked)
        temp.append(tempProfile)

        

        postsandlikes.append(temp)
         
    # TODO create query to find all of your/your friends posts
    #posts = 
    return render_template('home.html', posts=posts, postsandlikes=postsandlikes)

@app.route('/post', methods=['POST', 'GET'])
def makepost():
    if 'user' not in session:
        abort(401)
    entry = request.form.get('userpost')

    if not entry:
        abort(400)
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    y = session['id']
    id=y["idNum"] ## current users id
    y = session['full_name']
    x=y["full_name"]
    newPost = post( poster_id=id ,post_datetime=now ,post_entry=entry , poster_full_name = x )   
    try:
        db.session.add(newPost)
        db.session.commit()
    except:
        return 'we encountered an error'
    return redirect('/home')

@app.route('/postprofile', methods=['POST', 'GET'])
def makepostprofile():
    if 'user' not in session:
        abort(401)
    entry = request.form.get('userpost')

    if not entry:
        abort(400)
    now = time.strftime('%Y-%m-%d %H:%M:%S')
    y = session['id']
    id=y["idNum"] ## current users id
    y = session['full_name']
    x=y["full_name"]
    newPost = post( poster_id=id ,post_datetime=now ,post_entry=entry , poster_full_name = x )   
    try:
        db.session.add(newPost)
        db.session.commit()
    except:
        return 'we encountered an error'
    return redirect('/myprofile')

@app.route('/viewpost/<int:post_id>', methods=['POST','GET'])
def viewpost(post_id):
    if 'user' not in session:
        abort(401)
    y = session['id']
    x = y["idNum"]
    my_id = x
    curpost = post.query.filter_by(post_id=post_id).first()     #post to be viewed
    poster = userprofile.query.filter_by(user_id=curpost.poster_id).first()    #person who created post to be viewed
    commentry = comments.query.filter_by(post_id=post_id).all()     # all comments on post to be viewed
    likes = postlike.query.filter_by(post_id=post_id).all()         #all likes on post

    alreadyLikedPost = False
    for like in likes:
        if like.liker_id == x:
            alreadyLikedPost = True

    comsandlikes = []
    for comment in commentry:
        temp = []
        temp.append(comment)
        comlikes = commentlike.query.filter_by(comment_id=comment.comment_id).all()

        if comlikes != None:
            alreadyLikedComment=False

            for like in comlikes:
                if like.liker_id == x:
                    alreadyLikedComment = True
                    break

            temp.append(comlikes)
            temp.append(alreadyLikedComment)

        comsandlikes.append(temp)

    return render_template('post.html', my_id=my_id, curpost=curpost,commentry=commentry, poster=poster, likes=likes, comsandlikes=comsandlikes, alreadyLikedPost=alreadyLikedPost)

@app.route('/likeposthome/<int:post_id>', methods=['POST','GET'])
def likeposthome(post_id):
    y = session['full_name']
    x=y["full_name"]

    id = session['id']
    user_id=id["idNum"]

    newLike = postlike(post_id=post_id, like_name=x, liker_id=user_id)
    try:
        db.session.add(newLike)
        db.session.commit()
    except:
        return 'we encountered an error'

    return redirect('/home')

@app.route('/likepostview/<int:post_id>', methods=['POST','GET'])
def likepostview(post_id):

    y = session['full_name']
    x=y["full_name"]

    id = session['id']
    user_id=id["idNum"]

    newLike = postlike(post_id=post_id, like_name=x , liker_id=user_id)
    try:
        db.session.add(newLike)
        db.session.commit()
    except:
        return 'we encountered an error'

    return redirect(f'/viewpost/{post_id}')

@app.route('/likepostprofile/<int:post_id>', methods=['POST','GET'])
def likepostprofile(post_id):
    y = session['full_name']
    x=y["full_name"]

    id = session['id']
    user_id=id["idNum"]

    newLike = postlike(post_id=post_id, like_name=x, liker_id=user_id)
    try:
        db.session.add(newLike)
        db.session.commit()
    except:
        return 'we encountered an error'
    
    postprofile = post.query.filter_by(post_id=post_id).first()
    profileID = postprofile.poster_id

    return redirect(f'/profile/{profileID}')

@app.route('/comment/<int:post_id>', methods=['POST','GET'])
def comment(post_id):
    y = session['id']
    x=y["idNum"]

    seshname = session['full_name']
    name=seshname["full_name"]

    entry = request.form.get('comment')
    now = time.strftime('%Y-%m-%d %H:%M:%S')

    new_comment = comments(post_id=post_id,commenter_id=x, commenter_name=name, comment_entry=entry, comment_datetime=now)
    try:
        db.session.add(new_comment)
        db.session.commit()
    except:
        return 'we encountered an error'
    
    return redirect(f'/viewpost/{post_id}')

@app.route('/likecomment/<int:comment_id>', methods=['POST','GET'])
def likecomment(comment_id):

    likedComment = comments.query.filter_by(comment_id=comment_id).first()
    thePostWhichHasALikedComment = post.query.filter_by(post_id=likedComment.post_id).first()
    post_id = thePostWhichHasALikedComment.post_id

    y = session['full_name']
    x=y["full_name"]

    id = session['id']
    user_id=id["idNum"]

    newLike = commentlike(comment_id=comment_id, like_name=x , liker_id=user_id)
    try:
        db.session.add(newLike)
        db.session.commit()
    except:
        return 'we encountered an error'

    return redirect(f'/viewpost/{post_id}')

@app.route('/search', methods=['POST','GET'])
def search():
    if 'user' not in session:
        abort(401)
    searchCriteria = request.form.get('searchCriteria')

    if not searchCriteria:
        abort(400)

    results = userprofile.query.filter_by(full_name=searchCriteria)

    return render_template('search.html', results=results)

@app.route('/searchtab', methods=['POST','GET'])
def searchtab():
    if 'user' not in session:
        abort(401)
    return render_template('search.html')

@app.route('/profile/<int:user_id>', methods=['POST','GET'])
def profile(user_id):
    if 'user' not in session:
        abort(401)
    #get list of friends to check if friends before adding friendv
    y = session['id']
    x=y["idNum"]

    friendR = friendlist.query.filter_by(user_request=x).all() # list of relations where user_request = current user id
    friendA = friendlist.query.filter_by(user_accept=x).all()  # list of relations where user_accept = current user id
    listOfFriends = []

    if friendR != None:  #where you are the requesting party
        for friend in friendR:
            #logging.warning("See this message in Flask Debug Toolbar!")
            id = friend.user_accept
            user = userprofile.query.filter_by(user_id=id).first()
            listOfFriends.append(user)
    if friendA != None:   #where you are the accepting party
        for friend in friendA:
            id = friend.user_request
            user = userprofile.query.filter_by(user_id=id).first()
            listOfFriends.append(user)
    numberFriends = len(listOfFriends)
    alreadyFriends = False
    if listOfFriends != None:
        for friend in listOfFriends:
            if friend.user_id == user_id:
                alreadyFriends = True

    posts = post.query.filter_by(poster_id=user_id).all()  # all of the users posts
    postsandlikes = []    ## [ [post, [like,like,like]] , [post, [like,like,like]] ]
    posts.sort(key=lambda x: x.post_datetime, reverse=True)  #sort the posts by date

    for userpost in posts: 
        temp = []
        likes = postlike.query.filter_by(post_id=userpost.post_id).all() #likes = []
        temp.append(userpost)

        if likes != None:
            alreadyLiked=False
            for like in likes:
                if like.liker_id == x:
                    alreadyLiked = True
                    break

            temp.append(likes)
            temp.append(alreadyLiked)
            postsandlikes.append(temp)


    y = session['id']
    id=y["idNum"] ## current users id
    curruser = userprofile.query.filter_by(user_id=id).first()  ## curruser is you
    user = userprofile.query.filter_by(user_id=user_id).first() ## user is the profile you are viewing

    #logic to tell whether or not you already have a chat created with this person
    alreadyHaveChat = False
    currUsersSendChats = chat.query.filter_by(send_id=curruser.user_id).all() #you initiate
    currUsersReceiveChats = chat.query.filter_by(receive_id=curruser.user_id).all() #they initiate
    if len(currUsersSendChats) >= 1:
        for chatt in currUsersSendChats:
            if chatt.receive_id == user.user_id:
                alreadyHaveChat = True
    if len(currUsersReceiveChats) >= 1:
        for chatt in currUsersReceiveChats:
            if chatt.send_id == user.user_id:
                alreadyHaveChat = True

    return render_template('profile.html',user=user, curruser=curruser,alreadyFriends=alreadyFriends,posts=posts, postsandlikes=postsandlikes, numberFriends=numberFriends, alreadyHaveChat=alreadyHaveChat)

@app.route('/myprofile', methods=['POST','GET'])
def myprofile():
    if 'user' not in session:
        abort(401)
    y = session['id']
    id=y["idNum"]
    curruser = userprofile.query.filter_by(user_id=id).first()


    posts = post.query.filter_by(poster_id=id).all()
    postsandlikes = []    ## [ [post, [like,like,like]] , [post, [like,like,like]] ]
    posts.sort(key=lambda x: x.post_datetime, reverse=True)
    for userpost in posts: 
        temp = []
        likes = postlike.query.filter_by(post_id=userpost.post_id).all() #likes = []
        temp.append(userpost)

        if likes != None:
            alreadyLiked=False
            for like in likes:
                if like.liker_id == id:
                    alreadyLiked = True
                    break

            temp.append(likes)
            temp.append(alreadyLiked)
            postsandlikes.append(temp)


    #user = userprofile.query.filter_by(user_id=session['id'])
    return render_template('profile.html',curruser=curruser, user=curruser, sent=False, posts=posts, postsandlikes=postsandlikes)

@app.route('/addfriend/<int:user_id>', methods=['POST'])
def addfriend(user_id):
    if 'user' not in session:
        abort(401)

    y = session['id']
    id=y["idNum"]

    curruser = userprofile.query.filter_by(user_id=id).first()
    user = userprofile.query.filter_by(user_id=user_id).first()

    newRelation=friendlist(user_request=id,user_accept=user_id,accepted=True)
    try:
        db.session.add(newRelation)
        db.session.commit()
    except:
        return 'we encountered an error'

    if newRelation:
        sent = True
        session['requestSent'] = {
        'requestSent': True
    }
    return redirect(f'/profile/{user_id}')
    #return render_template('profile.html',user=user, curruser=curruser,sent=sent)

@app.route('/friends', methods=['POST','GET'])
def friends():
    if 'user' not in session:
        abort(401)

    y = session['id']
    x=y["idNum"]

    friendR = friendlist.query.filter_by(user_request=x).all() # list of relations where user_request = current user id
    friendA = friendlist.query.filter_by(user_accept=x).all()  # list of relations where user_accept = current user id
    listOfFriends = []

    if friendR != None:  #where you are the requesting party
        for friend in friendR:
            id = friend.user_accept
            user = userprofile.query.filter_by(user_id=id).first()
            listOfFriends.append(user)

    if friendA != None:   #where you are the accepting party
        for friend in friendA:
            id = friend.user_request
            user = userprofile.query.filter_by(user_id=id).first()
            listOfFriends.append(user)

    totalFriends = len(listOfFriends)
    #TODO create query to find all friends 
    return render_template('friends.html', listOfFriends=listOfFriends , working=totalFriends)

@app.route('/logout', methods=['POST','GET'])
def logout():
    session["id"] = None
    session["user"] = None
    return redirect("/")

@app.route('/messages/<int:chat_id>', methods=['POST','GET'])
def messages(chat_id):
    if 'user' not in session:
        abort(401)
    
    allMessage = message.query.filter_by(chat_id=chat_id).all()
    currChat = chat.query.filter_by(chat_id=chat_id).first()

    idDic = session['id']
    id=idDic["idNum"]

    nameDic = session['full_name']
    currUserName=nameDic["full_name"]

    if currChat.send_id == id:
        chatWithID = currChat.receive_id
    else:
        chatWithID = currChat.send_id

    chatWithUser = userprofile.query.filter_by(user_id=chatWithID).first()

    #TODO create querys for messages list/send these should maybe be two different methods idk
    return render_template('messages.html' ,allMessage=allMessage, userId=id,currUserName=currUserName, chatWith=chatWithUser.full_name, chatID=currChat.chat_id)

@app.route('/startchat/<int:user_id>', methods=['POST','GET'])
def startchat(user_id):
    
    idDic = session['id']
    id=idDic["idNum"]

    nameDic = session['full_name']
    currUserName=nameDic["full_name"]

    receiver = userprofile.query.filter_by(user_id=user_id).first()

    new_chat = chat(send_id=id, receive_id=user_id, send_name=currUserName, receive_name=receiver.full_name)
    try:
        db.session.add(new_chat)
        db.session.commit()
    except:
        return 'we encountered an error'

    return redirect(f'/messages/{new_chat.chat_id}')

@app.route('/chats', methods=['POST','GET'])
def chats():
    if 'user' not in session:
        abort(401)

    y = session['id']
    id=y["idNum"]

    sChats = chat.query.filter_by(send_id=id).all()
    rChats = chat.query.filter_by(receive_id=id).all()

    schatlist=[]
    for chatt in sChats:
        temp = []
        temp.append(chatt)
        tempProfile = userprofile.query.filter_by(user_id=chatt.receive_id).first()
        temp.append(tempProfile)
        schatlist.append(temp)
    
    rchatlist=[]
    for chatt in rChats:
        temp=[]
        temp.append(chatt)
        tempProfile = userprofile.query.filter_by(user_id=chatt.send_id).first()
        temp.append(tempProfile)
        rchatlist.append(temp)

    #TODO create query to find all of current users chats
    return render_template('chats.html',schatlist=schatlist, rchatlist=rchatlist )

@app.route('/newmessage/<int:chat_id>', methods=['POST','GET'])
def newmessage(chat_id):
    entry = request.form.get('message')
    now = time.strftime('%Y-%m-%d %H:%M:%S')
   
    currChat = chat.query.filter_by(chat_id=chat_id).first()

    idDic = session['id']
    id=idDic["idNum"]

    nameDic = session['full_name']
    currUserName=nameDic["full_name"]
    
    if currChat.send_id == id:
        chatWithID = currChat.receive_id
    else:
        chatWithID = currChat.send_id

    chatWithUser = userprofile.query.filter_by(user_id=chatWithID).first()
    newMessage = message(chat_id=chat_id, message_entry=entry, sent_time=now, send_id=id, receive_id=chatWithUser.user_id, send_name=currUserName, receive_name=chatWithUser.full_name )
    try:
        db.session.add(newMessage)
        db.session.commit()
    except:
        return 'we encountered an error'
    return redirect(f'/messages/{chat_id}')

#####TODO
@app.route('/deletecomment/<int:comment_id>', methods=['POST','GET'])
def deletecomment(comment_id):
    post_id = 0
    return redirect(f'/viewpost/{post_id}') #retreive post_id

@app.route('/deletepost/<int:post_id>')
def deleteposthome(post_id):
    #post_to_delete = post.query.filter_by(post_id=post_id)
    post_to_delete = post.query.get_or_404(post_id)
    
    post.query.filter_by(post_id=post_id).delete()
        #delete(post).where(post.post_id == post_id)
       # db.session.delete(post_to_delete)
        #db.session.commit()
    return redirect('/home') ##redirect to home
    
        #return 'There was a problem deleteing that task'
    return redirect('/home')

@app.route('/editpost/<int:post_id>', methods=['POST','GET'])
def editpost(post_id):

    return redirect(f'/viewpost/{post_id}')

@app.route('/editcomment/<int:comment_id>', methods=['POST','GET'])
def editcomment(comment_id):
    post_id = 0
    return redirect(f'/viewpost/{post_id}') #retrieve post_id

@app.route('/test', methods=['POST','GET'])
def test():

    temp = False
    #comments = comments.query.filter_by(post_id=post_id).all()
    return render_template('temp.html',temp=temp)


#shortcuts
#@app.route('/', methods=['POST','GET'])
#def ():
    #return render_template('.html')

#x = id_num
#y = session['id']
#x = y["idNum"]

#x = email
#y = session['user']
#x = y["email"]

#x = full name
#y = session['full_name']
#x = y["full_name"]

#x = country
#y = session['country']
#x = y["country"]

#x = birthdate
#y = session['birth']
#x = y["birth"]





