from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth import authenticate,login
# Create your views here.


def kologin(request):

    if 'kologin' in request.POST:
        print('user clicked login button')
        loginuname = request.POST.get('kologinusername')
        loginpassword = request.POST.get('kologinpassword')
        print(loginuname,loginpassword)

        a = authenticate(usernamae = loginuname,password = loginpassword)
        print(a)

        if a is not None:
            login(request,a)
            print('user passed to home page')

        else:
            try:
                user_table = Kouser.objects.get(username = loginuname)
                print(user_table)
                print(user_table.id)
                request.session['userid'] = user_table.id
                print(user_table.password)
                if user_table.password == loginpassword:
                    login(request,a)
                    print('user passed to home page')
                    return redirect('kohome')
                else:
                    return render(request,'KOKO_tmpl/kologin.html',{'errormessage':"PASSWORD DOESN'T MATCH"})

            except Exception as e:
                print(e)
                print('no user found')
                return render(request,'KOKO_tmpl/kologin.html',{'errormessage':'NO USER FOUND'})

    return render(request,'KOKO_tmpl/kologin.html')


def kosignin(request):

    default_message = 'PLEASE FILL THIS INFORMATIONS CAREFULLY'
    if 'signinsubmit' in request.POST:
        suser = request.POST.get('username')
        sfn = request.POST.get('firstname')
        sln = request.POST.get('lastname')
        semail = request.POST.get('email')
        sphone = request.POST.get('phone')
        sdob = request.POST.get('dob')
        spword = request.POST.get('password')
        sgender = request.POST.get('gender')
        sclid = request.POST.get('clientid')
        sadd = request.POST.get('address')
        print(suser,sfn,sln,semail,sphone,sdob,sclid,sadd,sgender,spword)

        #check if user is there or not..
        try:
            check = Kouser.objects.get(username = suser)
            print(check)
            return render(request,'KOKO_tmpl/kosignin.html',{'message':'USER ALREADY EXITS'})
        except:
            #creating a data in data for new user.. 
            create = Kouser.objects.create(username = suser,first_name = sfn,last_name = sln,email = semail,Phone = sphone,Is_client = 1,
            Gender = sgender,DoB = sdob,password = spword)
            create.save()
            create_client = Koclient.objects.create(Username = create,User_type = 'CLEINT',Address = sadd,Client_id = sclid,Client_Status = 'GOOD')
            create_client.save()
            return redirect('kologin')

    return render(request,'KOKO_tmpl/kosignin.html',{'message':default_message})


def kohome(request):

    userid = request.session['userid']
    userobject = Kouser.objects.get(id = userid)

    if userobject.Is_bank:
        sups = Kosupplier.objects.all()
        clis = Koclient.objects.all()
        if 'oursup' in request.POST:
            return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','supplier':sups,'userobject':userobject})
        elif 'ourcli' in request.POST:
            return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','clients':clis,'userobject':userobject})
        elif 'addcli' in request.POST:
            print('adding')
            return redirect('kosignin')
        elif 'editc' in request.POST:
            print('edit')
            return redirect('editc')
        elif 'aproval' in request.POST:
            print("approvals")
            appr = Verified_Invoice.objects.all()
            print(appr)
            return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','approvals':appr,'userobject':userobject})
        elif 'appsubmit' in request.POST:

            Requested_by = request.POST.get('Requested_by')
            Supplier_code= request.POST.get('Supplier_code')
            Invoice_number = request.POST.get('Invoice_number')
            Invoice_date = request.POST.get('Invoice_date')
            Invoice_amount = request.POST.get('Invoice_amount')
            Currency = request.POST.get('Currency')
            Approved_by = request.POST.get('Approved_by')
            Verified_by  = request.POST.get('Verified_by ')
            
            appr = Verified_Invoice.objects.all()


            Approved_In = Approved_Invoice.objects.create(
            Requested_by = Requested_by,
            Supplier_code=Supplier_code,
            Invoice_number = Invoice_number,
            Invoice_date = Invoice_date,
            Invoice_amount = Invoice_amount,
            Currency = Currency,
            Approved_by = Approved_by,)

            Approved_In.save()

            
            return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','approvals':appr,'userobject':userobject})

        elif 'apdeny' in request.POST:
            Requested_by = request.POST.get('Requested_by ')
            Supplier_code= request.POST.get('Supplier_code')
            Invoice_number = request.POST.get('Invoice_number')
            Invoice_date = request.POST.get('Invoice_date')
            Invoice_amount = request.POST.get('Invoice_amount')
            Currency = request.POST.get('Currency')
            Approved_by = request.POST.get('Approved_by')
            Verified_by  = request.POST.get('Verified_by ')
            
            appr = Verified_Invoice.objects.all()
            delete = Verified_Invoice.objects.all()
            print('delete operation is under work')
            return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','approvals':appr,'userobject':userobject})
        elif 'apinap' in request.POST:
            aproed = Approved_Invoice.objects.all()
            return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','approved':aproed,'userobject':userobject})

        else:
            return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','supplier':sups,'userobject':userobject})

        
        


    elif userobject.Is_client:
        print('cli')
        k = Koclient.objects.filter(Username = userobject)
        print(k)
        a = ''
        for i in k:
            a = i.Client_id
            print(a)
        poda = Approved_Invoice.objects.filter(Requested_by = a)
        print(poda)
        if 'crcli' in request.POST:
            return render(request,'KOKO_tmpl/kohome.html',{'role':'client','userobject':userobject, 'poda':poda})
        elif 'upload' in request.POST:
            return redirect('noway')
        return render(request,'KOKO_tmpl/kohome.html',{'role':'client','userobject':userobject, 'poda':poda})


    elif userobject.Is_supplier:
        print('sup')
        a = Approved_Invoice.objects.all()
        d = Denied.objects.all()
        if 'sourcli' in request.POST:
            print('clients')
            
            print(a,d)
            return render(request,'KOKO_tmpl/kohome.html',{'role':'supplier','userobject':userobject,'approve':a,'denied':d})
        elif 'seditcli' in request.POST:
            print('edit client')
            return redirect('editc')
        elif 'saddcli' in request.POST:
            print('add edit')
            return redirect('kosignin')
        elif 'verpend' in request.POST:
            print('verfications')
            return redirect('kover')
        else:
            return render (request,'KOKO_tmpl/kohome.html',{'role':'supplier','userobject':userobject,'approve':a,'denied':d})
            
    return render(request,'KOKO_tmpl/kohome.html',{'role':'bank','userobject':userobject})
                


def koeditclient(request):

    userid = request.session['userid']
    userobject = Kouser.objects.get(id = userid)
    clis = Kouser.objects.filter(Is_client = True)

    if 'editv' in request.POST:
        print('yaa we can edit')
        sfn = request.POST.get('firstname')
        sln = request.POST.get('lastname')
        semail = request.POST.get('email')
        sphone = request.POST.get('phone')
        sdob = request.POST.get('dob')
        sgender = request.POST.get('gender')
        suser = request.POST.get('username')
        print(sfn,sln,semail,sphone,sdob,sgender,)
        try:
            edit = Kouser.objects.get(username = suser)
            edit.first_name = sfn
            edit.last_name = sln
            edit.email = semail
            edit.Phone =sphone
            edit.DoB = sdob
            edit.Gender = sgender
            edit.save()
            return render(request,'KOKO_tmpl/koeditclient.html',{'userobject':userobject,'clients':clis,'error':'edits saved'})
        except Exception as e:
            print(e)
            return render(request,'KOKO_tmpl/koeditclient.html',{'userobject':userobject,'clients':clis,'error':'please dont change username'})
    elif 'delete' in request.POST:
         suser = request.POST.get('username')
         delete= Kouser.objects.filter(username = suser).delete()
         
    return render(request,'KOKO_tmpl/koeditclient.html',{'userobject':userobject,'clients':clis})


   
def kover(request):
    userid = request.session['userid']
    userobject = Kouser.objects.get(id = userid)
    rin = Requested_Invoice.objects.filter(defa = 'defa')

    if 'sverf' in request.POST:
        print('verfication done')
        supc = request.POST.get('5')
        innum = request.POST.get('1')
        indt = request.POST.get('2')
        rqby = request.POST.get('3')
        inamt = request.POST.get('4')
        cur = request.POST.get('6')
        apby = request.POST.get('7')
        print(supc,innum,indt,rqby,inamt,cur,apby)
        ok = Verified_Invoice.objects.create(
            Verified_by = apby,
            Requested_by = rqby,
            Supplier_code = supc,
            Invoice_number  = innum,
            Invoice_date = indt,
            Invoice_amount = inamt,
            Currency = cur

        )
        dele = Requested_Invoice.objects.get(Invoice_number = innum)
        print(dele)
        dele.delete()
    elif 'sdeny' in request.POST:
        supc = request.POST.get('5')
        innum = request.POST.get('1')
        indt = request.POST.get('2')
        rqby = request.POST.get('3')
        inamt = request.POST.get('4')
        cur = request.POST.get('6')
        apby = request.POST.get('7')
        print(supc,innum,indt,rqby,inamt,cur,apby)
        ok = Denied.objects.create(
            Invoice_number = innum,
            Denied_by  = 'supplier'
        )
        dele = Requested_Invoice.objects.get(Invoice_number = innum)
        print(dele)
        dele.delete()
    return render(request,'KOKO_tmpl/kover.html',{'rin':rin,'userobject':userobject})

def noway(request):
    print('upload')
    userid = request.session['userid']
    userobject = Kouser.objects.get(id = userid)
    if 'hgj' in request.POST:
        print('hgj')
        reby = request.POST.get('a')
        supid = request.POST.get('b')
        innum = request.POST.get('c')
        indt = request.POST.get('d')
        inamt = request.POST.get('e')
        cur = request.POST.get('f')

        print(reby,supid,innum,indt,inamt,cur)

        hj = Requested_Invoice.objects.create(
            Requested_by = reby,
            Supplier_code = supid,
            Invoice_number = innum,
            Invoice_date = indt,
            Invoice_amount=inamt,
            Currency = cur,

        )
        hj.save()
    else:
        print('hello')
    return render(request,'KOKO_tmpl/kohome.html',{'role':'client','userobject':userobject,'vena':'sona'})
