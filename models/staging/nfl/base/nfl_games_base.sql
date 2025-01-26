with
    base as (
        select
            id                      as id,
            season::integer         as season,
            date::date              as date,
            time                    as time,
            day_of_week             as day_of_week,
            winner_name             as winner_name,
            loser_name              as loser_name,
            winner_location         as winner_location,
            loser_location          as loser_location,
            winner_score::integer   as winner_score,
            loser_score::integer    as loser_score
        from {{ ref('seed_nfl_games') }}
    )
select *
from base