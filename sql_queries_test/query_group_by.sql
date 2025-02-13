SELECT a.name, count(b.title)
FROM authors a
JOIN books b
ON a.author_id = b.author_id
GROUP BY a.name
