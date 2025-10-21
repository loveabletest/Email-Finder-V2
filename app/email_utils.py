import re
import random
import smtplib
import dns.resolver
from email_validator import validate_email, EmailNotValidError

# --- Clean domain ---
def clean_domain(domain):
    domain = domain.lower().strip()
    domain = re.sub(r'^https?://', '', domain)
    domain = re.sub(r'^www\.', '', domain)
    return domain

# --- SMTP Mailbox Check ---
def smtp_verify(email):
    try:
        domain = email.split('@')[1]
        mx_records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(mx_records[0].exchange).rstrip('.')

        server = smtplib.SMTP(mx_record, timeout=10)
        server.helo("example.com")
        server.mail("test@example.com")
        code, _ = server.rcpt(email)
        server.quit()

        return code == 250
    except:
        return None

# --- Catch-all Detection ---
def is_catch_all(domain):
    try:
        random_email = f"random{random.randint(10000,99999)}@{domain}"
        result = smtp_verify(random_email)
        return result is True
    except:
        return False

# --- Verification Helper ---
def has_mx(domain):
    try:
        records = dns.resolver.resolve(domain, 'MX')
        return len(records) > 0
    except:
        return False

# --- Email Verification ---
def verify_email(email):
    try:
        validate_email(email)
        domain = email.split("@")[-1]
        if not has_mx(domain):
            return "⚠️ Invalid domain (no MX records)"
        if is_catch_all(domain):
            return "⚠️ Catch-all domain — deliverability uncertain"
        smtp_status = smtp_verify(email)
        if smtp_status is True:
            return "✔️ Deliverable"
        elif smtp_status is False:
            return "❌ Undeliverable"
        else:
            return "⚠️ SMTP check inconclusive"
    except EmailNotValidError:
        return "❌ Invalid syntax"

# --- LinkedIn Query ---
def linkedin_query(first, last, domain):
    return f'"{first} {last}" site:linkedin.com "{domain}"'

# --- Email Generator ---
def generate_emails(first, last, domain):
    first = first.lower().strip()
    last = last.lower().strip()
    domain = clean_domain(domain)
    f = first[0] if first else ''
    l = last[0] if last else ''

    emails = [
        f"{f}{last}@{domain}",
        f"{first}.{last}@{domain}",
        f"{first}@{domain}",
        f"{first}_{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{last}@{domain}",
        f"{last}{f}@{domain}",
        f"{f}.{last}@{domain}",
        f"{first}{l}@{domain}",
        f"{f}{l}@{domain}",
    ]
    emails = list(dict.fromkeys(emails))

    results = [{"Email": e, "Status": verify_email(e)} for e in emails]
    return results
