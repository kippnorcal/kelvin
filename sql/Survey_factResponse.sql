SELECT
    dr.RespondentKey AS RespondentKey
    , dq.QuestionKey AS QuestionKey
    , kpr.choice AS ResponseOrig
FROM custom.kelvin_pulse_responses kpr
INNER JOIN custom.Survey_dimSurvey dsurv
    ON kpr.pulse_window_end_date = dsurv.WindowEnd
    AND dsurv.Category = 'Pulse'
    AND dsurv.System = 'Kelvin'
    AND kpr.pulse_name = dsurv.Name
INNER JOIN custom.Survey_dimQuestion dq
    ON kpr.responses_stem = dq.Question
    AND dsurv.SurveyKey = dq.SurveyKey
INNER JOIN custom.Survey_dimRespondent dr
    ON kpr.participant_id = dr.RespondentKey COLLATE Latin1_General_CS_AS
    AND dsurv.SurveyKey = dr.SurveyKey
WHERE 1=1
    AND dsurv.WindowEnd > DATEADD(week, -1, GETDATE()) -- only get surveys that ended in the last week, assuming the connector runs weekly.
