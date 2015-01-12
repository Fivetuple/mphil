#!/usr/bin/python
#
#
#  PJM 2006
#
#  This program reads and applies a letter n-gram model in ARPA-MIT format
#  uses it to estimate the most likely natural language
#  of the input text.

import sys
import os

emiss = 0
gmiss = 0
dmiss = 0


def list2string(l):

    out = ""
    for i in l:
	if i[0:3] == 'en_':
	    out += i[3]
            prefix = 'en_'
	elif i[0:3] == 'ge_':
	    out += i[3]
            prefix = 'ge_'
	elif i[0:3] == 'du_':
	    out += i[3]
            prefix = 'du_'
	elif i[0:3] == "<s>":
	    prefix = "xx_"
	    out += '$'
	elif i[0:4] == "</s>":
	    prefix = "xx_"
	    out += '.'
	else:
	    out += i 
    return prefix + out


#\1-grams:
#-1.069272	</s>
#-99	<s>	-4.280336
#-1.574383	du_a	-5.02618

#\2-grams:
#-1.520534	<s> du_a	-2.295027

#\3-grams:
#-0.6061128	<s> du_a du_a	-2.718146
#-1.736837	<s> du_a du_b	-1.274791
#-1.215247	<s> du_a du_c	-1.291715

#\4-grams:
#-2.830785	<s> du_a du_a du_g
#-2.658878	<s> du_a du_a du_i
#-1.849013	<s> du_a du_a du_l

# 
# Read language model
#

fplm = open(sys.argv[1], 'r')

lm = fplm.readlines()


en_lm= { }
ge_lm= { }
du_lm= { }
en_lm1= { }
ge_lm1= { }
du_lm1= { }
en_lm2= { }
ge_lm2= { }
du_lm2= { }
en_lm3= { }
ge_lm3= { }
du_lm3= { }


got1 = 0
got2 = 0
got3 = 0
got4 = 0

for line in lm:

#     print  line

     if (line == '\\2-grams:\n'):
        got1 = 0
        got2 = 1
        continue

     if (line == '\\3-grams:\n'):
        got2 = 0
        got3 = 1
        continue

     elif (line == '\\4-grams:\n'):
        got3 = 0
        got4 = 1
        continue

     if got1:
	     els = line.split()
	     if len(els) == 0: continue

	     if len(els) > 2 :
             	val = els[0] + " " + els[2]
	     else:
             	val = els[0] + " 0"
		
	     preq = list2string(els[1:2])
	     if preq[0:3] ==  'en_':
  	         en_lm1[preq[3:]] = val
	     if preq[0:3] ==  'ge_':
  	         ge_lm1[preq[3:]] = val
	     if preq[0:3] ==  'du_':
  	         du_lm1[preq[3:]] = val

     if got2:
	     els = line.split()
	     if len(els) ==0: continue

	     #print els
             if len(els) > 3 :
             	val = els[0] + " " + els[3]
	     else:
             	val = els[0] + " 0"
		
	     preq = list2string(els[1:3])
	     if preq[0:3] ==  'en_':
  	         en_lm2[preq[3:]] = val
	     if preq[0:3] ==  'ge_':
  	         ge_lm2[preq[3:]] = val
	     if preq[0:3] ==  'du_':
  	         du_lm2[preq[3:]] = val

     elif got3:
	     els = line.split()
	     if len(els) ==0: continue

	     #print els
             if len(els) > 4 :
             	val = els[0] + " " + els[4]
	     else:
             	val = els[0] + " 0"
		
	     preq = list2string(els[1:4])
	     if preq[0:3] ==  'en_':
  	         en_lm3[preq[3:]] = val
	     if preq[0:3] ==  'ge_':
  	         ge_lm3[preq[3:]] = val
	     if preq[0:3] ==  'du_':
  	         du_lm3[preq[3:]] = val

     elif got4:
	     els = line.split()
	     # print(els)
	     if len(els) ==0: break
             val = els[0]
	     preq = list2string(els[1:5])
	     if preq[0:3] ==  'en_':
  	         en_lm[preq[3:]] = val
	     if preq[0:3] ==  'ge_':
  	         ge_lm[preq[3:]] = val
	     if preq[0:3] ==  'du_':
  	         du_lm[preq[3:]] = val
     else:
	if  (line == '\\1-grams:\n'): got1 = 1


#print ge_lm1
#print ge_lm2
#print ge_lm3
#print ge_lm

#sys.exit()	

#en_lm= { }
#ge_lm= { }
#du_lm= { }
#en_lm3= { }
#ge_lm3= { }
#du_lm3= { }


#
# lang_model
#
def lang_model(lang, size):

    if lang == 'en': 
	   if size == 4: return en_lm
	   elif size == 3: return en_lm3
	   elif size == 2: return en_lm2
	   elif size == 1: return en_lm1

    elif lang == 'ge': 
	   if size == 4: return ge_lm
	   elif size == 3: return ge_lm3
	   elif size == 2: return ge_lm2
	   elif size == 1: return ge_lm1

    elif lang == 'du': 
	   if size == 4: return du_lm
	   elif size == 3: return du_lm3
	   elif size == 2: return du_lm2
	   elif size == 1: return du_lm1

    else: print "Unknown lang in lang_model: " + str(lang)

#
# nlookup1
#
def nlookup_1(lang, cand, bo):

#    print "Cand is " + cand
    if cand == '$' or cand == '.': return 0

    lm_dict = lang_model(lang,1)
    if lm_dict.has_key(cand):
	  vals = lm_dict[cand].split()
	  if bo: out = float(vals[0]) + float(vals[1])
	  else: out = float(vals[0])
    else:
	print "Symbol not found: " + cand
#	print lm_dict
    return out

#
# nlookup2
#
def nlookup_2(lang, cand, bo):

    lm_dict = lang_model(lang,2)
    if lm_dict.has_key(cand):
	  vals = lm_dict[cand].split()
	  if bo: out = float(vals[0]) + float(vals[1])
	  else: out = float(vals[0])
    else:
	 # out = nlookup_1(lang,cand[0:1],1)
	  out = nlookup_1(lang,cand[1:2],1)
    return out

#
#
# nlookup3
#
def nlookup_3(lang, cand, bo):

    lm_dict = lang_model(lang,3)
    if lm_dict.has_key(cand):
	  vals = lm_dict[cand].split()
	  if bo: out = float(vals[0]) + float(vals[1])
	  else: out = float(vals[0])
    else:
	 # out = nlookup_2(lang,cand[0:2],1)
	 out = nlookup_2(lang,cand[1:3],1)
    return out

#
# nlookup4
#
def nlookup_4(lang, cand):

    lm_dict = lang_model(lang,4)
    if lm_dict.has_key(cand):
	  out = float(lm_dict[cand])
    else:
#	  out = nlookup_3(lang,cand[0:3],1) 
	  out = nlookup_3(lang,cand[1:4],1) 
    return out


#
# ngram lookup
#
def nlookup(lang, cand):

#    print "Nlookup lang: " + lang + ", cand: " + cand
    if len(cand) == 4:
	return nlookup_4(lang, cand)

    elif len(cand) == 3:
	return nlookup_3(lang, cand, 0)

    elif len(cand) == 2:
	return nlookup_2(lang, cand, 0)

    else:
	return nlookup_1(lang, cand, 0)


# 
# idlang
#
def idlang(aword):

	en_lp = 0
	ge_lp = 0
	du_lp = 0

	for i in range(3):
		en_lp += nlookup('en',aword[0:i+1])
		ge_lp += nlookup('ge',aword[0:i+1])
		du_lp += nlookup('du',aword[0:i+1])
#		print "en_lp: " + str(en_lp)


	if len(aword) > 3:
		for a in range(len(aword) - 1):
	               
			quad = aword[a:a+4]

			en_lp += nlookup('en',quad)
			ge_lp += nlookup('ge',quad)
			du_lp += nlookup('du',quad)

	if en_lp > ge_lp and en_lp > du_lp : 
		lang = 'en'
	elif ge_lp > en_lp and ge_lp > du_lp : 
		lang = 'ge'
	elif du_lp > en_lp and du_lp > ge_lp : 
		lang = 'du'
	else:
		lang = 'xx'

	out = lang + " " + str(en_lp) + " " + str(ge_lp) + " " + str(du_lp)
	return( out)

# 
# Main
#

fp = open(sys.argv[2], 'r')
entries = fp.readlines()

for word in entries:

        aword = "$" + word.strip() + '.'
	lang = idlang(aword)
	print word.strip() + " " + lang

