CREATE DATABASE movie_booking;
USE movie_booking;

CREATE TABLE movies (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(100),
    genre VARCHAR(50),
    duration INT,
    rating VARCHAR(10),
    language VARCHAR(20)
);

CREATE TABLE showtimes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    movie_id INT,
    hall VARCHAR(20),
    show_time DATETIME,
    price FLOAT,
    FOREIGN KEY (movie_id) REFERENCES movies(id)
);

CREATE TABLE bookings (
    booking_id VARCHAR(20) PRIMARY KEY,
    user_name VARCHAR(100),
    showtime_id INT,
    seats VARCHAR(50),
    total_price FLOAT,
    FOREIGN KEY (showtime_id) REFERENCES showtimes(id)
);

ALTER TABLE seats ADD UNIQUE (showtime_id, seat_number);

SELECT*FROM bookings

CREATE DATABASE IF NOT EXISTS movie_booking;
USE movie_booking;

CREATE TABLE IF NOT EXISTS bookings (
    booking_id VARCHAR(20) PRIMARY KEY,
    user_name VARCHAR(100),
    movie_title VARCHAR(100),
    showtime_id INT,
    seats VARCHAR(50),
    total_price FLOAT
);
