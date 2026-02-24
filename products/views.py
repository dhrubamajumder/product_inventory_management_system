from django.shortcuts import render, redirect, get_object_or_404
from . models import Category, Product, ExpenseCategory, IncomeCategory, Customer, Supplier, SystemSettings, Fund, Expense, OtherIncome, SupplierPayment, CustomerPayment, FundTransfer, Order, OrderItem, PurchaseItem, Purchase, Stock, PurchaseReturn
from . forms import CategoryForm, ProductForm, CustomerForm, SystemSettingsForm, FundForm, ExpenseForm, OtherIncomeForm, SupplierPaymentForm, CustomerPaymentForm, FundTransferForm, PurchaseForm, PurchaseItemForm
from django.contrib import messages
from django.forms import modelformset_factory
from django.forms import modelform_factory
from django.core.paginator import Paginator
from .utils import paginate_queryset
import json
from decimal import Decimal
from django.db import transaction
from django.db.models import Sum
from django.db.models import Q, F


# Create your views here.

def index(request):
    return render(request, 'index.html')

# ------------------------------------   Category List  ------------------------------------------
def category_list(request):
    categories = Category.objects.all().order_by('-id')
    page_obj = paginate_queryset(request, categories, per_page=10)
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Category added successfully")
            return redirect('category_list')
    context = {'form': form, 'page_obj': page_obj, 'per_page': request.GET.get('per_page', 10),}
    return render(request, 'category/category_list.html', context)


def category_update(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Category updated successfully")
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_list.html', {'form': form, 'category': category})


def category_delete(request, id):
    category = get_object_or_404(Category, id=id)
    if request.method == "POST":
        category.delete()
        messages.success(request, "🗑️ Category deleted successfully")
    return redirect('category_list')


# -------------------------------------------------------------   Product   ---------------------------------------------
def product_list(request):
    products = Product.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(products, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'product/product_list.html', {'page_obj': page_obj, 'per_page': per_page,})
    
def product_create(request):
    categories = Category.objects.all()
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Product added successfully")
            return redirect('product_list')
    else:
        form = ProductForm()
    context = {'form': form, 'categories': categories,}
    return render(request, 'product/product_form.html', context)

def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    categories = Category.objects.all()  
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Product updated successfully")
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
        'categories': categories,}
    return render(request, 'product/product_form.html', context)

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        messages.success(request, "🗑️ Product deleted successfully")
        return redirect('product_list')
    

# ---------------------------------------------------------   Expense Category View  -----------------------------------------------
def expense_category_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            ExpenseCategory.objects.create(name=name)
            return redirect("expense_category")
    ex_categories = ExpenseCategory.objects.all().order_by('-id')
    page_obj = paginate_queryset(request, ex_categories, per_page=10)
    context = {
        'categories': ex_categories,
        'page_obj': page_obj,
        'per_page': request.GET.get('per_page', 10), 
    }
    return render(request, 'expence/expense_category.html', context)


def expense_category_update(request, id):
    category = get_object_or_404(ExpenseCategory, id=id)
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            category.name = name
            category.save()
        return redirect("expense_category")
    
def expense_category_delete(request, id):
    if request.method == "POST":
        ExpenseCategory.objects.filter(id=id).delete()
    return redirect('expense_category')



# -------------------------------------------  Other Income Category View  -----------------------------------------------------------
def income_category_view(request):
    # CREATE
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            IncomeCategory.objects.create(name=name)
            messages.success(request, "✅ Income category added successfully")
            return redirect("income_category")
    
    # LIST
    categories = IncomeCategory.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(categories, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
    }
    return render(request, 'other_income/income_category.html', context)

def income_category_update(request, id):
    category = get_object_or_404(IncomeCategory, id=id)
    if request.method == "POST":
        category.name = request.POST.get("name")
        category.save()
    return redirect("income_category")


def income_category_delete(request, id):
    if request.method == "POST":
        IncomeCategory.objects.filter(id=id).delete()
    return redirect('income_category')



# ------------------------------------------------------  Supplier View  -----------------------------------------------
def supplier_list(request):
    suppliers = Supplier.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    paginator = Paginator(suppliers, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'per_page': per_page,}
    return render(request, 'supplier/suppliers.html', context)

# -----------------------------
# Supplier Create View
# -----------------------------
def supplier_create(request):
    if request.method == "POST":
        Supplier.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
        )
        messages.success(request, "✅ Supplier added successfully")
        return redirect('supplier')
    return render(request, 'supplier/supplier_form.html')

# -----------------------------
# Supplier Update View
# -----------------------------
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == "POST":
        supplier.name = request.POST.get('name')
        supplier.phone = request.POST.get('phone')
        supplier.address = request.POST.get('address')
        supplier.save()
        messages.success(request, "✏️ Supplier updated successfully")
        return redirect('supplier')
    context = {'supplier': supplier}
    return render(request, 'supplier/supplier_form.html', context)

# -----------------------------
# Supplier Delete View
# -----------------------------
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == "POST":
        supplier.delete()
        messages.success(request, "🗑️ Supplier deleted successfully")
    return redirect('supplier')

# --------------------------------------------------------------  Customer View -----------------------------------------------------------

def customer_list(request):
    customers = Customer.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    paginator = Paginator(customers, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
    }
    return render(request, 'customer/customer.html', context)

# ---------------------------
# 2. Customer Create View
# ---------------------------
def customer_create(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "✅ Customer added successfully")
            return redirect('customer')
    else:
        form = CustomerForm()
    return render(request, 'customer/customer_form.html', {'form': form})


# ---------------------------
# 3. Customer Update View
# ---------------------------
def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            messages.success(request, "✏️ Customer updated successfully")
            return redirect('customer')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer/customer_form.html', {'form': form, 'customer': customer})


# ---------------------------
# 4. Customer Delete View
# ---------------------------
def customer_delete(request, pk):
    if request.method == "POST":
        Customer.objects.filter(pk=pk).delete()
        messages.success(request, "🗑️ Customer deleted successfully")
    return redirect('customer')


# =================================================================================================
# ===============================      Settings   =================================================
# =================================================================================================

def settings_list(request):
    settings_instance = SystemSettings.objects.first()
    return render(request, 'settings/setting_list.html', {'settings': settings_instance})


# Create new system settings
def setting_create(request):
    if SystemSettings.objects.exists():
        return redirect('settings_list')
    if request.method == "POST":
        form = SystemSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.POST.get('delete_logo') and instance.logo:
                instance.logo.delete(save=False)
                instance.logo = None
            instance.save()
            return redirect('settings_list')
    else:
        form = SystemSettingsForm()
    print(form.instance.logo)   
    print(form.errors)    
    return render(request, 'settings/setting_form.html', {'form': form, 'title': 'Create System Settings'})
      
def setting_update(request, pk):
    settings_update = get_object_or_404(SystemSettings, pk=pk)
    if request.method == "POST":
        form = SystemSettingsForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            if request.POST.get('delete_logo') and instance.logo:
                instance.logo.delete(save=False)
                instance.logo = None
            instance.save()
            return redirect('settings_list')
    else:
        form = SystemSettingsForm(instance=settings_update)
    return render(request, 'settings/setting_form.html', {'form':form, 'title':'Update System Settings'})


# -=====================================================   Fund Create  ================================
def fund_list(request):
    per_page = int(request.GET.get('per_page', 10))
    page = request.GET.get('page', 1)

    funds = Fund.objects.all().order_by('id')  # 👈 fresh queryset

    paginator = Paginator(funds, per_page)
    page_obj = paginator.get_page(page)

    return render(request, 'fund/fund_list.html', {
        'page_obj': page_obj,
        'per_page': per_page,
    })
    
    
# Create
def fund_create(request):
    form = FundForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('fund_list')
    return render(request, 'fund/fund_form.html', {'form': form})

# Update
def fund_update(request, id):
    fund = get_object_or_404(Fund, id=id)
    form = FundForm(request.POST or None, instance=fund)
    if form.is_valid():
        form.save()
        return redirect('fund_list')
    return render(request, 'fund/fund_form.html', {'form': form, 'fund':fund})

# Delete
def fund_delete(request, id):
    fund = get_object_or_404(Fund, id=id)
    fund.delete()
    return redirect('fund_list')


# ===========================   Expence Create  ===========================

def expense_list(request):
    expenses = Expense.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    paginator = Paginator(expenses, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'per_page': per_page,}
    return render(request, 'expence/expence_list.html', context)

# 2️⃣ Create Expense
def expense_create(request):
    form = ExpenseForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('expense_list')
    categories = ExpenseCategory.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'expense': None,
        'categories': categories,
        'funds': funds,}
    return render(request, 'expence/expence_form.html', context)


# Update Expense
def expense_update(request, id):
    expense = get_object_or_404(Expense, id=id)
    form = ExpenseForm(request.POST or None, instance=expense)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('expense_list')
    categories = ExpenseCategory.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'expense': expense,
        'categories': categories,
        'funds': funds,}
    return render(request, 'expence/expence_form.html', context)

# 4️⃣ Delete Expense
def expense_delete(request, id):
    expense = get_object_or_404(Expense, id=id)
    expense.delete()
    return redirect('expense_list')



# -=====================================================   Fund Create  ===========================================
def income_list(request):
    income = OtherIncome.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    paginator = Paginator(income, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,}
    return render(request, 'other_income/income_list.html', context)

def income_create(request):
    form = OtherIncomeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('income_list')
    categories = IncomeCategory.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'expense': None,
        'categories': categories,
        'funds': funds,}
    return render(request, 'other_income/income_form.html', context)

# Update income
def income_update(request, id):
    expense = get_object_or_404(OtherIncome, id=id)
    form = OtherIncomeForm(request.POST or None, instance=expense)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('income_list')
    categories = IncomeCategory.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'expense': expense,
        'categories': categories,
        'funds': funds,}
    return render(request, 'other_income/income_form.html', context)


# 4️⃣ Delete Expense
def income_delete(request, id):
    expense = get_object_or_404(OtherIncome, id=id)
    expense.delete()
    return redirect('income_list')


# -=====================================================   Supplier Payment Create  ===========================================
def payment_list(request):
    supplier = SupplierPayment.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    paginator = Paginator(supplier, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'supplier':supplier,
        }
    return render(request, 'supplier/payment_list.html', context)


def payment_create(request):
    form = SupplierPaymentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('supplier_payment_list')
    suppliers = Supplier.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'expense': None,
        'suppliers': suppliers,
        'funds': funds,}
    return render(request, 'supplier/payment_form.html', context)

def payment_update(request, id):
    payment = get_object_or_404(SupplierPayment, id=id)
    form = SupplierPaymentForm(request.POST or None, instance=payment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('supplier_payment_list')
    payments = SupplierPayment.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'payment': payment,
        'payments': payments,
        'funds': funds,}
    return render(request, 'supplier/payment_form.html', context)

# 4️⃣ Delete payment
def payment_delete(request, id):
    expense = get_object_or_404(SupplierPayment, id=id)
    expense.delete()
    return redirect('supplier_payment_list')



# -=====================================================   Customer Payment Create  ===========================================
def customer_payment_list(request):
    customer = CustomerPayment.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    paginator = Paginator(customer, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,}
    return render(request, 'customer/payment_list.html', context)


def customer_payment_create(request):
    form = CustomerPaymentForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('customer_payment_list')  
    customers = Customer.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'expense': None,
        'customers': customers,
        'funds': funds,}
    return render(request, 'customer/payment_form.html', context)


def customer_payment_update(request, id):
    payment = get_object_or_404(CustomerPayment, id=id)
    form = CustomerPaymentForm(request.POST or None, instance=payment)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('customer_payment_list')
    customers = Customer.objects.all()
    funds = Fund.objects.all()
    context = {
        'form': form,
        'payment': payment,
        'customers': customers,
        'funds': funds,}
    return render(request, 'customer/payment_form.html', context)


# 4️⃣ Delete payment
def customer_payment_delete(request, id):
    expense = get_object_or_404(CustomerPayment, id=id)
    expense.delete()
    return redirect('customer_payment_list')


# -=====================================================   Fund Transfer List  ===========================================

def fund_transfer_list(request):
    transfers = FundTransfer.objects.all().order_by('-id')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    paginator = Paginator(transfers, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,}
    return render(request, 'fund/fund_tran_list.html', context)


def fund_transfer_create(request):
    form = FundTransferForm(request.POST or None)
    funds = Fund.objects.filter(amount__gt=0)
    fund = Fund.objects.all()
    if request.method == 'POST' and form.is_valid():
        from_fund_id = request.POST.get('from_fund')
        to_fund_id = request.POST.get('to_fund')
        amount = form.cleaned_data['amount']
        date = form.cleaned_data['date']
        note = form.cleaned_data.get('note', '')
        # get Fund objects
        from_fund = get_object_or_404(Fund, pk=from_fund_id)
        to_fund = get_object_or_404(Fund, pk=to_fund_id)
        # Validate amount: can't transfer more than available
        if amount > from_fund.amount:
            messages.error(request, f"Cannot transfer {amount}. {from_fund.fund_name} only has {from_fund.amount}.")
            return redirect('fund_transfer_create')
        try:
            with transaction.atomic():
                # Create FundTransfer record
                transfer = FundTransfer.objects.create(
                    from_fund=from_fund,
                    to_fund=to_fund,
                    amount=amount,
                    date=date,
                    note=note,
                    created_by=request.user)
                # Update funds
                from_fund.amount -= amount
                from_fund.save()
                to_fund.amount += amount
                to_fund.save()
        except Exception as e:
            messages.error(request, f"Error: {str(e)}")
            return redirect('fund_transfer_create')
        messages.success(request, f"Transferred {amount} from {from_fund.fund_name} to {to_fund.fund_name}")
        return redirect('fund_transfer_list')
    context = {
        'form': form,
        'funds': funds,
        'fund': fund,
        'transfer': None,}
    return render(request, 'fund/fund_tran_form.html', context)


def fund_transfer_update(request, pk):
    transfer = get_object_or_404(FundTransfer, pk=pk)
    form = FundTransferForm(request.POST or None, instance=transfer)

    # List of available funds
    from_funds = Fund.objects.filter(Q(amount__gt=0) | Q(id=transfer.from_fund.id))
    to_funds = Fund.objects.all()

    if request.method == 'POST' and form.is_valid():
        from_fund_id = request.POST.get('from_fund')
        to_fund_id = request.POST.get('to_fund')
        amount = form.cleaned_data['amount']

        try:
            with transaction.atomic():
                # Step 1: Revert old transfer
                Fund.objects.filter(pk=transfer.from_fund.pk).update(
                    amount=F('amount') + transfer.amount
                )
                Fund.objects.filter(pk=transfer.to_fund.pk).update(
                    amount=F('amount') - transfer.amount
                )

                # Refresh fund instances after revert
                from_fund = get_object_or_404(Fund, pk=from_fund_id)
                to_fund = get_object_or_404(Fund, pk=to_fund_id)
                from_fund.refresh_from_db()
                to_fund.refresh_from_db()

                # Step 2: Validation
                if amount > from_fund.amount:
                    messages.error(
                        request,
                        f"{from_fund.fund_name} only has {from_fund.amount}"
                    )
                    return redirect('fund_transfer_update', pk=pk)

                # Step 3: Save updated transfer
                updated_transfer = form.save(commit=False)
                updated_transfer.from_fund = from_fund
                updated_transfer.to_fund = to_fund
                updated_transfer.save()
                updated_transfer.refresh_from_db()

                # Step 4: Apply new transfer safely
                Fund.objects.filter(pk=from_fund.pk).update(
                    amount=F('amount') - amount
                )
                Fund.objects.filter(pk=to_fund.pk).update(
                    amount=F('amount') + amount
                )

                # Refresh fund instances after update
                from_fund.refresh_from_db()
                to_fund.refresh_from_db()

        except Exception as e:
            messages.error(request, str(e))
            return redirect('fund_transfer_list')

        messages.success(request, "Fund Transfer updated successfully!")
        return redirect('fund_transfer_list')

    return render(request, 'fund/fund_tran_form.html', {
        'form': form,
        'funds': from_funds,
        'fund': to_funds,
        'transfer': transfer,
    })


def fund_transfer_delete(request, id):
    transfer = get_object_or_404(FundTransfer, id=id)
    transfer.delete()
    return redirect('fund_transfer_list')





# -------------------------------------------    Purchase Create    ------------------------------------------------------------

def purchase_list(request):
    per_page = int(request.GET.get('per_page', 10))  # ডিফল্ট 10
    page = request.GET.get('page', 1)
    purchases = Purchase.objects.all().order_by('-purchase_date')  # fresh queryset
    paginator = Paginator(purchases, per_page)
    purchase_item = PurchaseItem.objects.all()
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'purchase_item':purchase_item
    }
    return render(request, 'purchase/purchase_list.html', context)


def purchase_create(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        items_json = request.POST.get('purchase_items')
        if form.is_valid() and items_json:
            purchase = form.save(commit=False)
            purchase.created_by = request.user
            purchase.save()
            items = json.loads(items_json)
            for item in items:
                product = Product.objects.get(pk=item['product_id'])
                # Create PurchaseItem
                PurchaseItem.objects.create(
                    purchase=purchase,
                    product=product,
                    quantity=item['quantity'],
                    purchase_price=item['price']
                )
                # Update Stock
                stock, created = Stock.objects.get_or_create(product=product)
                stock.quantity += item['quantity']
                stock.save()
            # Update purchase total
            purchase.update_total_amount()
            messages.success(request, "Purchase created successfully!")
            return redirect('purchase_list')
        else:
            # Show validation errors
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f"{field}: {error}")
            if not items_json:
                messages.error(request, "No items were added to the purchase.")
    else:
        form = PurchaseForm()

    context = {
        'form': form,
        'purchase': None,
        'suppliers': Supplier.objects.all(),
        'categories': Category.objects.all(),
        'products': Product.objects.all(),
    }
    return render(request, 'purchase/purchase_form.html', context)


def purchase_update(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    PurchaseItemFormSet = modelformset_factory(PurchaseItem, form=PurchaseItemForm, extra=0, can_delete=True)
    if request.method == 'POST':
        form = PurchaseForm(request.POST, instance=purchase)
        formset = PurchaseItemFormSet(request.POST, queryset=purchase.items.all())
        if form.is_valid() and formset.is_valid():
            try:
                with transaction.atomic():
                    purchase = form.save()
                    # Keep track of old items
                    old_items = {item.pk: item for item in purchase.items.all()}
                    for item_form in formset:
                        if item_form.cleaned_data:
                            if item_form.cleaned_data.get('DELETE', False):
                                # DELETE item → reduce stock
                                if item_form.instance.pk:
                                    old_item = old_items.get(item_form.instance.pk)
                                    if old_item:
                                        stock = Stock.objects.get(product=old_item.product)
                                        stock.quantity -= old_item.quantity
                                        stock.save()
                                    item_form.instance.delete()
                            else:
                                # NEW or UPDATED item
                                item = item_form.save(commit=False)
                                item.purchase = purchase
                                # Stock adjust
                                if item.pk:  # existing item
                                    old_item = old_items.get(item.pk)
                                    delta_qty = item.quantity - old_item.quantity
                                    stock = Stock.objects.get(product=item.product)
                                    stock.quantity += delta_qty
                                    stock.save()
                                else:  # new item
                                    stock, created = Stock.objects.get_or_create(product=item.product)
                                    stock.quantity += item.quantity
                                    stock.save()

                                item.save()
                    # Update total
                    purchase.update_total_amount()
                    messages.success(request, "Purchase updated successfully!")
                    return redirect('purchase_list')
            except Exception as e:
                messages.error(request, f"Error updating purchase: {e}")

    else:
        form = PurchaseForm(instance=purchase)
        formset = PurchaseItemFormSet(queryset=purchase.items.all())

    context = {'form': form, 'formset': formset, 'purchase': purchase}
    return render(request, 'purchase/purchase_form.html', context)


# Delete Purchase
def purchase_delete(request, id):
    purchase = get_object_or_404(Purchase, id=id)
    purchase.delete()
    return redirect('purchase_list')



@transaction.atomic
def purchase_return(request):
    if request.method == 'POST':
        purchase_id = request.POST.get('purchase_id')
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        note = request.POST.get('note')
        purchase = get_object_or_404(Purchase, id=purchase_id)
        product = get_object_or_404(Product, id=product_id)
        stock = get_object_or_404(Stock, product=product)
        if quantity > stock.quantity:
            messages.error(request, "Return quantity exceeds available stock")
            return redirect('purchase_return')
        PurchaseReturn.objects.create(
            purchase=purchase,
            product=product,
            quantity=quantity,
            note=note,
            created_by=request.user
        )
        stock.quantity -= quantity
        stock.save()
        messages.success(request, "Purchase return successful")
        return redirect('purchase_list')
    context = {
        'purchases': Purchase.objects.all(),
        'products': Product.objects.select_related('stock'),
    }
    return render(request, 'purchase/purchase_return.html', context)


def purchase_return_list(request):
    per_page = int(request.GET.get('per_page', 10))  # ডিফল্ট 10
    page = request.GET.get('page', 1)
    qs = PurchaseReturn.objects.select_related(
        'purchase', 'product', 'created_by', 'purchase__supplier'
    ).order_by('-id')
    paginator = Paginator(qs, per_page)
    page_obj = paginator.get_page(page)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
    }
    return render(request, 'purchase/purchase_return_list.html', context)

# ===================================    Pending Order    =======================================================

    
def pending_order_list(request):
    per_page = int(request.GET.get('per_page', 10)) 
    page = request.GET.get('page', 1)
    orders_qs = Order.objects.filter(status='pending') \
        .prefetch_related('items') \
        .order_by('-id')  # fresh queryset
    paginator = Paginator(orders_qs, per_page)
    page_obj = paginator.get_page(page)
    settings = SystemSettings.objects.first()
    context = {
        'page_obj': page_obj,  # pagination object
        'per_page': per_page,
        'settings': settings,}
    return render(request, 'collect_order/pending_order.html', context)


    
def accept_order(request, order_id):
    order = Order.objects.get(id=order_id, status='pending')
    order.status = 'completed'
    order.save()
    messages.success(request, f"Order accepted successfully!")
    return redirect('pending_orders')  # redirect to sales report



# =================================================  Collect Order  ===========================================


def order_list(request, category_id=None):
    categories = Category.objects.all()
    funds = Fund.objects.all()

    if category_id:
        selected_category = get_object_or_404(Category, pk=category_id)
        products = Product.objects.filter(category=selected_category, stock__isnull=False, stock__quantity__gt=0)
    else:
        products = Product.objects.filter(stock__isnull=False, stock__quantity__gt=0)
        selected_category = None
    context = {
        'categories': categories,
        'products': products,
        'selected_category': selected_category,
        'funds': funds}
    return render(request, 'collect_order/order_list.html', context)


def create_collect_order(request):
    if request.method == 'POST':
        table = request.POST.get('table')
        order_type = request.POST.get('order_type')
        discount = Decimal(request.POST.get('discount') or 0)
        grand_total = Decimal(request.POST.get('grand_total') or 0)
        paid_amount = Decimal(request.POST.get('paid_amount') or 0)
        change_amount = Decimal(request.POST.get('change_amount') or 0)
        fund_id = request.POST.get('fund')

        if not table:
            messages.error(request, "Table is required!")
            return redirect('create_order')

        if Order.objects.filter(table=table, status='pending').exists():
            messages.error(request, f"Table {table} already has a pending order!")
            return redirect('create_order')

        items = json.loads(request.POST.get('order_items', '[]'))
        if not items:
            messages.error(request, "Add at least one product!")
            return redirect('create_order')

        fund = get_object_or_404(Fund, pk=fund_id) if fund_id else None

        try:
            with transaction.atomic():
                # Create Order
                order = Order.objects.create(
                    table=table,
                    order_type=order_type,
                    discount=discount,
                    grand_total=grand_total,
                    paid_amount=paid_amount,
                    change_amount=change_amount,
                    fund=fund,
                    status='pending'
                )

                # Create Order Items
                for item in items:
                    product = Product.objects.get(id=item['product_id'])
                    quantity = int(item['quantity'])
                    price = Decimal(item['price'])
                    amount = quantity * price

                    if product.stock.quantity < quantity:
                        raise ValueError(f"{product.name} not enough stock!")

                    OrderItem.objects.create(
                        order=order,
                        product_name=product.name,
                        quantity=quantity,
                        price=price,
                        amount=amount
                    )

                    # Reduce product stock
                    product.stock.quantity -= quantity
                    product.stock.save()

                # Update fund amount
                if fund:
                    print("Paid amount:", paid_amount, "Fund before:", fund.amount)
                    fund.amount += paid_amount
                    fund.save()
                    print("Fund after:", fund.amount)

        except Exception as e:
            messages.error(request, str(e))
            return redirect('create_order')

        messages.success(request, "Order created successfully and Fund updated!")
        return redirect('pending_orders')

    # GET request
    categories = Category.objects.all()
    products = Product.objects.filter(stock__isnull=False, stock__quantity__gt=0)
    funds = Fund.objects.all()
    return render(request, 'collect_order/order_list.html', {
        'categories': categories,
        'products': products,
        'funds': funds
    })
    
    

# ===============================   Sales Report =======================
def sales_report_list(request):
    orders = Order.objects.filter(status='completed').order_by('-created_at')
    per_page = request.GET.get('per_page', 10)
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10
    paginator = Paginator(orders, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # Total grand amount (all orders, not just page)
    total_grand = orders.aggregate(total=Sum('grand_total'))['total'] or 0
    settings = SystemSettings.objects.first()
    context = {
        'page_obj': page_obj,
        'per_page': per_page,
        'total_grand': total_grand,
        'settings': settings,}
    return render(request, 'stock/stock_list.html', context)
    
    
    
def purchase_report(request):
    purchases = Purchase.objects.prefetch_related('items', 'supplier').all().order_by('-purchase_date')
    per_page = request.GET.get('per_page')
    try:
        per_page = int(per_page)
        if per_page <= 0:
            per_page = 10
    except (TypeError, ValueError):
        per_page = 10
    paginator = Paginator(purchases, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'per_page': per_page,}
    return render(request, 'purchase/purchase_report.html', context)

