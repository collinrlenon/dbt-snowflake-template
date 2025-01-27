-- This model is purposely not optimized to highlight an approach to cleaning source tables

with
    base as (
        -- Specify data types and column names
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
    ),
    intermediate as (
        -- Include any filters
        select *
        from base
        where true
            and winner_score is not null
            and loser_score is not null
    ),
    final as (
        -- Join models and create calcs
        select *
        from intermediate
    )
select *
from final