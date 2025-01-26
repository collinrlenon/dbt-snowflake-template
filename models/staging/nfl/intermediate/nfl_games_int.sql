with
    intermediate as (
        select *
        from {{ ref('nfl_games_base') }}
        where true
            and winner_score is not null
            and loser_score is not null
    )
select *
from intermediate