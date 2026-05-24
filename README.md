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
Checking: Submission #1
Checking: Submission #2
Checking: Submission #3
  Flagged! Contains unsafe HTML

Checking: Submission #4
Checking: Submission #5
  Flagged! Contains unsafe HTML

Checking: Submission #6
Checking: Submission #7
Checking: Submission #8
Checking: Submission #9
Checking: Submission #10

========== RESULTS ==========

EMAILS FOUND:
  Official : ['amara.diallo@alueducation.com', 'eric.nshimiyimana@alueducation.com', 'solange.uwimana@alueducation.com']
  Alumni   : ['kevin.mugisha@alumni.alueducation.com', 'grace.iradukunda@alumni.alueducation.com']
  SI       : ['diane.uwase@si.alueducation.com', 'patrick.habimana@si.alueducation.com']
  Other    : none

URLs FOUND:
   https://amaradiallo.com/portfolio
   https://kevinmugisha.dev
   https://diane-uwase.notion.site
   https://github.com/ericnshimiyimana
   https://graceiradukunda.com/projects
   https://patrickhabimana.io/startup
   https://medium.com/@solange-uwimana

PHONES FOUND:
   0782 345 678
   0729 678 901
   0733 012 345

CREDIT CARDS FOUND (masked):
   XXXX-XXXX-XXXX-6467
   XXXX-XXXX-XXXX-9903
   XXXX-XXXX-XXXX-9776
   XXXX-XXXX-XXXX-6453
   XXXX-XXXX-XXXX-0000
   XXXX-XXXX-XXXX-1234
   XXXX-XXXX-XXXX-7890

TIMES FOUND:
  ['9:00 AM', '10:30 AM', '2:15 PM', '14:00', '3:45 PM', '8:05 AM', '16:30']

HASHTAGS FOUND:
  ['#ALUStudent', '#TechAfrica', '#ALUAlumni', '#Rwanda', '#SocialInnovation', '#ALU', '#OpenSource', '#CodeRwanda', '#WomenInTech', '#ALUAlumni', '#Startup', '#EdTech', '#Rwanda', '#ALUStaff', '#BuildingAfrica']

CURRENCY FOUND:
  ['RWF 50,000', 'USD 200', 'RWF 75,000', 'EUR 150', 'USD 350', 'RWF 120,000', 'USD 500']

FLAGGED SUBMISSIONS:
  ['Submission #3', 'Submission #5']

=============================
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
