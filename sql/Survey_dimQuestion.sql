SELECT DISTINCT
    dsurv.SurveyKey AS SurveyKey
    , kpr.responses_stem AS Question
    , kpr.pulse_name AS Domain
    , NULL AS RSODepartment -- Should this be school culture?
    , dri.ResponseType
    , NULL AS CommonQuestionKey
    , NULL AS Question_Cleaned
FROM custom.kelvin_pulse_responses kpr
LEFT JOIN custom.Survey_dimSurvey dsurv
    ON kpr.pulse_window_end_date = dsurv.WindowEnd
    AND dsurv.Category = 'Pulse'
    AND dsurv.System = 'Kelvin'
LEFT JOIN custom.Survey_dimResponseItem dri
    ON kpr.choice = dri.ResponseOrig
    AND IIF(kpr.responses_is_favorable = 1, 1, 0) = dri.Sentiment
WHERE NOT EXISTS (
    SELECT *
    FROM custom.Survey_dimQuestion dq
    WHERE dq.SurveyKey = dsurv.SurveyKey
        AND dq.Question = kpr.responses_stem
)