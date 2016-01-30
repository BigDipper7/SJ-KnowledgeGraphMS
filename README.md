[![Build Status](https://travis-ci.org/BigDipper7/SJ-KnowledgeGraphMS.svg?branch=master)](https://travis-ci.org/BigDipper7/SJ-KnowledgeGraphMS)

# SJ-KnowledgeGraphMS
Python Flask - Knowledge Graph Management System

## Introduction ##
- this is just a Management System for Knowledge Graph using in S.J.  
- this web using python framework- `Flask` . have to admit, it's really a very  
  good light framework. good to use.  
- using `Cayley` with `MongoDB` to manage the whole Knowledge Graph
- using `travis-ci` to build and test

## Tech List ##
- `Cayley` with `MongoDB`
- `Flask` with `Flask-Boostrap` `wtforms`
- `Travis-ci`

## TODO List ##
- change to  `blueprint`
- integrate with `Flask-Login`
- add `MongoDB` Management System
- fulfill all in `test-all.py`
- fix order bug, and other things doesn't matter
- Need to change many alert to a new type, just like flash
- enhance: concurrency many people delete one at same time;
- enhance: flash with args
- enhance: return is true or false for delete action
- enhance: change to delete useless log clause



## Bug Wanted ##
- i guess the reason why it shows such a error, maybe just because that what you  
   do has change it, for the reason is there are two reasons, first one is that you  
   has post two same request but no response, maybe you needed to shorten the request  
   frequence, also maybe there two processing way, add lock or make other things.



## Bug fix list ##
- good now to fix bug in multi-lines display in card.html in sect_text, just pre-process all \n before send response back

- bug fix, bug because multi-lines in one excel cell, cause the constructed json data goes wrong
we can use \n to instead, or use || such a symbol to present.

- exists bug, can not delete absolutely, will fix it next day. it doesn't matter

- needed feature, add delete all button,
- fix bug
- add multi-lines present page in card.html

- find another bug, reason is that in the beginning of the string has a whitespace,  
  but in HTML, this beginning whitespace will be transfer into `&nbsp`, but when we  
  just post it to our server, this whitespace still be `&nbsp`, so it delete with a  
  wrong triples`'{}, {}, {'&nbspBLABLABLA BALBALBAL'}'`, so you can deal with such   
  things when you get to import such data, Gooooooood
- for delete, it just because you have make a wrong things that delete also must   
  escape `\n` to  `\\n`, that the reason.
- bug fixed, bug fix in delete maybe exist some bugs, means concurrency, i will   
  handle it hense
- the real reason for delete is the:  
  first, \n not change to \\n in json format_exc  
  second. Unknown char, the example is in the beginning

- enhance: change for `json.dumps(dict)` not use current manually add a json string


- enhance: Unknown char may make your delete char failed. like this sting ' natural person'  
  {just copy and paste}, the beginning of this string is an Unknown char, invisible also.  
  fix such a bug, because jinja2 will auto-escape, so such `Unknown character` may be auto-escape  
  to some curious html tag, just for secure reason, for not be XSS, so the auto-escape must be  
  open, but in the server side, i can use flask.Markup.unescape to handle the escaped post data  
  , and BTW, WTF, just fix Unknown character can not delete error, goooooooood, just fix this bug  

- bug fix in invisible code of delete bug, the reason is because that invisible character is 'NBSP'  
  in python string is: in `utf-8` `'\xc2\xa0'` in `unicode` `'\xa0'`, if it is `auto-escape` by flask  
  it will be `'&nbsp;'` in `HTML`

## Change List ##
- Add deprecated annotation, will delete useless code blocks in few days
- nothing changed  code review
- nothing change
