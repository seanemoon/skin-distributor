SELECT T.id, T.event_id, T.sender, T.subject, T.header, T.body, T.code_types
FROM template AS T JOIN event AS E ON T.event_id = E.id
WHERE E.id = 11
AND E.account_id = 1;
