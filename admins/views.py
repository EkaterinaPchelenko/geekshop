from django.contrib.auth.decorators import user_passes_test
from django.db import connection
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from admins.forms import UserAdminRegisterForm, UserAdminProfileForm, CategoryEditForm, ProductEditForm
from users.models import User
from mainapp.models import Product, ProductCategory


def index(request):
    return render(request, 'admins/admin.html')

class UserListView(ListView):
    model = User
    template_name = 'admins/admin-users-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Пользователи'
        return context

class UserCreateView(CreateView):
    model = User
    template_name = 'admins/admin-users-create.html'
    form_class = UserAdminRegisterForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Регистрация'
        return context

class UserUpdateView(UpdateView):
    model = User
    template_name = 'admins/admin-users-update-delete.html'
    form_class = UserAdminProfileForm
    success_url = reverse_lazy('admins:admins_user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление пользователя'
        return context


class UserDeleteView(DeleteView):
    model = User
    template_name = 'admins/admin-users-read.html'
    success_url = reverse_lazy('admins:admins_user')

    @method_decorator(user_passes_test(lambda u:u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(UserDeleteView, self).dispatch(request,*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView):
    model = ProductCategory
    template_name = 'admins/admin-categories-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        return context


class CategoryCreateView(CreateView):
    model = ProductCategory
    template_name = 'admins/admin-categories-create.html'
    form_class = CategoryEditForm
    success_url = reverse_lazy('admins:admins_category')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание категории'
        return context


def db_profile_by_type(prefix, type, queries):
    update_queries = list(filter(lambda x: type in x['sql'], queries))
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


class CategoryUpdateView(UpdateView):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    form_class = CategoryEditForm
    context_object_name = 'category'
    success_url = reverse_lazy('admins:admins_category')

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                print(f'Применяется скидка {discount} % к товарам категории {self.object.name}')
                self.object.product_set.update(price=F('price')*(1-discount/100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(CategoryUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление категории'
        return context


class CategoryDeleteView(DeleteView):
    model = ProductCategory
    template_name = 'admins/admin-categories-update-delete.html'
    success_url = reverse_lazy('admins:admins_category')

    @method_decorator(user_passes_test(lambda u:u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(request,*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # ProductCategory.objects.filter(id=self.object.id).delete()
        self.object.product_set.update(is_active=False)
        self.object.is_active = False
        self.object.save()

        # category = ProductCategory.objects.all()
        # context = {'object_list': category}
        # result = render_to_string('admins/admin-categories-update-delete.html', context, request=request)
        #
        # return JsonResponse({'result': result})
        return HttpResponseRedirect(self.get_success_url())


class ProductListView(ListView):
    model = Product
    template_name = 'admins/admin-products-read.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Категории'
        return context


class ProductCreateView(CreateView):
    model = ProductCategory
    template_name = 'admins/admin-products-create.html'
    form_class = ProductEditForm
    success_url = reverse_lazy('admins:admins_product')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductCreateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Создание продукта'
        return context


class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    form_class = ProductEditForm
    context_object_name = 'product'
    success_url = reverse_lazy('admins:admins_product')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductUpdateView, self).get_context_data(**kwargs)
        context['title'] = 'Админка | Обновление продукта'
        return context


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'admins/admin-products-update-delete.html'
    success_url = reverse_lazy('admins:admins_product')

    @method_decorator(user_passes_test(lambda u:u.is_superuser))
    def dispatch(self, request, *args, **kwargs):
        return super(ProductDeleteView, self).dispatch(request,*args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        # Product.objects.filter(id=self.object.id).delete()
        self.object.is_active = False
        self.object.save()

        # product = ProductCategory.objects.all()
        # context = {'object_list': product}
        # result = render_to_string('admins/admin-products-read.html', context, request=request)

        # return JsonResponse({'result': result})
        return HttpResponseRedirect(self.get_success_url())