WITH k as (
    select * from kittens
)
SELECT * from  k
    inner join fuzzy.bunnies
