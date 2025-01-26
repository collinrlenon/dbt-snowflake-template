with
    base as (
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
    )
select *
from base