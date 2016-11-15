# Development at Hudora

Here we store Information in regard to Software Development at Hudora.

## Tools


* We use [github.com/hudora][github] for version control, tickets and reviews
  ([Introduction][githubintro]) - you should create an account there
* We use [gerrit][gerrithudora] as a review system - you should create an account there

[github]: http://github.com/hudora
[githubintro]: https://cybernetics.hudora.biz/intern/wordpress/2009/12/github-it-is/
[gerrithudora]: http://gerrit.hudora.de/
[sublime]: http://www.sublimetext.com/


##  Coding

 * [Refactor Mercilessly][refactor] - your own code and others.
 * If you touch a file you are responsible that it is in decent shape afterwards. Even if it was messy *before* you touched it.
 * Your commit messages should be in german or english, use markdown and follow general [commit message best practices][commitmessage]. Sample: `[LH #4711] added abbility to print docs for Swiss customs`
 * Check the [timeline/dashboard][timeline] regulary to see what's happening. Skimm the changesets and ask if you don't understand something.
 * always do `make test`, `make check` or equivalent before commit.
 * add the URL of the ticket in the ticket system to the end of your commit message
 * Work in branches where appropriate. For every feature/ticket a branch may be appropriate.
 * Use extensive comments as if you would be writing for [docco][docco]
 
[refactor]: http://www.extremeprogramming.org/rules/refactor.html
[commitmessage]: http://www.tpope.net/node/106
[timeline]: https://github.com/organizations/hudora/
[docco]: http://jashkenas.github.com/docco/


## Style

 * Wrap code at column 109. If you use Textmate type
   `defaults write com.macromates.textmate OakWrapColumns '( 40, 72, 78, 109 )'` to make wraping
   more comfortable.
 * Follow [PEP 8][pep8].
 * Follow [PEP 257][pep257] for docstrings
 * No tabs. Not anywhere (except in Makefiles). Always indent with 4 spaces.
 * use [flake8][flake8] to check compliance. 
 * Use [pylint][pylint]. See [gaetk][gaetkinc] for sesible options.
 * Classes/Variables which reference Objects specific to our ERP/our Industry/german trade should be in german as technical terms. Generic Objects should be named in english: "Lieferscheinnummer", "Kundenauftragsnumer", "Rechnung" but "TransportEndpoint" and "DataStore". This line is very blurry. See the "Protokolle" at SoftwareEntwicklung for further guidelines on naming.
 * Variable Names should not be abbreviated. The only exceptions are "nummer" -> "nr" and "kommissionier" -> "kommi".
 * Code should be targeted at Python 2.7 on FreeBSD / Ubuntu Linux or Google AppEngine
 * Functions should be no longer than a screen.
 * Helper functions should appear below their parent functions.
 * `__underscore_methods__()` and inner classes should always be defined first within a class.
 * Let [the Zen of Python][zen] guide you and avoid [Anti-Idioms][donts].
 * [Fail Fast][failfast] and [crash early][crashearly]!
 * Make your stuff [Idempotent][idempotent].
 * Always provide audit logs.
 * avoid float values where possible. They [probably don't work as you think they work][floats]. Store Cent instead of Euro, Millimeters instead of Centimeters and so on.
 * Provide a `Makefile` with `dependencies`, `test` and `check` (pylint/pyflakes/pep8) targets.

[pep8]: http://www.python.org/dev/peps/pep-0008/
[pep257]: http://www.python.org/dev/peps/pep-0257/
[flake8]: https://pypi.python.org/pypi/flake8
[pylint]: http://www.python.org/pypi/pylint 
[gaetkinc]: https://github.com/mdornseif/appengine-toolkit/blob/master/include.mk
[zen]: http://www.python.org/dev/peps/pep-0020/
[donts]: http://docs.python.org/howto/doanddont.html
[failfast]: http://en.wikipedia.org/wiki/Fail-fast 
[crashearly]: https://sites.google.com/a/hudora.de/intern/doc/blog-archiv/blog-sonstige-eintraege-2/offensive-programming-or-crash-early-crash-often
[coverage]: http://www.python.org/pypi/coverage
[floats]: http://docs.sun.com/source/806-3568/ncg_goldberg.html
[idempotent]: http://en.wikipedia.org/wiki/Idempotent


## Conventions

Use our naming conventions for [Adresses][adressprot], [Orders][orderprotocol] and [Warehouse related stuff][icwmsprot] (more to come).

[adressprot]: http://github.com/mdornseif/huTools/blob/master/doc/standards/address_protocol.markdown
[orderprotocol]: http://github.com/mdornseif/huTools/blob/master/doc/standards/verysimpleorderprotocol.markdown
[icwmsprot]: http://github.com/mdornseif/huTools/blob/master/doc/standards/messaging_ic-wms.markdown


## Identifiers

Use global unique identifiers where ever possible. `huTools.luids.guid128()` creates somewhat compact representations of random IDs. It's even better if you can find an standartisized Scheme of unique IDs. Good Candidates are found in the [EPC Tag Data Standard (TDS)][tds], in [Tag URIs][taguri] as defined in [RfC 4151][rfc4151]. Avoid global counters. Special considerations on Appengine apply. Try 

```kopf.guid = "c%s" % huTools.unicode.num_encode_uppercase(kopf.key.id())```

where `c` should be replaced by an object specific letter.

[tds]: http://www.epcglobalinc.org/standards/tds/
[taguri]: http://en.wikipedia.org/wiki/Tag_URI
[rfc4151]: http://tools.ietf.org/html/rfc4151


## Misc

* you can assume that setuptools, virtualenv, and pip are installed
* Always test Iñtërnâtiônàlizætiøn by putting strange strings into input fields
* Always test `<script>alert("XSS");</script> & <bold>Co</bold>` by putting strange strings into input fields
* use [huTools](http://hudora.github.com/huTools/) where appropriate
* `Iñtërnâtiônàlizætiøn <script>alert("XSS");</script> %+'"<!--` might be a good test string. Suggested Test Address:
    
    --!> Müller's & Æeleen\'s <!--
    Rue <script>alert("!");</script>
    IE-Dublin


## Google AppEngine Specifica

* Use `filter()` instead of GQL - skips the parsing step.
* Use [gaetk][gaetk], instead of Django
* Use `ndb`, instead of `db`
* Aim for response time under 1 s better under 500 ms and page sizes under 10 kb.
* Always comment the indexes you add to `index.yaml`


[gaetk]: https://github.com/mdornseif/appengine-toolkit


## Required Reading

* [HOWTO Use UTF-8 Throughout Your Web Stack][uft8stack]
* [Getting unicode right in Python][unicode]
* [The Zen of Python][zen]
* [Code Like a Pythonista: Idiomatic Python][idiomatic]
* [Google Python Style Guide][pyguide]
* [Refactoring: Improving the Design of Existing Code][refactoring] by Fowler, Beck, Brant, Opdyke, Roberts
* [An Illustrated History of Failure][failure] (Video)

[uft8stack]: http://rentzsch.tumblr.com/post/9133498042/howto-use-utf-8-throughout-your-web-stack
[unicode]: http://blog.notdot.net/2010/07/Getting-unicode-right-in-Python
[zen]: http://www.python.org/dev/peps/pep-0020/
[idiomatic]: http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
[pyguide]: http://google-styleguide.googlecode.com/svn/trunk/pyguide.html
[refactoring]: http://martinfowler.com/books.html#refactoring
[failure]: https://www.youtube.com/watch?v=KkoyVPPXt5w