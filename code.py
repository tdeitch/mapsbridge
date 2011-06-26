#!/usr/bin/env python

import web
from web import form
import re
import mechanize

render = web.template.render('templates/')

urls = ('/', 'index', '/maps/', 'mymaps')
app = web.application(urls, globals())

myform = form.Form( 
    form.Textbox("username", class_="input", description="Username"), 
    form.Password("password", class_="input", description="Password"),)

class index: 
    def GET(self): 
        f = myform()
        # make sure you create a copy of the form by calling it (line above)
        # Otherwise changes will appear globally
        return render.formtest(f)
    def POST(self): 
        f = myform() 
        if not f.validates(): 
            return render.formtest(f)
        else:
            # form.d.boe and form['boe'].value are equivalent ways of
            # extracting the validated arguments from the form.
            user = f.d.username
            pswd = f.d.password
            # Save username and password using cookies
            setcookie()
            # Sign-in to the Google Account
            br = mechanize.Browser()
            br.open("https://www.google.com/accounts/ServiceLogin?service=mobile&passive=true&cd=US&hl=en&continue=http://www.google.com/m&followup=http://www.google.com/m&btmpl=mobile_tier2")
            br.select_form(nr=0)
            br["Email"] = user
            br["Passwd"] = pswd
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
            links = ""
            for msid in msids:
                links+="<li><a href='maps:q=http%3A//maps.google.com/maps/ms%3Fhl%3Den%26ie%3DUTF8%26oe%3DUTF8%26msa%3D0%26output%3Dkml%26msid%3D"+msid[0]+"'>"+msid[1]+"</a></li>\n"
            return render.maps(links)

if __name__=="__main__":
    web.internalerror = web.debugerror
    app.run()

