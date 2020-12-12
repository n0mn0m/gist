/*
Setup a recursive CTE to iterate over ascii ranges and remove
any characters within given ranges. Remember max recursion depth
is sql server is 100 by default
*/

--Initial increment handler
DECLARE @controlcharacter int = 32,
--Second increment handler
@extendedcharacter int = 256;

;with controlcharacters as (
  --Initialize counter for control characters(00),
  --Place constraint at proper recursion depth (32 for asii purpose).
  SELECT 0 AS cnt, REPLACE(Col,char(00), '') as col
  FROM source
  WHERE condition
  UNION ALL
  --Increment the counter and use replace to remove unwanted ascii
  --characters. Check cntr against declared variable.
  SELECT cntr + 1 as cntr, REPLACE (col,char(cntr), '') as col
  FROM controlcharacters c
  where cntr < @controlcharacter),
  
  extendedcharacters as (
    --Same initialization as above, but using the last row from the
    --first recursive set (controlcharacters) to start.
    SELECT 127 as cntr, REPLACE(col,char(127), '') as col
    FROM controlcharacters
    WHERE cntr = (SELECT MAX(cntr) from controlcharacters)
    UNION ALL
    SELECT cntr + 1, REPLACE(col,char(cntr), '') as col
    FROM extendedcharacters c
    WHERE cntr< @extendedcharacter)
    
SELECT * FROM extendedcharacters where cntr = (SELECT MAX(cntr) from extendedcharacters)
--Override MAXRECURSION 100 so that the second pass can go from 127 to 255
OPTION (MAXRECURSION 128);
