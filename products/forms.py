from django import forms
from . models import Category, Product, Customer, SystemSettings, Fund, Expense, OtherIncome, SupplierPayment, CustomerPayment, FundTransfer, Purchase, PurchaseItem



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'description': forms.TextInput(attrs={'class':'form-control', 'rows':3}),
        }
        

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__" 


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'phone', 'address', 'note']
        
        
class SystemSettingsForm(forms.ModelForm):
    class Meta:
        model = SystemSettings
        fields = '__all__'
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }

class FundForm(forms.ModelForm):
    class Meta:
        model = Fund
        fields = ['fund_name', 'fund_type', 'amount', 'description']


class ExpenseForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Expense
        fields = ['category', 'fund', 'amount', 'date', 'note']
        
        
class OtherIncomeForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = OtherIncome
        fields = ['category', 'fund', 'amount', 'date', 'note']
        
        
class SupplierPaymentForm(forms.ModelForm):
    class Meta:
        model = SupplierPayment
        fields = ['supplier', 'fund', 'amount',  'note']
        
class CustomerPaymentForm(forms.ModelForm):
    class Meta:
        model = CustomerPayment
        fields = ['customer', 'fund', 'amount',  'note']


class FundTransferForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = FundTransfer
        fields = ['from_fund', 'to_fund', 'amount', 'date', 'note']        


        

class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = [
            'supplier',
            'discount',
            'service_charge',
            'status'
        ]
        
        
class PurchaseItemForm(forms.ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['product', 'quantity', 'purchase_price']

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return quantity

        
