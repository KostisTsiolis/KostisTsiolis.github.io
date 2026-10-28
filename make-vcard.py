# Builds contact.vcf (the "Save contact" button) from config.js.
# Re-run after changing your details or photo:  python3 make-vcard.py
import base64, re, subprocess, tempfile, os

cfg = open("config.js").read()
get = lambda key: re.search(rf'{key}:\s*"([^"]*)"', cfg).group(1)
name, title, org, email, linkedin, photo = (get(k) for k in
    ("name", "title", "org", "email", "linkedin", "photo"))
first, _, last = name.rpartition(" ")

# Small thumbnail keeps the file light for phones
with tempfile.TemporaryDirectory() as tmp:
    thumb = os.path.join(tmp, "thumb.jpg")
    subprocess.run(["sips", "-Z", "240", photo, "--out", thumb], check=True, capture_output=True)
    b64 = base64.b64encode(open(thumb, "rb").read()).decode()

def fold(line):  # vCard lines must wrap at 75 chars
    return "\r\n ".join(line[i:i + 74] for i in range(0, len(line), 74))

lines = [
    "BEGIN:VCARD", "VERSION:3.0",
    f"N:{last};{first};;;", f"FN:{name}",
    f"ORG:{org}", f"TITLE:{title}",
    f"EMAIL;TYPE=INTERNET,WORK:{email}",
    f"URL;TYPE=LinkedIn:{linkedin}",
    f"X-SOCIALPROFILE;TYPE=linkedin:{linkedin}",
    f"PHOTO;ENCODING=b;TYPE=JPEG:{b64}",
    "END:VCARD",
]
open("contact.vcf", "w", newline="").write("\r\n".join(fold(l) for l in lines) + "\r\n")
print("wrote contact.vcf")
