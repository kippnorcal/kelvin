SELECT DISTINCT
    NULL AS ResponseType -- TODO can we infer response type based on choice?
    , kpr.choice AS ResponseOrig
    , CONVERT(INT,kpr.responses_is_favorable) AS Sentiment
    , kpr.number AS Value
FROM custom.kelvin_pulse_responses kpr
WHERE NOT EXISTS (
    SELECT *
    FROM custom.Survey_dimResponseItem dri
    WHERE kpr.choice = dri.ResponseOrig
)