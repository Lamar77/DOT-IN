from builtins import dict, len, zip
import sqlite3
 
   
  
# conn = sqlite3.connect('SqliteDBnex.db')
# cur = conn.cursor()
  

class SqliteDBnexDatabase :
   

  def  __init__(self):

    self.execute_hash_query('CREATE TABLE IF NOT EXISTS "Birds" ( "Name"	TEXT NOT NULL, "User"	TEXT NOT NULL, "Bio"	TEXT NOT NULL, "Age"	INTEGER NOT NULL, "PasswordHash"	INTEGER NOT NULL, "BirdId"	INTEGER NOT NULL, PRIMARY KEY("BirdId" AUTOINCREMENT));')  
    self.execute_hash_query( 'CREATE TABLE IF NOT EXISTS  "Comment" ( "User" TEXT NOT NULL, "PostId"	INTEGER NOT NULL, "Comments"	TEXT NOT NULL,     PRIMARY KEY("PostId" AUTOINCREMENT));') 
    self.execute_hash_query('CREATE TABLE IF NOT EXISTS "Counts" ( "PostId"	INTEGER NOT NULL, "Likescount"	TEXT NOT NULL, "User"	TEXT NOT NULL,      PRIMARY KEY("PostId" AUTOINCREMENT));') 
    self.execute_hash_query('CREATE TABLE IF NOT EXISTS "Likes" ( "User"	TEXT NOT NULL, "PostId"	INTEGER NOT NULL );') 
    self.execute_hash_query('CREATE TABLE IF NOT EXISTS "Messages" ( "MessageId"	TEXT NOT NULL, "UserId1"	TEXT NOT NULL, 	"UserId2"	TEXT NOT NULL, "Message"	INTEGER NOT NULL, "Date/Time"	TIMESTAMP DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY("MessageId"));') 
    self.execute_hash_query('CREATE TABLE IF NOT EXISTS "Posts" ("PostId"	INTEGER NOT NULL, "Texts"	TEXT NOT NULL, "BirdId" INTEGER NOT NULL, PRIMARY KEY("PostId" AUTOINCREMENT));')
    self.execute_hash_query('CREATE TABLE IF NOT EXISTS "friends" ("ReceiverId"	INTEGER NOT NULL,	"SenderId"	INTEGER NOT NULL);')
    self.execute_hash_query('CREATE TABLE IF NOT EXISTS "request" ( 	"SenderId"	INTEGER NOT NULL, 	"ReceiverId"	INTEGER NOT NULL );')


  def create_user(self,Name,User, Bio,Age, PasswordHash):
    self.execute_hash_query("""INSERT INTO Birds (Name,User,Bio,Age,PasswordHash) VALUES (?, ?, ?, ?, ?)""",Name,User, Bio,Age, PasswordHash)
 # conn.commit() 

        
  def get_user_by_Id(self,BirdId):
    return self.execute_query("SELECT * FROM Birds WHERE BirdId = ?",BirdId) 

  def get_id_by_user(self, user):
    return self.execute_query("SELECT * FROM Birds WHERE Name = ?",user) 

  def get_id_by_users(self, user):
    return self.execute_query("SELECT * FROM Birds WHERE Name = ?",user)
    
   
 

     # if len(results) > 0:      
     # return results[0]
     # else:
     # return None

  def execute_hash_query(self, query_text, *parameters):
      conn = sqlite3.connect('SqliteDBnex.db')
      cur = conn.cursor()
      cur.execute(query_text, parameters)
      conn.commit()


  def execute_query(self, query_text, *parameters):
      conn = sqlite3.connect('SqliteDBnex.db')
      cur = conn.cursor()
      cur.execute(query_text, parameters)

      column_names = []
      for column in cur.description:
       column_names.append(column[0])

      rows = cur.fetchall()
      dicts = []
      for row in rows:
        d = dict(zip(column_names, row))
        dicts.append(d)
        conn.close()
      return dicts

  def get_posts_by_Id(self,user):
        # return self.execute_query("""SELECT * FROM Posts WHERE PostId=?""",user)
    return self.execute_query("SELECT * FROM Posts Inner JOIN Birds ON Posts.BirdId = Birds.BirdId WHERE Birds.BirdId = ?", user)

  def get_all_users(self):
    return self.execute_query("SELECT * FROM Birds")

  def get_all_messages(self):
        return self.execute_query("SELECT * FROM Messages INNER JOIN Birds ON Messages.UserId1 = Birds.BirdId ")

  # def get_all_posts(self,user ): 
  #   return self.execute_query("SELECT * FROM Posts Inner JOIN Birds ON Posts.BirdId = Birds.BirdId WHERE Posts.PostId = ?", user)   
  def get_all_posts(self ): 
    return self.execute_query("SELECT * FROM Posts Inner JOIN Birds ON Posts.BirdId = Birds.BirdId")

  def friend_request(self,receiver_id):
    return self.execute_query("SELECT * FROM Birds INNER JOIN request ON Birds.BirdId = request.SenderId AND request.ReceiverId =?",receiver_id)
  
  def add_friend_request(self,sender_id,receiver_id):
    return self.execute_hash_query("INSERT INTO request (SenderId, ReceiverId) VALUES (?,?)",sender_id,receiver_id)
         

  def cancel_friend_request(self,sender_id,receiver_id):
    return self.execute_hash_query("DELETE FROM request WHERE SenderId=? And ReceiverId=?",sender_id,receiver_id)  
 
  def add_a_friend(self,receiver_id,sender_id):
           print(receiver_id,sender_id)
           self.execute_hash_query("INSERT INTO friends (ReceiverId, SenderId) VALUES (?,?)",receiver_id,sender_id), 
          #  self.execute_hash_query("INSERT INTO friends (UserId, friendId) VALUES (?,?)",user_id,friend_id),  
          #  self.execute_hash_query("DELETE FROM requests WHERE senderID = ? AND receiverID = ?", senderId, receiverId) 
   
  def all_requested_friends(self,user_id):
    result = self.execute_query("SELECT ReceiverId FROM Request WHERE SenderId = ?", user_id)
    return [x['ReceiverId'] for x in result]

  def cancel_a_friend_request(self,sender_id,receiver_id):
    return self.execute_hash_query("DELETE FROM request WHERE SenderId=? And ReceiverId=?",sender_id,receiver_id)  
      
  def accept_friend_request(self):
    return self.execute_query(" SELECT * FROM Birds INNER JOIN friends ON Birds.BirdId = friends.ReceiverId or Birds.BirdId = friends.SenderId") 
    
  def friends_count(self,userid,friend_id):
    return self.execute_query("SELECT COUNT(*) FROM friends WHERE UserId =? AND friendId =? ",userid,friend_id)
  
  def request_count(self,user):
    return self.execute_query("SELECT COUNT(*) FROM request WHERE BirdId =? AND User =? ",user)   

  def get_all_posts_by_Id(self, user):
    return self.execute_query(""" SELECT Posts.Id, 
            Posts.BirdId, 
            Posts.Text, 
            birds.Name, 
            birds.Username, 
            L.LikeCount
        FROM Posts
        INNER JOIN birds
            ON Posts.BirdId = birds.BirdId
        INNER JOIN ( SELECT PostId, COUNT(BirdId) AS LikesCount FROM Likes GROUP BY PostId) L
            ON Posts.PostId = L.PostId """, user)

  def  get_comment_by_Id(self,post_id):
       conn = sqlite3.connect('SqliteDBnex.db')
       cur = conn.cursor()
       self.execute_query("""SELECT * FROM Comment WHERE PostId = ?""",post_id)
       columns = [column[0] for column in cur.description]
       results = []
       for row in cur:
            d = dict(zip(columns,row))
            results.append(d)
       return results

  def insert_post(self, id, post_content):
    self.execute_hash_query("INSERT INTO Posts (Texts, BirdId) VALUES (?, ?)", post_content, id)
    pass

  def insert_into_message(self, id, message_content):
    self.execute_hash_query("INSERT INTO messages (Texts, UserId1) VALUES (?, ?)", message_content,id)

    

  def like_post(self, user, post_id):
    self.execute_hash_query("""INSERT INTO likes (User,PostId) VALUES (?,?)""",user,post_id)
        

 
  def like_count(self, post_id):
    data = self.execute_query("""SELECT COUNT(*) FROM Counts WHERE  PostId=?""",post_id)
    return len(data)

  def already_liked(self,user, post_id):
      res = self.execute_query("""SELECT COUNT(*) FROM likes WHERE  PostId = ? AND User = ?""",post_id,user)
      return len(res) > 0
  

    #  for row in cur:
    #     return (row[0] > 0)      

  def unlike_post(self, user, post_id):
    self.execute_hash_query("""DELETE FROM likes WHERE User=? And PostId=?""",user,post_id)

  def toggle_like(self,user,post_id):
      if self.already_liked(user,post_id):
           action = 'unlike'
           self.unlike_post(user,post_id)
      else:
            action = 'like'
            self.like_post(user,post_id)
      return {
             'like_count' : self.like_count(post_id),
             'action' : action
       } 

  def delete_post(self, post_id, user_id):
    self.execute_hash_query("""DELETE FROM Posts WHERE PostId=? And BirdId=?""", post_id, user_id)
    
  def search_user(self, search_input):
    return self.execute_query("SELECT User FROM Birds WHERE User LIKE ?", "%" + search_input + "%")

    
         