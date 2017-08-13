# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from forms import LoginForm, RegisterForm, CharacterForm, StaticForm, StaticAddMemberForm
from django.contrib.auth import authenticate, login
from decorators import login_required
from models import AlbionCharacter, Craft, PlayerCraft, Static
from django.contrib.auth.models import User
# Create your views here.
@login_required
def dashboard(request):
    context = {}
    if AlbionCharacter.objects.filter(user=request.user).count() > 0:
        context['character'] = AlbionCharacter.objects.get(user=request.user)
    return render(request, 'dashboard.html', context)

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            user = authenticate(username=request.POST['username'],
                    password = request.POST['password'])
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                return redirect('dashboard')
    else:
        form = LoginForm()

    return render(
            request,
            'login.html',
            context={
                'form': form,
                }
            )
def register_user(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                    request.POST['username'],
                    request.POST['email'],
                    request.POST['password'],
                    )
            user.save()
            print("Saved notification for user: " + user.username)
            return redirect('login')
    else:
        form = RegisterForm()

    return render(
            request,
            'register.html',
            context={}
            )
@login_required
def character_add(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = AlbionCharacter(
                    name=request.POST['name'],
                    role=request.POST['role'],
                    user=request.user
                    )
            character.save()
            return redirect('dashboard')
    else:
        form = CharacterForm()
    context = {}
    context['form'] = form
    return render(request, 'characters/character_add.html', context)

@login_required
def character_remove(request):
    pass
@login_required
def character_update(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = AlbionCharacter.objects.get(user=request.user)
            character.name = request.POST['name']
            character.role = request.POST['role']
            character.secondary = request.POST['secondary']
            character.discord = request.POST['discord']
            character.save()
            return redirect('dashboard')
    else:
        character = AlbionCharacter.objects.get(user=request.user)
        initial = {}
        initial['name'] = character.name
        initial['role'] = character.role
        initial['secondary'] = character.secondary
        initial['discord'] = character.discord
        form = CharacterForm(initial=initial)
    context = {}
    context['form'] = form
    return render(request, 'characters/character_update.html', context)

@login_required
def character_list(request):
    characters = AlbionCharacter.objects.all().order_by('-user__last_login', 'role')
    tanks = AlbionCharacter.objects.filter(role='Tank')
    healers = AlbionCharacter.objects.filter(role='Healer')
    ranged = AlbionCharacter.objects.filter(role='Ranged DPS')
    melee = AlbionCharacter.objects.filter(role='Melee DPS')
    dps = ranged | melee
    context = {}
    context['characters'] = characters
    context['tanks'] = tanks
    context['healers'] = healers
    context['dps'] = dps
    return render(request, 'characters/character_list.html', context)

@login_required
def craft_update(request):
    if request.method == 'POST':
        character = AlbionCharacter.objects.get(user=request.user)
        clear_playercrafts(character)
        for item in request.POST:
            try:
                playercraft = PlayerCraft(craft=Craft.objects.get(id=item),
                        tier=request.POST[item],
                        character=character)
                playercraft.save()
            except:
                pass
        return redirect('dashboard')
    context = {}
    t_data = []
    c_data = []
    buildings = ['Hunter', 'Mage', 'Warrior', 'Toolmaker']
    for building in buildings:
        crafts = Craft.objects.filter(building=building)
        for craft in crafts:
            playercrafts = PlayerCraft.objects.filter(craft__item=craft).all()
            c_data.append([craft, playercrafts])
        t_data.append([building, c_data])
        c_data = []
    # GET INITIAL CRAFTS
    playercrafts = PlayerCraft.objects.filter(character=AlbionCharacter.objects.get(user=request.user))
    print(playercrafts)
    context['playercrafts'] = playercrafts
    context['data'] = t_data
    return render(request, 'crafts/craft_update.html', context)
@login_required
def craft_list(request):
    context = {}
    t_data = []
    c_data = []
    buildings = ['Hunter', 'Mage', 'Warrior', 'Toolmaker']
    for building in buildings:
        crafts = Craft.objects.filter(building=building)
        for craft in crafts:
            playercrafts = PlayerCraft.objects.filter(craft__item=craft).all().order_by('-tier')[:5]
            c_data.append([craft, playercrafts])
        t_data.append([building, c_data])
        c_data = []
    context['data'] = t_data
    return render(request, 'crafts/craft_list.html', context)

@login_required
def policies(request):
    context = {}
    return render(request, 'policies.html', context)

@login_required
def statics(request):
    context = {}
    return render(request, 'groups/statics.html', context)

@login_required
def statics_add(request):
    if request.method == 'POST':
        form = StaticForm(request.POST)
        if form.is_valid():
            static = Static(
                    name=request.POST['name'],
                    description=request.POST['description'],
                    leader=AlbionCharacter.objects.get(user=request.user)
                    )
            static.save()
            static.members.add(static.leader)
            static.save()
            return redirect('static_view', pk=static.pk)
    else:
        form = StaticForm()
    context = {}
    context['form'] = form
    return render(request, 'groups/statics_add.html', context)

@login_required
def static_edit(request, pk):
    if request.method == 'POST':
        form = StaticForm(request.POST)
        if form.is_valid():
            static = Static.objects.get(pk=pk)
            static.name = request.POST['name']
            static.description = request.POST['description']
            static.save()
            return redirect('static_view', pk=static.pk)
    else:
        static = Static.objects.get(pk=pk)
        initial = {}
        initial['name'] = static.name
        initial['description'] = static.description
        form = StaticForm(initial=initial)
    context = {}
    context['form'] = form
    return render(request, 'groups/statics_add.html', context)

@login_required
def statics_delete(request):
    context = {}
    return render(request, 'groups/statics_remove.html', context)

@login_required
def statics_view(request):
    context = {}
    statics = Static.objects.all()
    context['statics'] = statics
    return render(request, 'groups/statics_view.html', context)

@login_required
def static_view(request, pk):
    context = {}
    context['static'] = Static.objects.get(pk=pk)
    return render(request, 'groups/static_view.html', context)

@login_required
def static_add_member(request, pk):
    if request.method == 'POST':
        form = StaticAddMemberForm(request.POST)
        if form.is_valid():
            static = Static.objects.get(pk=pk)
            character = AlbionCharacter.objects.get(name=request.POST['member'])
            static.members.add(character)
            static.save()
            return redirect('static_view', pk=static.pk)
    else:
        form = StaticAddMemberForm()
    context = {}
    context['form'] = form
    return render(request, 'groups/static_add_member.html', context)


@login_required
def clear_playercrafts(character):
    playercrafts = PlayerCraft.objects.filter(character=character)
    for playercraft in playercrafts:
        playercraft.delete()
    return True

