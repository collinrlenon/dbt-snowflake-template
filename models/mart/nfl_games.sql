with
    final as (
        select
            id              as game_id,
            date            as date,
            time            as time,
            season          as season,
            day_of_week     as day_of_week,
            winner_name     as winner_name,
            loser_name      as loser_name,
            winner_location as winner_location,
            loser_location  as loser_location,
            winner_score    as winner_score,
            loser_score     as loser_score
        from {{ ref('nfl_games_xf') }}
    )
select *
from final