from django.contrib.auth.models import Group
from django.shortcuts import redirect, render

from accounts.forms import RegisterForm
from accounts.models import UserProfile


def register(request):
    register_form = RegisterForm(request.POST or None)

    if register_form.is_valid():
        user = register_form.save(commit=False)
        user.is_staff = True
        user.save()
        group = Group.objects.get(name='service_provider')
        user.groups.add(group)
        UserProfile.objects.create(user=user)
        return redirect('admin:login')

    return render(request, 'accounts/register.html', {'form': register_form})


def detail(request, pk):
    user = UserProfile.objects.get(pk=pk)
    return render(request, 'accounts/detail.html', {'user': user})
