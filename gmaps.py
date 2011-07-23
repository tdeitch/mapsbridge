"""
This is a one-file, command-line-only program designed to generate a link to every map on a user's Google My Maps page for viewing on the iPad.

Inputs:
  'user': the user's Google account username
  'pswd': the user's Google account username

Output:
  Links to each of the user's Google My Maps, formatted for viewing on the iPad, in raw HTML form (e.g. <a href=...).
"""

import re
import mechanize

# Create a browser session using mechanize called br
br = mechanize.Browser()

# Open the login page, get the user's credentials, and sign-in to their Google account
br.open("https://www.google.com/accounts/ServiceLogin?service=mobile&passive=true&cd=US&hl=en&continue=http://www.google.com/m&followup=http://www.google.com/m&btmpl=mobile_tier2")
br.select_form(nr=0)
user = raw_input("Username: ")
pswd = raw_input("Password: ")
br["Email"] = str(user)
br["Passwd"] = str(pswd)
login_response = br.submit()

# Get the URL of the user's My Profile page, which contains a list of the user's maps, and put it in 'maps_url'
br.open("http://maps.google.com/maps/user")
maps_profile = br.follow_link(text="My Profile")
maps_url = maps_profile.geturl() + "&ptab=2"

# Add the URL of each of the user's maps to 'pages'
pages = []
br.open(maps_url)
for link in br.links(url_regex=r"msid",text_regex=r"\xbb"):
    pages.append((link.url,link.text))

# Extract the unique MSID from each URL in 'pages' and put the result into 'msids'
# each item in 'msids' is a tuple of the form (MSID_of_the_map, Title_of_the_map) 
msids = []
# an MSID is a string of alphanumeric characters, followed by a period, followed by more alphanumeric characters
# The links we want all contain "msid=" followed by the msid
msidPattern = re.compile(r'msid=(\w+\.\w+)$')
for page in pages:
    msids.append(((msidPattern.search(page[0]).groups()[0]),page[1][:-2]))

# Print individual page links, formatted as HTML
for msid in msids:
    print("<a href='maps:q=http%3A//maps.google.com/maps/ms%3Fhl%3Den%26ie%3DUTF8%26oe%3DUTF8%26msa%3D0%26output%3Dkml%26msid%3D"+msid[0]+"'>"+msid[1]+"</a>")
