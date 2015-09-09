create or replace view "lectures_busy_months" as
with "busy_months" as (
    select
        "lectures_room"."building" as "building",
        date_trunc('month', "lectures_lecture"."date") as "month",
        count(*) as "count"
    from "lectures_lecture"
    left join "lectures_room" on "lectures_room"."id" = "lectures_lecture"."room_id"
    group by "building", "month"
)
select distinct on ("building")
    "building",
    first_value("month") over "building_window" as "least_busy_month",
    last_value("month") over "building_window" as "most_busy_month"
from
    "busy_months"
window "busy_months" as (
    partition by "building"
    order by "count"
    rows between unbounded preceding and unbounded following
);
