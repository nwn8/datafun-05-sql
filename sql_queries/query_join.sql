SELECT a.first_name, a.last_name, b.title 
FROM authors a
JOIN books b
ON a.author_id = b.author_id
