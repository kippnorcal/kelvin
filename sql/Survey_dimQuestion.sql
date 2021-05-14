SELECT DISTINCT
    dsurv.SurveyKey AS SurveyKey
    , kpr.responses_stem AS Question
    , kpr.responses_dimension AS Domain
    , 'School Culture' AS RSODepartment
    , dri.ResponseType
    , NULL AS CommonQuestionKey
    , NULL AS Question_Cleaned
FROM custom.kelvin_pulse_responses kpr
LEFT JOIN custom.Survey_dimSurvey dsurv
    ON kpr.pulse_window_end_date = dsurv.WindowEnd
    AND kpr.pulse_name = dsurv.Name
    AND dsurv.Category = 'Pulse'
    AND dsurv.System = 'Kelvin'
LEFT JOIN custom.Survey_dimResponseItem dri
    ON kpr.choice = dri.ResponseOrig
    AND CONVERT(INT,kpr.responses_is_favorable) = dri.Sentiment
WHERE NOT EXISTS (
        SELECT *
        FROM custom.Survey_dimQuestion dq
        WHERE dq.SurveyKey = dsurv.SurveyKey
            AND dq.Question = kpr.responses_stem
)