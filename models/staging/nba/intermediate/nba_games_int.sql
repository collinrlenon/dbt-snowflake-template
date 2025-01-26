with
    intermediate as (
        select *
        from {{ ref('nba_games_base') }}
        where true
            and home_score is not null
            and visitor_score is not null
    )
select *
from intermediate