import re
text = "team members are : shakoneb27@itstep.ge, friend sabaananidze@gmail.com and one more text word test_user@yahoo.com"
# emailis amogeba siis mixedvit 
pattern = r"[a-zA-z0-9._%+-]+@[a_zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emils = re.findall(pattern, text)
print("emails")
#siis gadakceva ert stringat
result = "+".join("emails")
print(result)
emails = re.findall(r"\S+@\S+\.\w+", text)
import re

text = "contact me : ana@example.com or info@company.ge"

emails = re.findall(r'[\w.+-]+@[\w-]+(?:\.[\w-]+)+', text)
print(emails)

import re

text = "ouwer tim memebers are : shakoneb27@itstep.com, მეგობარი დიმა sabaananidze@gmail.com and one more text word test_user@yahoo.com"

pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
emails = re.findall(pattern, text)

# siis gadakceva ert stringad "+"
result = "+".join(emails)
print(result)