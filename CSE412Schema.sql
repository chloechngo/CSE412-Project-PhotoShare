-- TABLE
USE cse412schema;
CREATE TABLE Users (
    user_id INT(11) NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    birth DATE NOT NULL,
    hometown VARCHAR(255) NOT NULL,
    gender VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE Albums (
    album_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name TEXT,
    owner_id INTEGER,
    date_of_creation TEXT
);


CREATE TABLE Photos (
    photo_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    caption TEXT,
    data TEXT,
    album_id INTEGER NOT NULL,
    FOREIGN KEY (album_id) REFERENCES Albums(album_id)
);

CREATE TABLE Comments (
    comment_id INT PRIMARY KEY,
    texts TEXT,
    owner_id INT,
    photo_id INT,
    dates DATETIME,
    FOREIGN KEY (owner_id) REFERENCES Users(user_id),
    FOREIGN KEY (photo_id) REFERENCES Photos(photo_id)
);

CREATE TABLE Friends (
    user_id INTEGER,
    friend_id INTEGER,
    friendship_date TEXT,
    PRIMARY KEY (user_id, friend_id),
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (friend_id) REFERENCES Users(user_id)
);

CREATE TABLE Likes (
    like_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    user_id INTEGER NOT NULL,
    photo_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (photo_id) REFERENCES Photos(photo_id)
);



CREATE TABLE Tags (
    tag_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    tag TEXT,
    photo_id INTEGER NOT NULL,
    FOREIGN KEY (photo_id) REFERENCES Photos(photo_id)
);


-- INDEX
 
-- TRIGGER
 
-- VIEW
 
