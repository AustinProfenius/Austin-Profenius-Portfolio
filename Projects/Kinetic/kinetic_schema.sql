USE Kinetic;

CREATE TABLE userprofile (
    user_id 		INTEGER NOT NULL AUTO_INCREMENT,
    user_password   VARCHAR(255) NOT NULL,
    email 			VARCHAR(255) NOT NULL UNIQUE,
    birth_date 		Date NOT NULL,
    full_name    	VARCHAR(255) NOT NULL,
    country   		VARCHAR(255) NOT NULL,
    username		VARCHAR(255) NOT NULL UNIQUE,
    profile_path	VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE friendlist (
	relationship_id INTEGER NOT NULL AUTO_INCREMENT,
	user_request 	INTEGER NOT NULL,
    user_accept 	INTEGER NOT NULL,
    accepted 		BOOLEAN NOT NULL,
    PRIMARY KEY (relationship_id),
    FOREIGN KEY (user_accept) REFERENCES userprofile(user_id),
    FOREIGN KEY (user_request) REFERENCES userprofile(user_id)
);

CREATE TABLE post (
	post_id 		int(11) NOT NULL AUTO_INCREMENT,
    poster_id 		INTEGER(11) NOT NULL,
    post_datetime 	DATETIME NOT NULL,
    post_entry 		VARCHAR(255) NOT NULL,
    poster_full_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (poster_id) REFERENCES userprofile(user_id)
);

CREATE TABLE comments (
	comment_id 		int(11) NOT NULL AUTO_INCREMENT,
    post_id 		INTEGER(11) NOT NULL,
    commenter_id 	INTEGER(11) NOT NULL,
    commenter_name  VARCHAR(255) NOT NULL,	
    comment_entry 	VARCHAR(255) NOT NULL,
    comment_datetime DATETIME NOT NULL,
    PRIMARY KEY (comment_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (commenter_id) REFERENCES userprofile(user_id)
);

CREATE TABLE chat (
	chat_id 		int(11) NOT NULL AUTO_INCREMENT,
    send_id 		INTEGER(11) NOT NULL,
    receive_id 		INTEGER(11) NOT NULL,
    send_name		VARCHAR(255) NOT NULL,
    receive_name	VARCHAR(255) NOT NULL,
    PRIMARY KEY (chat_id),
    FOREIGN KEY (send_id) REFERENCES userprofile(user_id),
    FOREIGN KEY (receive_id) REFERENCES userprofile(user_id)
);

CREATE TABLE message (
	message_id 		int(11) NOT NULL AUTO_INCREMENT,
    chat_id 		INTEGER(11) NOT NULL,
    message_entry 	VARCHAR(255) NOT NULL,
    sent_time 		DATETIME NOT NULL,
    send_id 		INTEGER(11) NOT NULL,
    receive_id 		INTEGER(11) NOT NULL,
    send_name		VARCHAR(255) NOT NULL,
    receive_name	VARCHAR(255) NOT NULL,
    PRIMARY KEY (message_id),
    FOREIGN KEY (chat_id) REFERENCES chat(chat_id),
    FOREIGN KEY (send_id) REFERENCES userprofile(user_id),
    FOREIGN KEY (receive_id) REFERENCES userprofile(user_id)
);

CREATE TABLE postlike(
	postlike_id  	INTEGER NOT NULL AUTO_INCREMENT,
    post_id			INTEGER(11) NOT NULL,
    like_name		VARCHAR(255) NOT NULL,
    liker_id 			INTEGER(11) NOT NULL,
    PRIMARY KEY (postlike_id),
    FOREIGN KEY (post_id) REFERENCES post(post_id),
    FOREIGN KEY (liker_id) REFERENCES userprofile(user_id)
);

CREATE TABLE commentlike(
	commentlike_id  	INTEGER NOT NULL AUTO_INCREMENT,
    comment_id			INTEGER(11) NOT NULL,
    like_name			VARCHAR(255) NOT NULL,
    liker_id 			INTEGER(11) NOT NULL,
    PRIMARY KEY (commentlike_id),
    FOREIGN KEY (comment_id) REFERENCES comments(comment_id),
    FOREIGN KEY (liker_id) REFERENCES userprofile(user_id)
);





