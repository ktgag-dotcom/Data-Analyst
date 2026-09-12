# Data preparation

Download one fiscal year of federal contract award data from USAspending.gov and save the prepared file here as `contracts.csv`.

Minimum required columns:

```text
recipient_name
awarding_agency
obligated_amount
```

Useful optional fields for extending the project:

```text
awarding_subagency
naics_code
naics_description
award_type
start_date
end_date
recipient_state
```

The analysis intentionally does not commit a large raw government export. Before running the program, confirm that obligated amounts use consistent units and review whether deobligations/negative transactions should be included for your analytical question. The current exercise measures concentration using positive obligations only.
