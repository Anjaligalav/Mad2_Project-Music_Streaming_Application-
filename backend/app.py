from flask_jwt_extended import JWTManager,jwt_required,create_access_token,get_jwt_identity,unset_jwt_cookies
# from models import db,ma,bcrypt,User,user_shema
import urllib.parse
from models import*
from flask import Flask,request,Response,jsonify,send_file,send_from_directory,url_for
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from datetime import datetime
from tools.workers import celery, ContextTask
from tools.task import test
from flask_mail import Mail
from flask_caching import Cache



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mad2database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = "Anjali"
app.config["upload_folder"] = "upload"
app.config["MAIL_SERVER"] = 'localhost'
app.config["MAIL_PORT"] = 1025
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'


mail = Mail(app)
cache = Cache(app)
jwt = JWTManager(app)

db.init_app(app)
ma.init_app(app)
bcrypt.init_app(app)

CORS(app,origins='http://localhost:8080',supports_credentials=True)
CORS(app,origins='http://localhost:8081',supports_credentials=True)

with app.app_context():
    db.create_all()

celery = celery

celery.conf.update(
    broker_url = "redis://localhost:6379/1",
    result_backend ="redis://localhost:6379/2"
)

celery.Task = ContextTask

app.app_context().push()

@app.route('/',methods = ['GET'])
def home():
    test.delay(to='managerorcreator@gmail.com')
    # add.delay()
    return "Hello World!"

#----------------------SIGN_UP------------------------------------------------------------------

@app.route('/sign_up',methods =['POST'])
def Sign_up():
    data = request.get_json()
    name = data.get('username')
    email = data.get('email')
    password = data.get('password')

    

    if not name or not email or not password :
        return jsonify({'error' : 'required fields are not Empty'}),409

    existing_email = User.query.filter_by(email = email).first()
    if existing_email:
        return jsonify({'error' : 'Email is alredy signup'}),409
    
    new_user = User(username=name,
                    email=email,
                    password=password,
                    )
    try:
        db.session.add(new_user)
        db.session.commit()
        user = User.query.filter_by(email = email).first()
        access_token = create_access_token(identity={
            'id': user.id
        })
        return jsonify({'message' : 'Registration successfull','access_token':access_token}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error' : f'Some error occured{str(e)}'}),409

#---------------------------------LOGIN------------------------------------------------------  
# @jwt_required
@app.route('/login',methods =["POST"])
def Login():
    data = request.get_json()
    password = data.get('password')
    email = data.get('email')

    user = User.query.filter_by(email = email).first()

    if not user or not bcrypt.check_password_hash(user.password, password) :
        return jsonify({'error' : 'Invalid Credentials'}),401
    
    access_token = create_access_token(identity={
        'id': user.id
    })

    user.last_visit_time = datetime.now()
    db.session.commit()
    #2024-03-10 07:42:19.022172

    return jsonify({'message':"Login Successful",
        'access_token':access_token
    }),200

#--------------------------------------------LOG_OUT---------------------------------------------
@app.route('/logout',methods=["POST"])
@jwt_required()
def Logout():
    response = jsonify({"message":"Logout Successful"})
    unset_jwt_cookies = unset_jwt_cookies(response)
    return response,200

#--------------------ADMIN_INFO--------------------------------------------------------------
def AdminInfo():
    users = User.query.filter(User.role == 'User').all()
    creators = User.query.filter(User.role == 'creator').all()
    genres = db.session.query(Album.genre).distinct().all()
    
    song = Songs.query.all()
    album = Album.query.all()
    l  = []
    al = []
    u  = []
    c  = []

    for gana in song:
        l.append(gana)
    for a in album:
        al.append(a)
    for user in users:
        u.append(user)
    for creator in creators:
        c.append(creator)

    total_songs = len(l)
    total_album=len(al)
    total_users = len(u)
    total_creator = len(c)
    total_genre = len(genres)
    return (total_album,total_songs,total_users,total_creator,song,total_genre,genres)


#----------------------------------------FETCH_ADMIN_INFO------------------------------------
@app.route('/fetchAdminInfo',methods=["GET"])
@jwt_required()
def Admini_Info():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    if user.role!="admin":
        return jsonify({"error":"Not authorize"}),401
    values = AdminInfo()

    distinct_genres = db.session.query(Album.genre).distinct().all()
    genres_list = [genre.genre for genre in distinct_genres]
    avg_list = []
    for genre in genres_list:
        avg = 0
        songs = db.session.query(Songs).join(Album).filter(Album.genre == genre).all()
        for song in songs:
            avg+=song.rating
        avg=avg/len(songs)
        avg =round(avg,1)
        avg_list.append(avg)

    

    result = {"total_song" : values[1],"total_album" :values[0],
                "total_user" : values[2],"total_creator": values[3],
                    "total_genre":values[5],"avg_list":avg_list,"genres_list":genres_list}
    return jsonify({'data': result}), 200
    

#-------------------------------------FETCH_USER_INFO-------------------------------------
@app.route('/fetchuserinfo',methods=["GET"])
@jwt_required()
def Fetchuserinfo():
    this_user = get_jwt_identity()#this have a id of that user which logedIn
    user = User.query.get(this_user['id'])
    
    if not user:
        return jsonify({"message":"User not found"}),404

    user_data = user_shema.dump(user)
    return jsonify(user_data),200


#------------------------------------------CREATOR_REGISTER-----------------------------------
@app.route('/C_register',methods=["PUT"])
@jwt_required()
def C_Register():
    current_user = get_jwt_identity()
    
    user = User.query.filter_by(id=current_user['id']).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.role = 'creator'
    db.session.commit()
    return jsonify({'message': 'Registration successful'}), 200

#----------------------------------------UPLOAD_SONG------------------------------------------

@app.route('/upload',methods=["POST"])
@jwt_required()
def UploadSong():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()

    s_name = request.form.get("sname")
    lyrics= request.form.get("lyrics")
    date_str = request.form.get("date")
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    rating =0
    song_MP3 = request.files.get('songmp3')
    album_name = request.form.get("album_name")
    artist = request.form.get("artist")
    genre = request.form.get("genre")
    

    exist_album = Album.query.filter_by(a_name = album_name).first()
    exist_song=Songs.query.filter_by(s_name=s_name).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404
    elif exist_song:
        return jsonify({'error':"This song is Already exist"}),409
    
    try:
        mp3_filename = secure_filename(song_MP3.filename)
        mp3_path=os.path.join(app.config["upload_folder"],mp3_filename)
        print(mp3_path)
        os.makedirs(app.config["upload_folder"], exist_ok=True)
        song_MP3.save(mp3_path)
        
        
        if exist_album:
            toAdd = Songs(
                s_name= s_name,
                lyrics=lyrics,
                date=date,
                rating=rating,
                songMP3=mp3_filename,
                album_id=exist_album.a_id,
                user=user.id
            )   
            db.session.add(toAdd)
            db.session.commit() 
            return jsonify({'message': 'your song is uploaded successfuly'}), 200
        else:
            toadd = Album(a_name = album_name,artist = artist,genre = genre,user = user.id)
            db.session.add(toadd)
            db.session.commit()
            new_a_id = Album.query.filter_by(a_name = album_name).first()
            toAdd = Songs(
                s_name= s_name,
                lyrics=lyrics,
                date=date,
                rating=rating,
                songMP3=mp3_filename,
                album_id=new_a_id.a_id,
                user=user.id
            )   
            db.session.add(toAdd)
            db.session.commit()
            return jsonify({'message': 'your song is uploaded successfuly'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error' : f'Some error occured{str(e)}'}),409
    

#----------------------------------------------SONG_EDIT----------------------------------------
@app.route('/C_edit/<int:id>',methods=["POST"])
@jwt_required()
def C_Edit(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    song = Songs.query.filter_by(s_id=id).first()
    a = Album.query.filter_by(a_id = song.album_id).first()

    song.s_name = request.form.get("sname")
    song.lyrics= request.form.get("lyrics")
    date_str = request.form.get("date")
    song.date = datetime.strptime(date_str, '%Y-%m-%d').date()
    song.rating =0
    song_MP3 = request.files.get('songmp3')
    a.album_name = request.form.get("album_name")
    a.artist = request.form.get("artist")
    a.genre = request.form.get("genre")

    mp3_filename = secure_filename(song_MP3.filename)
    mp3_path=os.path.join(app.config["upload_folder"],mp3_filename)
    print(mp3_path)
    os.makedirs(app.config["upload_folder"], exist_ok=True)
    song_MP3.save(mp3_path)
    song.song_MP3 = song_MP3

    if not user:
        return jsonify({'error': 'User not found'}), 404

    try:
        db.session.commit()
        return jsonify({'message': 'your song is Edit successfuly'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error' : f'Some error occured{str(e)}'}),409

#-------------------------------------SONG_DELETE---------------------------------------------

@app.route('/C_delete/<int:id>',methods=['DELETE'])
@jwt_required()
def C_Delete(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    song = Songs.query.get(id)
    a_id = song.album_id

    playlists_with_song = Playlist.query.filter(Playlist.song_ids.contains(str(id))).all()

    if not user:
        return jsonify({'error': 'User not found'}),404
    if song:
        db.session.delete(song)

        songs =Songs.query.filter(Songs.album_id==a_id).all()
        if not songs:
            album = Album.query.filter_by(a_id =a_id).first()
            db.session.delete(album)

        for playlist in playlists_with_song:
            song_ids = playlist.song_ids.split(',')  # Split the string to a list
            song_ids = [int(id) for id in song_ids if int(id) != id]  # Remove the deleted song ID
            playlist.song_ids = ','.join(map(str, song_ids))  # Update the song IDs in the playlist
            db.session.add(playlist)
        db.session.commit()
        return jsonify({'message': 'your song is deleted successfuly'}), 200
    else:
        db.session.rollback()
        return jsonify({'error' : "Song is not available"}),404

#-------------------------------------------ALBUM_DELETE_BY_CREATOR------------------------------
    
@app.route('/C_A_delete/<int:id>',methods=['DELETE'])
@jwt_required()
def C_A_Delete(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    album = Album.query.filter_by(a_id =id).first()
    song =Songs.query.filter(Songs.album_id==id).all()

    if not user:
        return jsonify({'error': 'User not found'}),404
    
    if album:
        if song:
            for s in song:
                playlists_with_song = Playlist.query.filter(Playlist.song_ids.contains(str(s.s_id))).all()
                
                for playlist in playlists_with_song:
                    song_ids = playlist.song_ids.split(',')  # Split the string to a list
                    song_ids = [int(id) for id in song_ids if int(id) != s.s_id]  # Remove the deleted song ID
                    playlist.song_ids = ','.join(map(str, song_ids))  # Update the song IDs in the playlist
                    db.session.add(playlist)
                db.session.delete(s)
        db.session.delete(album)
        db.session.commit()
        return jsonify({'message': 'your album is deleted successfuly'}), 200
    else:
        db.session.rollback()
        return jsonify({'error' : "Song is not available"}),404
    
    
#----------------------------------------SONG_DELETE_BY_ADMIN-------------------------------
@app.route("/admin_delete/<int:id>",methods=["DELETE"])
@jwt_required()
def Admin_Delete(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    if user.role!="admin":
        return jsonify({"error":"Not authorize"}),401
    song = Songs.query.get(id)
    a_id = song.album_id

    playlists_with_song = Playlist.query.filter(Playlist.song_ids.contains(str(id))).all()

    if song:
        db.session.delete(song)
        #here i am checking that this is the only song that was remain in my album then also delete album
        #otherwise just delete song not whole album
        songs =Songs.query.filter(Songs.album_id==a_id).all()
        if not songs:
            album = Album.query.filter_by(a_id =a_id).first()
            db.session.delete(album)

        for playlist in playlists_with_song:
            song_ids = playlist.song_ids.split(',')  # Split the string to a list
            song_ids = [int(id) for id in song_ids if int(id) != id]  # Remove the deleted song ID
            playlist.song_ids = ','.join(map(str, song_ids))  # Update the song IDs in the playlist
            db.session.add(playlist)
        db.session.commit()
        return jsonify({'message': 'your song is deleted successfuly'}), 200
    else:
        db.session.rollback()
        return jsonify({'error' : "Song is not available"}),404

#---------------------------------------FETCH_ALL_SONGS---------------------------------------------
@app.route('/all_songs',methods=["GET"])
def AllSongs():
    all_songs = Songs.query.all()
    result = song_schemas.dump(all_songs)
    return jsonify({'data': result}), 200

#----------------------------------------------FETCH_LYRICS------------------------------------------

@app.route("/fetch_lyrics/<int:s_id>")
def FetchLyrics(s_id):
    song = Songs.query.filter_by(s_id=s_id).first()
    print(song.album_id)
    album= Album.query.filter_by(a_id=song.album_id).first()
    print(album)
    song_data = song_schema.dump(song)
    album_data = album_schema.dump(album)
    song_path = f"http://localhost:5000/mp3/{s_id}"
    result = {'song': song_data, 'album': album_data,'path': song_path}
    return jsonify({'data': result}), 200
   
#---------------------Song Play----------------------------------------
@app.route('/mp3/<int:s_id>',methods=["GET"])
def serve_mp3(s_id):
    song = Songs.query.filter_by(s_id=s_id).first()
    filename= os.path.basename(song.songMP3)
    print(filename)
    return send_from_directory(app.config["upload_folder"],filename)
    


#--------------------------------FETCH_SONG_BY_CREATOR--------------------------------------------
@app.route('/fetch_song_by_creator/<int:id>')
def Fetch_Song_by_creator(id):
    s = Songs.query.filter(Songs.user == id).all()
    a = Album.query.filter(Album.user == id).all()

    song_data=song_schemas.dump(s)
    album_data = album_schemas.dump(a)

    l=[]
    m = []
    avg = 0
    for gana in s:
        avg+=gana.rating
        l.append(gana)
    for album in a:
        m.append(album)

    avg=avg/len(l)
    avg =round(avg,2)
    total_songs = len(l)
    total_album=len(m)

    result = {'song': song_data, 'album': album_data, 'avg':avg, 'total_songs': total_songs, 'total_album':total_album}
    return jsonify({'data': result}), 200

#-------------------------------------ALL_ABOUT_PLAYLIST----------------------------------------------

@app.route("/create_playlist",methods=["POST"])
@jwt_required()
def CreatePlayList():
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()

    data = request.get_json()
    p_name = data.get("p_name")
    song_list = data.get("song_list")

    if not user:
        return jsonify({'error': 'User not found'}),404

    song_ids = ','.join(map(str, song_list))
    #if a playlist already exist
    play_list = Playlist.query.filter_by(name = p_name).first()

    try:
        if play_list:
            if play_list.song_ids:
                play_list.song_ids += f",{song_ids}"
            else:
                play_list.song_ids = song_ids
            db.session.commit()
            
            return jsonify({'message': 'Songs are added in your playlist'}), 200
            
        else:
            p1 = Playlist(username = user.username,name = p_name,song_ids = song_ids)
            db.session.add(p1)
            db.session.commit()
            
            return jsonify({'message': 'Your playlist is created successfuly'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error' : f'Some error occured{str(e)}'}),409
    

@app.route('/delete_playlist/<int:id>',methods=['DELETE'])
@jwt_required()
def DeletePlaylist(id):
    current_user = get_jwt_identity()
    user = User.query.filter_by(id=current_user['id']).first()
    playlist = Playlist.query.filter_by(id=id).first()
    if not user:
        return jsonify({'error': 'User not found'}),404
    if playlist:
        db.session.delete(playlist)
        db.session.commit()
        return jsonify({'message': 'your playlist is deleted successfuly'}), 200
    else:
        db.session.rollback()
        return jsonify({'error' : "playlist is not available"}),404
    
@app.route("/single_playlist/<int:id>")
def SinglePlaylist(id):
    user = User.query.filter_by(id =id).first()
    play = Playlist.query.filter(Playlist.username == user.username).all()
    play_data = play_schemas.dump(play)
    return jsonify({'data':play_data}),200

@app.route("/myPlaylist/<int:id>")
def MyPlayList(id):
    play = Playlist.query.filter_by(id = id).first()
    play_data = play_schema.dump(play)
    song_ids = play.song_ids

    song_list = []
    for i in song_ids:
        if i!= ',':
            s = Songs.query.filter_by(s_id = i).first()
            song_data=song_schema.dump(s)
            song_list.append(song_data)
    return jsonify({'song_list':song_list,'play':play_data}),200


#---------------------------------------RATING--------------------------------------------------

@app.route('/rate_song/<int:song_id>', methods=['POST'])
def rate_song(song_id):
    # Assuming you're using JSON data in the request body
    data = request.json
    rating = data.get('rating')

    # Fetch the song from the database
    song = Songs.query.get(song_id)
    if not song:
        return jsonify({'error': 'Song not found'}), 404

    # Update the song's rating
    song.rating = rating
    db.session.commit()

    return jsonify({'message': 'Song rating updated successfully'}), 200


from sqlalchemy import func

#----------------------------------------SEARCHING--------------------------------------------------
@app.route("/search/<search>")
def Search(search):
    try:
        if search:
            # Decode the search query, remove spaces, and convert to lowercase
            search = urllib.parse.unquote(search).replace(" ", "").lower()
            # Perform a case-insensitive search with partial matching
            filtered_songs = Songs.query.join(Album, Songs.album_id == Album.a_id).filter(
                db.or_(
                    func.lower(func.replace(Songs.s_name, " ", "")).like(f"%{search}%"), 
                    func.lower(func.replace(Album.artist, " ", "")).like(f"%{search}%")  
                )
            ).all()
            if filtered_songs:
                result = song_schemas.dump(filtered_songs)
                return jsonify({'data': result}), 200
            else:
                return jsonify({'message': 'No such song or artist found'}), 404

        else:
            # If no search query is provided, return all songs
            filtered_songs = Songs.query.all()
            result = song_schemas.dump(filtered_songs)
            return jsonify({'data': result}), 200
    except Exception as e:
        # Handle exceptions and return an error response
        return jsonify({'error': str(e)}), 500





    
if __name__ == "__main__":
    app.run(debug=True)

