# alu-regex-data-extraction_hngabo-lang
# ALU Regex Data Extraction

This is a Python script that reads unorded form submissions and pulls out useful information like emails, phone numbers, credit cards, and more. It also detects and skips any submissions that contain dangerous text.

---

## What it does

It reads a text file full of form submissions, goes through each one, and extracts:

- Emails — sorted into ALU official, alumni, and SI
- URLs — any web links
- Phone numbers — Rwanda format only (+250 or 07X)
- Credit cards — found and masked immediately for safety
- Times — both 12hr and 24hr format
- Hashtags — any word starting with #
- Currency — RWF, USD, EUR amounts

If a submission contains dangerous text like `<script>` or `<iframe>` it gets flagged and skipped.

---

## Folder structure

```
alu-regex-data-extraction/
├── input/
│   └── raw-text.txt        ← the form submissions to read
├── src/
│   └── main.py             ← the script that does all the work
├── output/
│   └── sample-output.json  ← results are saved here
└── README.md
```

---

## How to run it

Make sure you are in the project root folder then run:

```bash
python3 src/main.py
```
Attention don't run it in src directory
That is it. Results are saved automatically to `output/sample-output.json`.

---

## What you will see

```
Found 10 submissions

Checking: Submission #1
  Emails: 1 | Cards: 1

Checking: Submission #2
  Emails: 1 | Cards: 1

Checking: Submission #3
  Flagged! Contains unsafe HTML

...

Done! Results saved to output/sample-output.json
```

---

## Security

- Submissions with `<script>`, `<iframe>`, `<onerror>`, or `javascript:` are flagged and skipped
- Credit card numbers are never saved in full — only the last 4 digits are kept like `XXXX-XXXX-XXXX-6467`

---

## Requirements

- Python 3.10 or higher
- No extra libraries needed — uses only `re`, `json`, and `os` which come with Python
