with
    final as (
        select
            date,
            start_time,
            home_team,
            home_score,
            visitor_team,
            visitor_score,
            attendance,
            length_of_game,
            arena
        from {{ ref('nba_games_xf') }}
    )
select *
from final