WITH existingResponses AS (
    SELECT fr.*
    FROM custom.Survey_factResponse fr
    INNER JOIN custom.Survey_dimQuestion q
        ON q.QuestionKey = fr.QuestionKey
    INNER JOIN custom.Survey_dimSurvey s
        ON s.SurveyKey = q.SurveyKey
    WHERE s.WindowEnd > DATEADD(month, -1, GETDATE()) -- only compare to last month of surveys due to performance issues
)

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
    AND dsurv.WindowEnd > DATEADD(month, -1, GETDATE()) -- only compare to last month of surveys due to performance issues
INNER JOIN custom.Survey_dimQuestion dq
    ON kpr.responses_stem = dq.Question
    AND dsurv.SurveyKey = dq.SurveyKey
INNER JOIN custom.Survey_dimRespondent dr
    ON kpr.participant_id = dr.RespondentKey COLLATE Latin1_General_CS_AS
    AND dsurv.SurveyKey = dr.SurveyKey
LEFT JOIN existingResponses er
    ON er.RespondentKey COLLATE Latin1_General_CS_AS + STR(er.QuestionKey) = dr.RespondentKey + STR(dq.QuestionKey)
WHERE er.QuestionKey IS NULL