import re
import json
import os

input_path  = 'input/raw-text.txt'
output_path = 'output/sample-output.json'

def main():

    # ── read the file ──
    try:
        with open(input_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print("Error: could not find", input_path)
        return

    # ── regex patterns ──
    email_pattern    = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    url_pattern      = r"https?://[^\s]+"
    phone_pattern    = r"(?:\+250|0)7[2389]\d[\s\-]?\d{3}[\s\-]?\d{3}"
    card_pattern     = r"\d{4}[\s\-]\d{4}[\s\-]\d{4}[\s\-]\d{4}"
    time_pattern     = r"\b(?:1[0-2]|[1-9]|[01][0-9]|2[0-3]):[0-5][0-9](?:\s?(?:AM|PM))?\b"
    hashtag_pattern  = r"#[a-zA-Z]\w+"
    currency_pattern = r"(?:USD|EUR|RWF|\$)\s?\d+(?:[.,]\d+)*"

    # ── html tags that are dangerous ──
    bad_tags = ["<script>", "<iframe>", "<onerror>", "javascript:"]

    # ── split file into separate submissions ──
    blocks = re.split(r"--\s*Submission #\d+[^-]*--", text)[1:]
    print("Found", len(blocks), "submissions\n")

    results = []

    for i, block in enumerate(blocks):
        label = "Submission #" + str(i + 1)
        print("Checking:", label)

        # check for dangerous html tags
        flagged = any(tag.lower() in block.lower() for tag in bad_tags)

        if flagged:
            print("  Flagged! Contains unsafe HTML\n")
            results.append({"submission": label, "flagged": True})
            continue

        # find all emails
        all_emails = re.findall(email_pattern, block)

        # sort emails into ALU categories
        official_emails = [e for e in all_emails if "@alueducation.com"        in e and "@alumni" not in e and "@si" not in e]
        alumni_emails   = [e for e in all_emails if "@alumni.alueducation.com" in e]
        si_emails       = [e for e in all_emails if "@si.alueducation.com"     in e]
        other_emails    = [e for e in all_emails if "alueducation.com"         not in e]

        # find and mask credit cards
        raw_cards    = re.findall(card_pattern, block)
        masked_cards = ["XXXX-XXXX-XXXX-" + c.replace(" ", "").replace("-", "")[-4:] for c in raw_cards]

        print("  Emails:", len(all_emails), "| Cards:", len(raw_cards), "\n")

        results.append({
            "submission": label,
            "flagged"   : False,
            "emails": {
                "official": official_emails,
                "alumni"  : alumni_emails,
                "si"      : si_emails,
                "other"   : other_emails,
            },
            "urls"     : re.findall(url_pattern,      block),
            "phones"   : re.findall(phone_pattern,    block),
            "cards"    : masked_cards,
            "times"    : re.findall(time_pattern,     block, re.IGNORECASE),
            "hashtags" : re.findall(hashtag_pattern,  block),
            "currency" : re.findall(currency_pattern, block),
        })

    # ── save to json ──
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

    print("Done! Results saved to", output_path)

if __name__ == "__main__":
    main()
