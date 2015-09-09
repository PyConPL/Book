create temporary table "names"("name" text) on commit drop;

insert into "names" values
('john'),
('mary'),
('barbara'),
('peter'),
('thomas'),
('kevin'),
('betty'),
('april'),
('bob'),
('sean'),
('denise');

truncate table "auth_user" cascade;
insert into "auth_user"("username", "first_name", "last_name", "email", "password", "is_active", "is_staff", "is_superuser", "date_joined")
select "name", "name", '', '', '', true, false, false, now() from "names";


with random_data as (
    select
        "id",
        floor(random() * 4) as grade,
        date_trunc('hour', '2015-01-01'::timestamp + (random()*365 || ' days')::interval) as date
    from auth_user
    left join generate_series(1, 240) on true
)
insert into "grades_grade"("student_id", "date", "grade")
select
    id,
    date,
    grade + 2
from random_data;

