
drop aggregate if exists linear_fit(float);

create or replace function linear_fit_finalfunc(p_state float[]) returns float[] as
$$
    import numpy

    if [i for i in p_state if i is None]:
        return None

    return numpy.polyfit(xrange(len(p_state)), p_state, 1)
$$
language plpythonu immutable;

create aggregate linear_fit(float)
(
    stype = float[],
    initcond = '{}',
    sfunc = array_append,
    finalfunc = linear_fit_finalfunc
);

