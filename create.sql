CREATE TABLE hotel(
Hotel_Address TINYTEXT NOT NULL,
Additional_Number_of_Scoring integer NOT NULL,
Hotel_Name TINYTEXT NOT NULL,
CONSTRAINT hotel_pk PRIMARY KEY (Hotel_Address)

);


CREATE TABLE reviews(

review_id number(6) NOT NULL,
Hotel_Address TINYTEXT NOT NULL,
reviewer_id number(6) NOT NULL,
Review_Date date NOT NULL,
Average_Score float NOT NULL,
Negative_Review text,
Positive_Review text,
Total_Number_of_Reviews number(6) NOT NULL,
CONSTRAINT review_pk PRIMARY KEY (review_id)
);

CREATE TABLE reviewer(
reviewer_id number(6) NOT NULL,
Reviewer_Score float NOT NULL,
Reviewer_Nationality TINYTEXT NOT NULL,
CONSTRAINT reviewer_pk PRIMARY KEY (reviewer_id)

);