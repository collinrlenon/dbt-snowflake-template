with
    xfinal as (
        select *
        from {{ ref('nfl_games_int') }}
    )
select *
from xfinal