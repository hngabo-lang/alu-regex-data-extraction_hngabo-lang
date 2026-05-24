import re
import json
import os

input_path  = 'input/raw-text.txt'
output_path = 'output/sample-output.json'

def main():

    # read the file
    try:
        with open(input_path, 'r') as f:
            text = f.read()
    except FileNotFoundError:
        print("Could not find", input_path)
        return

    # matches the real pattern of email having both letters and digits and also @followed by alu domains
    email_pattern    = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
    # matches all real URL links having https
    url_pattern      = r"https?://[^\s]+"
    # matches Rwanda phone numbers starting with +250 or 07
    phone_pattern    = r"(?:\+250|0)7[2389]\d[\s\-]?\d{3}[\s\-]?\d{3}"
    # matches credit cards in groups of 4 digits separated by space or dash
    card_pattern     = r"\d{4}[\s\-]\d{4}[\s\-]\d{4}[\s\-]\d{4}"
    # matches time in both 12hr and 24hr format
    time_pattern     = r"\b(?:1[0-2]|[1-9]|[01][0-9]|2[0-3]):[0-5][0-9](?:\s?(?:AM|PM))?\b"
    # matches all text starting with a #
    hashtag_pattern  = r"#[a-zA-Z]\w+"
    # matches currencies in USD, EUR and RWF
    currency_pattern = r"(?:USD|EUR|RWF|\$)\s?\d+(?:[.,]\d+)*"

    # dangerous HTML tags that should never appear in real submissions
    bad_tags = ["<script>", "<iframe>", "<onerror>", "javascript:"]

    # split file into separate submissions
    blocks = re.split(r"--\s*Submission #\d+[^-]*--", text)[1:]

    # empty lists to collect all results grouped by category
    all_official = []
    all_alumni   = []
    all_si       = []
    all_other    = []
    all_urls     = []
    all_phones   = []
    all_cards    = []
    all_times    = []
    all_hashtags = []
    all_currency = []
    flagged      = []
    results      = []

    for i, block in enumerate(blocks):
        label = "Submission #" + str(i + 1)
        print("Checking:", label)

        # check for dangerous html tags
        is_flagged = any(tag.lower() in block.lower() for tag in bad_tags)

        if is_flagged:
            flagged.append(label)
            print("  Flagged! Contains unsafe text\n")
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

        # add everything to the grouped lists
        all_official.extend(official_emails)
        all_alumni.extend(alumni_emails)
        all_si.extend(si_emails)
        all_other.extend(other_emails)
        all_urls.extend(re.findall(url_pattern,          block))
        all_phones.extend(re.findall(phone_pattern,      block))
        all_cards.extend(masked_cards)
        all_times.extend(re.findall(time_pattern,        block, re.IGNORECASE))
        all_hashtags.extend(re.findall(hashtag_pattern,  block))
        all_currency.extend(re.findall(currency_pattern, block))

        # save this submission to results
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

    # print everything grouped by category
    print("\n========== RESULTS ==========\n")
    print("EMAILS FOUND:")
    print("  Official :", all_official if all_official else "none")
    print("  Alumni   :", all_alumni   if all_alumni   else "none")
    print("  SI       :", all_si       if all_si       else "none")
    print("  Other    :", all_other    if all_other    else "none")
    print("\nURLs FOUND:")
    for url in all_urls: print("  ", url)
    print("\nPHONES FOUND:")
    for phone in all_phones: print("  ", phone)
    print("\nCREDIT CARDS FOUND (masked):")
    for card in all_cards: print("  ", card)
    print("\nTIMES FOUND:")
    print(" ", all_times if all_times else "none")
    print("\nHASHTAGS FOUND:")
    print(" ", all_hashtags if all_hashtags else "none")
    print("\nCURRENCY FOUND:")
    print(" ", all_currency if all_currency else "none")
    print("\nFLAGGED SUBMISSIONS:")
    print(" ", flagged if flagged else "none")
    print("\n=============================")

    # save to json
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=4)

    print("Done! Results saved to", output_path)

if __name__ == "__main__":
    main()
