from django.http import HttpResponse
from django.shortcuts import render

def index(response):
    return render(response, 'index.html')
def inf(request):
    n1= (request.POST.get('text1', 'default'))#fetch data from user 
    n2=(request.POST.get('text2', 'default'))
    n1=n1.lower()#in case if user gives in capitalize it will convert to lower
    n2=n2.lower()
    pn1=""
    qn1=""
    pn2=""
    qn2=""
    n1=n1.split()
    n2=n2.split()#converts string to list
    bimples=False#this will take care when a "if then" statment was present in input
    for i in n1:
        if i=='then' or i=='and' or i=='or':#making chunks of major premse into pn1,qn1 by keeping constraints like then ,and,or
            
            pn1 = n1[0:n1.index(i)]#sliceing until any of the above condition is present
            qn1 = n1[n1.index(i)+1:]
            pn1=' '.join(pn1)#converting array to string
            if 'if' in pn1:
                bimples=True
                pn1=pn1[2:]
            qn1=' '.join(qn1)
            break
            

        else:
            pn1 = n1
            pn1=' '.join(pn1)

    for i in n2:
        if i=='then' or i=='and' or i=='or' :#making chunks of minor premse into pn2,qn2 by keeping constraints like then ,and,or
            pn2 = n2[0:n2.index(i)]
            
            qn2 = n2[n2.index(i)+1:]
        
            pn2=' '.join(pn2)
            if 'if' in pn2:
                bimples=True
                pn2=pn2[2:]
            
            qn2=' '.join(qn2)
            break

        else:
            
            pn2 = n2
            pn2=' '.join(pn2)
    r=validation(pn1,pn2,qn1,qn2,n1,n2,bimples)
    return render(request, 'output.html', r)

def validation(pn1,pn2,qn1,qn2,n1,n2,bimples):
    print(bimples)
    if  (pn1 and qn1 and pn2 and len(qn2)==0) and bimples:#base conditions for Modus Tollen,Modus Ponens
        if "not" in pn1 or "not" in pn2:#for Modus Tollen this is the conditions
            print("Therefore: ","not",pn2)
            res1="Modus Tollen, "+"Therefore: "+" ( Negation(~) of ) "+ pn2
            params = {'name':'The Conculsion is', 'string':res1}

        elif "not" not in pn1 :#for Modus Ponens this is the conditions
            res1="Modus Ponens, "+"Therefore: "+qn2+" "+qn1
            params = {'name':'The Conculsion is ', 'string':res1}

    elif pn1 and not qn1 and not n2:#base conditions for Addition
        print("Addition")
        n1s=' '.join(n1)
        print("Therefore: ",n1s,"or q   (Where q is any statement )")
        res1="Addition, "+"Therefore: "+n1s+" "+"or q   (Where q is any statement )"
        params = {'name':'The Conculsion is', 'string':res1}

    elif pn1 and not qn1 and pn2 and not qn2:#base conditions for Conjunction
        n1s=' '.join(n1)
        n2s=' '.join(n2)
        res1="Conjunction, "+"Therefore: "+n1s+" and " +n2s
        params = {'name':'The Conculsion is', 'string':res1}

    elif pn1 and qn1 and not n2:#base conditions for Simplification
        res1="Simplification, "+"Therefore: "+pn1
        params = {'name':'The Conculsion is', 'string':res1}

    elif (pn1 and qn1 and pn2 and not qn2):#base conditions for Disjunctive Syllogism
        res1="Disjunctive Syllogism, "+"Therefore: "+qn1
        params = {'name':'The Conculsion is', 'string':res1}


    elif pn1 and qn1 and pn2 and qn2 :#base conditions for Resoltuion,Hypothetical Syllogism
        if ('not' in pn2) and not bimples:
            print("Resoltuion")
            print("Therefore: ",qn1,"or",qn2)
            res1="Resoltuion, "+"Therefore: "+qn1+" or "+qn2
            params = {'name':'The Conculsion', 'string':res1}
            
        else:
            print("Hypothetical Syllogism")
            print("Therefore: ",pn1,"implies",qn2)
            res1="Hypothetical Syllogism, "+"Therefore: "+pn1+"implies"+qn2
            params = {'name':'The Conculsion is', 'string':res1}

    else:#when any of the above conditions are not satsifed 
        print("The given statements doesn't satisfy any Syllogisms !!. A relation(conclusion) cannot be established with the given statments")
        res1="The given statements doesn't satisfy any Syllogisms !!. A relation(conclusion) cannot be established with the given statments"
        params = {'name':'The Conculsion is ', 'string':res1}
    return params
