-- This model is purposely not optimized to highlight an approach to cleaning source tables

with
    base as (
        -- Specify data types and column names
        select
            date::date              as date,
            start_time              as start_time,
            visitor_team            as visitor_team,
            visitor_score::integer  as visitor_score,
            home_team               as home_team,
            home_score::integer     as home_score,
            attendance::integer     as attendance,
            length_of_game          as length_of_game,
            arena                   as arena
        from {{ ref('seed_nba_games') }}
    ),
    intermediate as (
        -- Include any filters
        select *
        from base
        where true
            and home_score is not null
            and visitor_score is not null
    ),
    final as (
        -- Join models and create calcs
        select *
        from intermediate
    )
select *
from final