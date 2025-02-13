SELECT a.first_name|| ',' || a.last_name as Author, count(b.title)
FROM authors a
JOIN books b
ON a.author_id = b.author_id
GROUP BY Author
