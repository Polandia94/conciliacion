from django.forms import *
from .models import Cbrenc, Cbrbcod, Cbrencl, Cbrerpd, Cbtcta, Cbtusu, Cbtemp,Cbtcol,Cbtbco


class CbrbcodForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CbrbcodForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['readonly'] = 'true'

        # self.fields['codbco'].widget.attrs['autofocus'] = True
    class Meta:
        model = Cbrbcod
        fields = ['fechatra', 'horatra', 'oficina', 'desctra', 'reftra', 'codtra', 'debe', 'haber', 'saldo' ]

class CbrerpdForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CbrerpdForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
            form.field.widget.attrs['readonly'] = 'true'

    class Meta:
        model = Cbrerpd
        fields = ['idrerpd',
                  'nrotra',
                  'fechatra',
                  'nrocomp',
                  'aux',
                  'ref',
                  'glosa',
                  'debe',
                  'haber',
                  'saldo',
                  'fechacon',
                  ]


class CbrencaForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        super(CbrencaForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['empresa'].widget.attrs['autofocus'] = True



    def save(self, commit=True):
        data={}
        form=super()
        try:
            if form.is_valid():
                data = form.save(commit=True)
            else:
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data

    class Meta:
        model = Cbrenc
        fields = ['idrenc', 'empresa', 'codbco', 'nrocta', 'ano', 'mes', 'archivoerp', 'archivobco', 'archivoimgbco' ]
        # fields = '__all__'
        widgets = {
            'idrenc': TextInput(
                attrs={'readonly': 'readonly'}
            ),
            'empresa': TextInput(
                attrs = { 'placeholder': 'Empresa',
                          'class': 'form-control'}
            ),            
            'codbco': TextInput(
                attrs = { 'placeholder': 'Clave del banco',
                          'class': 'form-control'}
            ),
            'nrocta': TextInput(
                attrs = { 'placeholder': 'Cuenta',
                          'class': 'form-control getanomes'}
            ),
            'ano': NumberInput(
                attrs={'placeholder': 'Año',
                          'class': 'form-control'}
            ),
            'mes': NumberInput(
                attrs = { 'placeholder': 'Mes',
                          'class': 'form-control'}
            ),
            'archivobco': FileInput(
                attrs = { 'placeholder': '',
                          'class': 'form-control'}
            ),
            'archivoerp': FileInput(
                attrs = { 'placeholder': '',
                          'class': 'form-control'}
            ),

            'archivoimgbco': FileInput(
                attrs = { 'placeholder': '',
                          'class': 'form-control'}
            )

        }


class CbtctaForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        super(CbtctaForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['empresa'].widget.attrs['autofocus'] = True

    def save(self, commit=True):
        data={}
        form=super()

        try:
            if form.is_valid():
                data = form.save(commit=True)
            else:
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data

    class Meta:
        model = Cbtcta
        fields = ['idtcta', 'empresa', 'codbco', 'nrocta','descta', 'monbasebco', 'monbaseerp', 'ano', 'mes', 'saldoinibco', 'saldoinierp' ]
        # fields = '__all__'
        widgets = {
            'idtcta': TextInput(
                attrs={'readonly': 'readonly', 
                            'class': 'form-control'}
            ),
            'empresa': TextInput(
                attrs = { 'placeholder': 'Empresa',
                          'class': 'form-control'}
            ),            
            'codbco': TextInput(
                attrs = { 'placeholder': 'Clave del banco',
                          'class': 'form-control'}
            ),
            'nrocta': TextInput(
                attrs = { 'placeholder': 'Cuenta',
                          'class': 'form-control'}
            ),
            'descta': TextInput(
                attrs = { 'placeholder': 'Descripcion Cuenta',
                          'class': 'form-control'}
            ),
            'monbasebco': TextInput(
                attrs = { 'placeholder': 'Mes Base Banco',
                          'class': 'form-control'}
            ),
            'monbaseerp': TextInput(
                attrs = { 'placeholder': 'Mes Base ERP',
                          'class': 'form-control'}
            ),
            'ano': NumberInput(
                attrs={'placeholder': 'Año',
                          'class': 'form-control'}
            ),
            'mes': NumberInput(
                attrs = { 'placeholder': 'Mes',
                          'class': 'form-control'}
            ),
            'saldoinibco': NumberInput(
                attrs = { 'placeholder': 'Saldo Inicial Banco',
                          'class': 'form-control'}
            ),
            'saldoinierp': NumberInput(
                attrs = { 'placeholder': 'Saldo Inicial ERP',
                          'class': 'form-control'}
            )

        }

class CbrencDeleteForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        super(CbrencDeleteForm, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(CbrencDeleteForm, self).get_form(request, obj, **kwargs)
        form.cbrenc = request.cbrenc
        return form 

    def save(self, commit=True):
        data={}
        form=super()
        try:
            if form.is_valid():
                data = form.save(commit=True)
            else:
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data

    class Meta:
        model = Cbrencl
        fields = ['idrenc', 'glosa']
        # fields = '__all__'
        widgets = {
            'idrenc': TextInput(
                attrs={'readonly': 'readonly', 
                            'class': 'form-control'}
            ),
            'glosa': TextInput(
                attrs = { 'placeholder': 'Glosa',
                          'class': 'form-control mb-2'}
            )

        }


class CbrencVerificarGuardado( ModelForm ):
    def __init__(self, *args, **kwargs):
        super(CbrencVerificarGuardado, self).__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(CbrencVerificarGuardado, self).get_form(request, obj, **kwargs)
        return form 

    def save(self, commit=True):
        data={}
        form=super()
        try:
            if form.is_valid():
                data = form.save(commit=True)
            else:
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data
    
class CbtusuForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        super(CbtusuForm, self).__init__(*args, **kwargs)
        self.fields['tipousu'].required = False
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'



    def save(self, commit=True):
        data={}
        form=super()

        try:            
            if form.is_valid():
                data = form.save(commit=True)
            else:
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data

    class Meta:
        model = Cbtusu
        fields = ['idusu1', 'descusu','tipousu','actpas']
        # fields = '__all__'
        widgets = {
            'idusu1': TextInput(
                attrs = { 'placeholder': 'Usuario',
                          'class': 'form-control'}
            ),            
            'descusu': TextInput(
                attrs = { 'placeholder': 'Descripcion del usuario',
                          'class': 'form-control'}
            ),
            'tipousu': CheckboxInput(
                attrs = { 'placeholder': 'Cuenta',
                          'class': 'form-control'}
            ),
            'actpas': CheckboxInput(
                attrs = { 'placeholder': 'Cuenta',
                          'class': 'form-control'}
            )        
                 
        }

class CbtempForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        super(CbtempForm, self).__init__(*args, **kwargs)
        self.fields['actpas'].required = False
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'



    def save(self, commit=True):
        data={}
        form=super()

        try:            
            if form.is_valid():
                data = form.save(commit=True)
            else:
                print(form.errors)
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data

    class Meta:
        model = Cbtemp
        fields = ['empresa', 'desemp','actpas']
        # fields = '__all__'
        widgets = {
            'empresa': TextInput(
                attrs = { 'placeholder': 'Empresa',
                          'class': 'form-control'}
            ),            
            'desemp': TextInput(
                attrs = { 'placeholder': 'Descripcion de la Empresa',
                          'class': 'form-control'}
            ),
            'actpas': CheckboxInput(
                attrs = { 'placeholder': '¿Está activa?',
                          'class': 'form-control'}
            )            
        }

class CbtbcoForm( ModelForm ):
    def __init__(self, *args, **kwargs):
        super(CbtbcoForm, self).__init__(*args, **kwargs)
        self.fields['actpas'].required = False
        for form in self.visible_fields():
            form.field.widget.attrs['autocomplete'] = 'off'



    def save(self, commit=True):
        data={}
        form=super()

        try:            
            if form.is_valid():
                data = form.save(commit=True)
            else:
                print(form.errors)
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data

    class Meta:
        model = Cbtbco
        fields = ['codbco','actpas']
        # fields = '__all__'
        widgets = {
            'codbco': TextInput(
                attrs = { 'placeholder': 'Banco',
                          'class': 'form-control'}
            ),            
            'actpas': CheckboxInput(
                attrs = { 'placeholder': '¿Está activo?',
                          'class': 'form-control'}
            )            
        }

class CbtusucForm( Form ):
    #def __init__(self, *args, **kwargs):
        #super(CbtusucForm, self).__init__(*args, **kwargs)
        #columnas = Cbtcol.objects.all()
        #for columna in columnas:
        #    self.fields[columna.descol].required = False
        #for form in self.visible_fields():
            #form.field.widget.attrs['autocomplete'] = 'off'

    def save(self, commit=True):
        data={}
        form=super()

        try:
            if form.is_valid():
                data = form.save(commit=True)
            else:
                data['error']=form.errors
        except Exception as e:
            print(e)
            data['error']=str( e )
        return data

    class Meta:
        #model = Cbtusuc
        # try permite crear las migraciones sin fallar
        try:
            columnas = Cbtcol.objects.all()
            lista=[]
            diccionario = {}
            for columna in columnas:
                lista.append(columna.descol)
                diccionario [columna.descol] = CheckboxInput(
                    attrs = { 
                            'class': 'form-control'}
                ) 

            fields = lista
            # fields = '__all__'
            widgets = diccionario
        except:
            pass