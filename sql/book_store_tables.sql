drop table members, cart, books, orders, odetails;

-- Creating the 'members' table
CREATE TABLE members (
    userid INT AUTO_INCREMENT PRIMARY KEY,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    address VARCHAR(50) NOT NULL,
    city VARCHAR(30) NOT NULL,
    zip INT NOT NULL,
    phone VARCHAR(15) NULL,
    email VARCHAR(40) UNIQUE NOT NULL,
    password VARCHAR(200) NOT NULL
);

-- Creating the 'books' table
CREATE TABLE books (
    isbn CHAR(10) PRIMARY KEY,
    author VARCHAR(100) NOT NULL,
    title VARCHAR(200) NOT NULL,
    price FLOAT NOT NULL,
    _subject VARCHAR(100) NOT NULL
);

-- Creating the 'cart' table
CREATE TABLE cart (
    userid INT,
    isbn CHAR(10),
    qty INT NOT NULL,
    PRIMARY KEY (userid, isbn),
    FOREIGN KEY (userid) REFERENCES members(userid),
    FOREIGN KEY (isbn) REFERENCES books(isbn)
);

-- Creating the 'orders' table
CREATE TABLE orders (
    ono INT AUTO_INCREMENT PRIMARY KEY,
    userid INT NOT NULL,
    created DATE NULL,
    shipAddress VARCHAR(50) NULL,
    shipCity VARCHAR(30) NULL,
    shipZip INT NULL,
    FOREIGN KEY (userid) REFERENCES members(userid)
);

-- Creating the 'odetails' table
CREATE TABLE odetails (
    ono INT,
    isbn CHAR(10),
    qty INT NOT NULL,
    amount FLOAT NOT NULL,
     PRIMARY KEY (ono, isbn),
    FOREIGN KEY (ono) REFERENCES orders(ono),
    FOREIGN KEY (isbn) REFERENCES books(isbn)
);
