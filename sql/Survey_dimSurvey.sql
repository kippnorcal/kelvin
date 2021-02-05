SELECT DISTINCT
    pulse_name AS Name
    , pulse_respondent_type AS Audience
    , 'Kelvin' AS System
    , custom.fn_SchoolYear4Digit(pulse_window_end_date) AS SchoolYear4Digit
    , pulse_window_start_date AS WindowStart
    , pulse_window_end_date AS WindowEnd
    , 0 AS CurrentlyActive
    , 'Pulse' AS Category
FROM custom.kelvin_pulse_responses kpr
WHERE NOT EXISTS(
    SELECT *
    FROM custom.Survey_dimSurvey dsurv
    WHERE WindowEnd = kpr.pulse_window_end_date
        AND dsurv.System = 'Kelvin'
)