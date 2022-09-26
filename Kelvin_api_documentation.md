### Schema

Use the `/api/v1/pulse_responses` endpoint to access pulse responses. This
endpoint will return an array of Pulse Response objects.

Pulse Response objects

```
[
  {
    "id": "", // Globally unique ID for the pulse response
    "pulse_id": "", // NOTE: internally is our pulse_config_id
    "pulse_name": "", // NOTE: internally is our pulse_config.description
    "pulse_window_id": "", // NOTE: internally is our pulse_id
    "pulse_window_number": "",
    "pulse_window_start_date": "",
    "pulse_window_end_date": "",
    "pulse_respondent_type": "", // students, families or staff
    "email": "", // Respondent's email address
    "state_id": "", // Respondent's state id (provided by Clever)
    "district_id": "", // Respondent's district id (provided by Clever)
    "display_id": "", // Respondent's id we display in Kelvin NOTE: maps to Clever's student_number
    "participant_id": "" // Respondent's id
    "responded_at": "", // Date/time
    "needs_assistance": "", // Whether or not the respondent selected they need assistance
    "needs_assistance_asked": "", // Whether or not the needs assistance question was asked
    "responses": [
      {
        "question_id": "", // Kelvin's internal question ID
        "skipped": "", // Whether or not the respondent skipped the question
        "stem": "", // The question stem e.g., How are you feeling?
        "choices": [
          {
            "choice": "", // The choice text, e.g., "Strongly Agree"
            "sort_order": "", // Zero-based sort order of the choice when presented to the participant
            "number": "", // The choice number, e.g. 5
          }
        ],
        "is_favorable": "", // Whether or not the selected choice was favorable
        "comment": "",
        "comment_share_name": "", // Whether or not the respondent opted to share their name with the comment
      }
    ],
  }
]
```

### Paging

The Kelvin API paginates large responses. To iterate through the results you can pass a `page` parameter. This will get you the next page of _100_ results until you receive no more data.

```
/api/v1/pulse_responses?page=1
/api/v1/pulse_responses?page=2
/api/v1/pulse_responses?page=3
```

### Example

This is a very basic javascript example using recursion to iterate through all
the results. This doesn't have error handling, etc.

```js
const params = new URLSearchParams();
params.set('page', 0);

// Filter to only responses that changed after a specific date
// params.set('after', '2020-07-16');

// Filter to a specific pulse (this is our internal pulse_config_id)
// params.set('pulse_id', 20);

// Filter to a specific pulse window (this is our internal pulse_id)
// params.set('pulse_window_id', 20);


getPulseResponses((pulseResponse) => {
  console.log(pulseResponse);
}, params);

async function getPulseResponses(cb, params) {
  const res = await fetch(
    `https://pulse.kelvin.education/api/v1/pulse_responses?${params}`,
    {
      headers: {
        Authorization: "token {{ YOUR TOKEN HERE}}",
      },
    }
  );

  const pulseResponses = await res.json();
  pulseResponses.forEach(cb);

  if (pulseResponses.length === 0) {
    return;
  }

  params.set('page', parseInt(params.get('page')) + 1);
  getPulseResponses(cb, params);
}
```
