DELIMITER //
CREATE PROCEDURE GetResponse (
	IN UI Varchar(32),
	IN User_Category Varchar(500),
	IN User_Sentiment DOUBLE,
	IN User_Entity Varchar(500),
	IN User_EntitySentiment DOUBLE,
	OUT Output Varchar(2000)
	)

BEGIN

/*
CREATE TEMPORARY TABLE User_Responses SELECT * FROM Responses WHERE User_Id = UI;
*/


IF (NOT EXISTS(SELECT 1 FROM Responses)) is NULL THEN
	SET Output = 'No Responses Found';

ELSE
	
	SELECT RESPONSE FROM
		(
			(SELECT DISTINCT * FROM Responses 
			WHERE User_Entity = Entity AND User_EntitySentiment >= EntitySentiment AND User_Id = UI
			ORDER BY EntitySentiment ASC LIMIT 1)
			UNION
			(SELECT DISTINCT * FROM Responses
			WHERE User_Entity = Entity AND User_EntitySentiment < EntitySentiment AND User_Id = UI
			ORDER BY EntitySentiment ASC LIMIT 1)
			ORDER by abs(EntitySentiment - User_EntitySentiment) LIMIT 1
		) AS A
	INTO Output;
END IF;

IF Output is NULL THEN
	SELECT RESPONSE FROM
		(
			(SELECT DISTINCT * FROM Responses 
			WHERE User_Category = Category AND User_Sentiment >= Sentiment AND User_Id = UI
			ORDER BY Sentiment ASC LIMIT 1)
			UNION
			(SELECT DISTINCT * FROM Responses 
			WHERE User_Category = Category AND User_Sentiment < Sentiment AND User_Id = UI
			ORDER BY Sentiment ASC LIMIT 1)
			ORDER by abs(Sentiment - User_Sentiment) LIMIT 1
		) AS B
	INTO Output;
END IF;

IF Output is NULL THEN
	SELECT RESPONSE FROM
		(
			(SELECT DISTINCT * FROM Responses 
			WHERE User_Sentiment >= Sentiment AND User_Id = UI
			ORDER BY Sentiment ASC LIMIT 1)
			UNION
			(SELECT DISTINCT * FROM Responses 
			WHERE User_Sentiment < Sentiment AND User_Id = UI
			ORDER BY Sentiment ASC LIMIT 1)
			ORDER by abs(Sentiment - User_Sentiment) LIMIT 1
		) AS C
	INTO Output;
END IF;

IF Output is NULL THEN
	SELECT Response INTO Output FROM Responses
	WHERE User_Id = UI
	ORDER BY RAND() LIMIT 1;
END IF;

END //
DELIMITER ;