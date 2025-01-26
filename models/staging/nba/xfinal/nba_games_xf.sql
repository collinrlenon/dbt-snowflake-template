with
    xfinal as (
        select *
        from {{ ref('nba_games_int') }}
    )
select *
from xfinal