# rssatom


**Table of Contents**

- [Installation](#installation)
- [License](#license)

## Installation

```console
pip install rssatom
```

## License

`rssatom` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.


## Usage:

usage: rssatom2html.py [-h] --url URL [--htmlfile HTMLFILE] [--show]<br/>

parse rss or atom file<br/>

options:<br/>
  -h, --help           show this help message and exit<br/>
  --url URL            url of an atom file to parse<br/>
  --htmlfile HTMLFILE  where to store the generated output<br/>
  --show               show the feed in a browser<br/>

rssatom2html retrieves a url containing an atom or rss feed, parses it
into html and, if --htmlfile and --show are invoked, displays the
generated html in your webbrowser

