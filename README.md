# modly
microservices as a microservice

# description
Modly enables the hosting of simple microservices... as a service.  Despite the
circularity, the concept is reasonable: modly hosts python wsgi apps dynamically
from GitHub, providing a whitelist and configuration mechanism to access each
microservice at either the current master, or via an additional `refName` URL
prefix, any tag or branch available.

# local use
Modly really isn't intended or useful for local use.  Since the fundamental
unit that modly consumes is a wsgi app which can be run quite easily using the
development server for any given web framework, there's no need to run locally.
The only consideration is that the deployment URL will be prefixed relative to
the URLs you use in a development environment.  Furthermore, in the case of
flask/werkzeug, the debugger no longer works.  I could probably fix this,
but really for any sort of development or debugging it's better to deal with the
app on its own.

# how _does_ it work then?
Using either the wsgi or development server approach, run the server.  Modly
expects `GH_USER` and `GH_REPO` environment variables to define a location to
look for either a `whitelist.json` or a `config.json`.  In the case of finding
a whitelist, modly will then look in each GitHub repo specified for a
`config.json`.  Modly will serve a flat hierarchy of apps at each specified
prefix, either from the single specified `config.json` or aggregated amongst
many discovered via the whitelist.

# modly is not a monolithic or omnipotent tool
Modly is intended to host a number of small flask apps for data models and
manipulation.  You can put it behind a reverse proxy such as nginx to point
each microservice to a specific domain/subdomain/URL-rewrite, or use it for
back-end services at the inherent URL structure.  If you're developing a
UX-oriented or large site, this is almost certainly not the tool.  The nature
of the dev-mode imposes certain limitations on imports (essentially your app
needs to be in one python file, and import only things on modly's pythonpath).
Modly's `opt_requirements.txt` includes a number of packages recommended for
the environment, to be available for apps to import (such as `requests` and
`pytz`).  You should also very seriously consider placing modly behind an
http cache of some sort if possible.

# modly is very young
This is a specific tool for a specific purpose: enabling the quick development
and deployment of data manipulation microservices.  Although it will never
provide a huge range of features, there are more planned.  More import
flexibility and an intelligent cache for GitHub content to protect against
your site going down when GitHub is down.  Also it'd be great to have more
flexibility in projects, such as multiple configs-per-repo by way of
sub-directories.
