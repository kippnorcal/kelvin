SELECT
    dr.RespondentKey AS RespondentKey
    , dq.QuestionKey AS QuestionKey
    , kpr.choice AS ResponseOrig
FROM custom.kelvin_pulse_responses kpr
INNER JOIN custom.Survey_dimSurvey dsurv
    ON kpr.pulse_window_end_date = dsurv.WindowEnd
    AND dsurv.Category = 'Pulse'
    AND dsurv.System = 'Kelvin'
INNER JOIN custom.Survey_dimQuestion dq
    ON kpr.responses_stem = dq.Question
    AND dsurv.SurveyKey = dq.SurveyKey
INNER JOIN custom.Survey_dimRespondent dr
    ON kpr.participant_id = dr.RespondentKey
WHERE NOT EXISTS (
    SELECT *
    FROM custom.Survey_factResponse fr
    WHERE fr.RespondentKey = dr.RespondentKey
        AND fr.QuestionKey = dq.QuestionKey
)