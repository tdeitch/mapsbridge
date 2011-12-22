require 'rubygems'
require 'mechanize'
require 'sinatra'

configure do
  set :default_encoding, 'utf-8'
end

def get_links(username, password)
  # Create a browser session using mechanize called agent
  agent = Mechanize.new

  # Open the login page, get the user's credentials, and sign-in to their Google account
  page = agent.get("https://www.google.com/accounts/ServiceLogin?service=mobile&passive=true&cd=US&hl=en&continue=http://www.google.com/m&followup=http://www.google.com/m&btmpl=mobile_tier2")
  login_form = page.forms.first
  login_form.Email = username
  login_form.Passwd = password
  page = agent.submit(login_form)

  if not page.search('div[@class="errormsg"]').empty?
    return "</ul>The username or password you entered is incorrect.<ul>"
  end

  # Save each map and its URL
  titles = []
  links = []

  # Get the URL of the users My Profile page, which contains a list of the users maps, and put it in maps_url
  page = agent.get("http://maps.google.com/maps/user")
  msids = ''
  page = agent.page.link_with(:text => 'Maps Profile').click
  page = agent.get(agent.page.uri.to_s + '&ptab=2')
  page.links_with(:text => %r{» }, :href => %r{msid}).each do |title|
    titles << title.text
    links << title.uri.to_s
  end
  for i in (0..titles.length-1)
    msids << '<li><a href="maps:q=http%3A//maps.google.com/maps/ms%3Fhl%3Den%26ie%3DUTF8%26oe%3DUTF8%26msa%3D0%26output%3Dkml%26msid%3D' + %r{msid=(.*)$}.match(links[i])[1] + '">'+titles[i]+'</a></li>'
  end
  return msids
end

get '/' do
  erb :index
end

post '/' do
  username = params[:username]
  password = params[:password]
  erb :maps,
  :locals => {:links => get_links(username, password)}
end