import re
import mechanize

# Sign-in to the Google Account
br = mechanize.Browser()
br.open("https://www.google.com/accounts/ServiceLogin?service=mobile&passive=true&cd=US&hl=en&continue=http://www.google.com/m&followup=http://www.google.com/m&btmpl=mobile_tier2")
br.select_form(nr=0)
user = raw_input("Username: ")
pswd = raw_input("Password: ")
br["Email"] = str(user)
br["Passwd"] = str(pswd)
response1 = br.submit()

# Get Google UID
br.open("http://maps.google.com/maps/user")
response2 = br.follow_link(text="My Profile")
maps_url = response2.geturl() + "&ptab=2"

# Get MSID URLs
pages = []
br.open(maps_url)
for link in br.links(url_regex=r"msid",text_regex=r"\xbb"):
    pages.append((link.url,link.text))

# Extract MSIDs from URLs
msids = []
msidPattern = re.compile(r'msid=(\w+\.\w+)$')
for page in pages:
    msids.append(((msidPattern.search(page[0]).groups()[0]),page[1][:-2]))

# Print Individual Page Links
for msid in msids:
    print("<a href='maps:q=http%3A//maps.google.com/maps/ms%3Fhl%3Den%26ie%3DUTF8%26oe%3DUTF8%26msa%3D0%26output%3Dkml%26msid%3D"+msid[0]+"'>"+msid[1]+"</a>")
