LOAD DATA INFILE 'D:/Github/Loyihalar/WEBQ/Savollar.txt'
INTO TABLE savol
FIELDS TERMINATED BY ';' 
LINES TERMINATED BY '\n'
(savol, javob);
mysql --local-infile -u username -p
