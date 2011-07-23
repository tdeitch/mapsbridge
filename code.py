#!/usr/bin/env python

"""
This is an iPad web app written in web.py to display a user's Google My Maps as links to open in the included Maps program.

Inputs:
  'user': str, the user's Google account username
  'pswd': str, the user's Google account password

Output:
  Upon first loading, displays a screen for the user to input a username and password. Upon validation, the user's My Maps are listed. Clicking one of these maps opens it in the iPad's Maps app.
"""

import web              # web.py
from web import form    # the form rendering and processing code
import re               # regular expression processing
import mechanize        # web scraping

# disable debug mode, just to be safe
web.config.debug = False

# the location of the templates directory, relative to code.py (this file)
render = web.template.render('templates/')

# the web app's directory structure. This can be modified as needed, or left alone and adjusted with mod_rewrite or another similar tool.
urls = ('/', 'index')
app = web.application(urls, globals())

# The form to collect the user's username and password is created here and passed to login.html as a variable.
myform = form.Form( 
    form.Textbox("username", class_="input", description="Username"), 
    form.Password("password", class_="input", description="Password"),)

class index: 
    # the only GET requests should be for the login form. all other requests should be POST requests.
    def GET(self):
        f = myform()
        # create a copy of 'myform' by calling it (as in the line above)
        # otherwise changes to the form will appear globally, since 'myform' was created outside this class
        # pass an instance 'f' of the form 'myform' to be rendered in login.html
        return render.login(f)
    def POST(self): 
        # create another instance of 'myform'. It's safe to override the previous one now (from the GET request).
        f = myform()
        # if the form doesn't validate, give the user another chance
        if not f.validates():
            return render.login(f)
        else:
            # save the username and password to shorter variables for easier typing, because I am lazy
            user = f.d.username
            pswd = f.d.password
            # Open the Google sign-in page and sign-in to the user's Google account using mechanize
            br = mechanize.Browser()
            br.open("https://www.google.com/accounts/ServiceLogin?service=mobile&passive=true&cd=US&hl=en&continue=http://www.google.com/m&followup=http://www.google.com/m&btmpl=mobile_tier2")
            br.select_form(nr=0)
            br["Email"] = user
            br["Passwd"] = pswd
            response1 = br.submit()
            # Get the URL of the user's 'My Profile' page and save it as 'maps_url'
            br.open("http://maps.google.com/maps/user")
            response2 = br.follow_link(text="My Profile")
            maps_url = response2.geturl() + "&ptab=2"
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
            # Save the individual page links, formatted as HTML, to the string 'links'
            links = ""
            for msid in msids:
                links+="<li><a href='maps:q=http%3A//maps.google.com/maps/ms%3Fhl%3Den%26ie%3DUTF8%26oe%3DUTF8%26msa%3D0%26output%3Dkml%26msid%3D"+msid[0]+"'>"+msid[1]+"</a></li>\n"
            # pass the formatted links to the maps.html template
            return render.maps(links)

# don't forget to run the actual app
if __name__=="__main__":
    app.run()

