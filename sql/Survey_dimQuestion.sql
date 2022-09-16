/*
2022-09-15 NWiener 9/15/22 Hotfix - All pulse questions on Likert-Agreement scale except for one, that is hard coded to set different response type
*/
SELECT DISTINCT
    dsurv.SurveyKey AS SurveyKey
    , kpr.responses_stem AS Question
    , kpr.responses_dimension AS Domain
    , 'School Culture' AS RSODepartment
    , IIF(kpr.responses_question_id=1453, 'Likert-Agreement-Reverse',dri.ResponseType) AS ResponseType
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
WHERE dri.ResponseType NOT LIKE '%reverse%'
AND NOT EXISTS (
        SELECT *
        FROM custom.Survey_dimQuestion dq
        WHERE dq.SurveyKey = dsurv.SurveyKey
            AND dq.Question = kpr.responses_stem
)
