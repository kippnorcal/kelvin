SELECT DISTINCT
    participant_id AS RespondentKey
    , dsurv.SurveyKey AS SurveyKey
    , NULL AS Language
    , lks.School_Name AS School
    , pulse_respondent_type AS Audience
    , dstu.Standardized_GradeLevel AS Grade
    , dstu.Standardized_Gender AS Gender
    , dstu.Standardized_PrimaryEthnicity AS Race
    , dstu.Standardized_LunchStatus AS FRL
    , NULL AS LGBT
    , dstu.Standardized_LanguageFluency AS ELL
    , dstu.Standardized_PrimaryDisability AS SPED
    , lks.ID AS lkschools_id
    , display_id AS LocalID
FROM custom.kelvin_pulse_responses kpr
LEFT JOIN custom.Survey_dimSurvey dsurv
    ON kpr.pulse_window_end_date = dsurv.WindowEnd
    AND dsurv.Category = 'Pulse'
    AND dsurv.System = 'Kelvin'
LEFT JOIN dw.DW_dimStudent dstu
    ON CONVERT(VARCHAR,kpr.display_id) = dstu.SystemStudentID
LEFT JOIN custom.lkSchools lks
    ON lks.SchoolKey_SZ = dstu.SchoolKEY_MostRecent
WHERE NOT EXISTS(
    SELECT *
    FROM custom.Survey_dimRespondent dr
    WHERE dsurv.SurveyKey = dr.SurveyKey
)