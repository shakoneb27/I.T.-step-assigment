import re
 
text = "team members are : shakoneb27@itstep.ge, friend sabaananidze@gmail.com and one more text word test_user@yahoo.com"
 
pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
 
emails = re.findall(pattern, text)
 
result = "+".join(emails)
 
print(result)
