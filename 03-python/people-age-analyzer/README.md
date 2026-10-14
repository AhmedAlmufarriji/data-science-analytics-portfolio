# People Age Analyzer

Validate dates of birth, compute current ages and weekdays, and summarize an arbitrary number of people.

**Stack:** Python standard library

## Behavior

Handles `dd-mm-yyyy` inputs, verifies real calendar dates, rejects impossible/future dates, prints invalid dates with the person's name, reports oldest and youngest, counts entries, sorts by age, reverses submissions and lists Sunday births.

For one valid person, it prints the required 'There is no oldest or youngest person' message.

## How to get started

```bash
python src/people_age_analyzer.py --demo
```

Run without `--demo` for interactive input. The `--demo` flag uses the assignment's historical reference date.
