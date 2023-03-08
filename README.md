# Overview

Not Slithering Anywhere is the Python(3) version of our [Not Go-ing Anywhere](https://github.com/trailofbits/not-going-anywhere) vulnerable
application. It is meant to demonstrate a number of security issues commonly found in Python applications, as well as serve as the basis
for static & dynamic tool testing grounds.

# Getting started

1. Setup a venv ala `python3 -m venv ~/.venv/class`
1. Enter your venv ala `source ~/.venv/class/bin/activate`
1. Install dependencies: `pip3 install -r requirements.txt`
1. Run the class: `python3 app.py`

The class itself uses common libraries such as flask, SQLAlchemy, and jinja2 to explain vulnerabilities.

# Expected Vulnerabilities

## Server

1. Server Misconfiguration
    1. CORS
    1. Caching
1. Injection Related
    1. XSS (technically separate according to OWASP)
    1. SQLi
    1. Server-Side Template Inclusion (SSTI)
1. Incorrect data validation (paths)
1. AuthN/AuthZ failures

## General Python

1. Unix & Python Environment
1. Keys & Sensitive Data Storage
1. Pickles & Serialization
1. Dependencies & Tooling
