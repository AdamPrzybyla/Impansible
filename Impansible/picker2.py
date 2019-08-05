import re
def picker2(w,p):
	if not p: return picker2_norm_str(w)
	e=p[0]
	p1=p[1:]
	if re.match("[0-9]+$",e): w=picker2_liczba(w,e,p1)
	elif re.search(",",e):
		if isinstance(w,dict):
			wklu,w,eklu,klu=picker2_przecinek(w,e,p1)
			if not p1: return picker2_si(wklu,w)
		else:
			return " ".join([picker2(w,[z]+list(p1)) for z in e.split(",")])
	elif re.search("=",e): w,e=picker2_rowne(w,e,p1)
	elif re.search("~",e): w,e=picker2_tylda(w,e,p1)
	elif e=='?': w=picker2_question(w)
	elif e=='+': w=picker2_plus(w,p1)
	else: w=picker2_attr(w,e,p1)
	#if type(w)==list:
	#	print "-"*20
	#	print w
	return picker2_norm(w)

def picker2_si(wklu,w):
	w=[type(x)==int and str(x) or x for x in w]
	if any(wklu):
		return " ".join([mno(a,b) for a,b in zip(w,wklu)])
	if all([isinstance(x,basestring) for x in w]):
		return " ".join(w)
	return w

def picker2_przecinek(w,e,p1):
	klu=e.split(",")
	wklu=[]
	eklu=[]
	for k in klu:
		if k[-3:] in ["GiB","MiB","KiB"]:
			eklu.append(k[:-3])
			wklu.append(k[-3:])
		else:
			eklu.append(k)
			wklu.append("")
	klu=eklu
	w=[picker2(w,[kl]+list(p1)) for kl in klu]
	return wklu,w,eklu,klu

def picker2_norm_str(w):
	if isinstance(w,int):
		w=str(w)
	return w

def picker2_norm(w):
	if isinstance(w,(list,tuple)) and len(w)==1: w=w[0]
	return w

def picker2_attr(w,e,p1):
	if hasattr(w,"get") and e in w:
		w=w.get(e,[])
	elif hasattr(w,e):
		w=getattr(w,e)
	elif e.find('.')+1:
		for k in e.split('.'):
			if isinstance(w,dict):
				w=w[k]
			elif isinstance(w,list):
				w=w[int(k)]
			else:
				w=getattr(w,k)
	else:
		w=[]
	if w: w=picker2(w,p1)
	return w

def picker2_plus(w,p1):
	if isinstance(w,dict):
		w=w.values()
	w=[picker2(kl,p1) for kl in w]
	w=[kl for kl in w if kl]
	return w

def picker2_question(w):
	if isinstance(w,dict):
		w=" ".join(w.keys())
	elif isinstance(w,list):
		w="<list> %d"%len(w)
	else:
		w="<string>"
	return w

def picker2_tylda(w,e,p1):
	e=e.split('~')
	if isinstance(w,(list,tuple)):
		w=[picker2(k,p1) for k in w if re.search("(?i)"+e[1],unicode(k.get(e[0],"")))]
	if isinstance(w,dict):
		w=w.values()
		w=[picker2(k,p1) for k in w if re.search("(?i)"+e[1],unicode(k.get(e[0],"")))]
	return w,e

def picker2_rowne(w,e,p1):
	e=e.split('=')
	if isinstance(w,(list,tuple)):
		w=[picker2(k,p1) for k in w if unicode(k.get(e[0],""))==e[1]]
	if isinstance(w,dict):
		w=w.values()
		w=[picker2(k,p1) for k in w if unicode(k.get(e[0],""))==e[1]]
	return w,e

def picker2_liczba(w,e,p1):
	if isinstance(w,dict):
		if e in w:
			w=picker2(w[e],p1)
		else:
			w=picker2(w[int(e)],p1)
	if isinstance(w,(list,tuple)):
		w=picker2(w[int(e)],p1)
	return w
