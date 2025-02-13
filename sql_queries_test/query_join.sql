SELECT a.name, b.title 
FROM authors a
JOIN books b
ON a.author_id = b.author_id
