from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db.models import Count, Q
from datetime import timedelta, date
from django.http import QueryDict
from django.contrib import messages
from django.urls import reverse
from datetime import date
from .models import Abitudine, LogAbitudine
from .forms import AbitudineForm
from .forms import AbitudineForm, ModificaAbitudineForm


@login_required
def dashboard(request):
    #Gestisci la data selezionata (default: oggi)
    data_selezionata_str = request.GET.get('data')
    if data_selezionata_str:
        try:
            data_selezionata = date.fromisoformat(data_selezionata_str)
        except ValueError:
            data_selezionata = timezone.localdate()
    else:
        data_selezionata = timezone.localdate()
    
    oggi = timezone.localdate()  # per confronti UI
    abitudini = Abitudine.objects.filter(proprietario=request.user)

    # Dati per la data selezionata (toggle)
    dati_giorno = []
    for ab in abitudini:
        log = LogAbitudine.objects.filter(abitudine=ab, data=data_selezionata).first()
        dati_giorno.append({
            'abitudine': ab,
            'completata': log.completata if log else False,
            'log_id': log.id if log else None
        })
    
    completate_giorno = sum(1 for item in dati_giorno if item['completata'])

    # Grafico: ultimi 7 giorni ENDING alla data selezionata
    giorni_indietro = [(data_selezionata - timedelta(days=i)) for i in range(6, -1, -1)]
    etichette = [g.strftime('%a %d/%m') for g in giorni_indietro]  # es: "Lun 12/05"
    
    dati_grafico = []
    for giorno in giorni_indietro:
        totale = abitudini.count()
        completate = LogAbitudine.objects.filter(
            abitudine__in=abitudini,
            data=giorno,
            completata=True
        ).count()
        percentuale = round((completate / totale * 100), 0) if totale > 0 else 0
        dati_grafico.append(int(percentuale))

    # Streak: conta giorni consecutivi COMPLETATI al 100% fino alla data selezionata
    streak = 0
    for g in reversed(giorni_indietro):  # dal più vecchio al più recente
        tot = abitudini.count()
        if tot == 0:
            break
        comp = LogAbitudine.objects.filter(
            abitudine__in=abitudini, 
            data=g, 
            completata=True
        ).count()
        if comp == tot:
            streak += 1
        else:
            break  

    context = {
        'dati_oggi': dati_giorno,  
        'data_selezionata': data_selezionata,
        'oggi': oggi,
        'etichette_grafico': etichette,
        'dati_grafico': dati_grafico,
        'streak': streak,
        'completate_giorno': completate_giorno,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
@require_POST
def toggle_abitudine(request, abitudine_id):
    abitudine = get_object_or_404(Abitudine, id=abitudine_id, proprietario=request.user)
    
    #  Leggi la data dal POST
    data_str = request.POST.get('data')
    if data_str:
        try:
            data_target = date.fromisoformat(data_str)
        except ValueError:
            data_target = timezone.localdate()
    else:
        data_target = timezone.localdate()
        
    #  Toggle log
    log, _ = LogAbitudine.objects.get_or_create(abitudine=abitudine, data=data_target)
    log.completata = not log.completata
    log.save()
    
    # Messaggio con la data ESATTA modificata
    messages.success(request, f"✅ {abitudine.nome} aggiornata per il {data_target.strftime('%d/%m/%Y')}")
    
    # Redirect pulito con reverse()
    return redirect(f"{reverse('dashboard')}?data={data_target.isoformat()}")


def aggiungi_abitudine(request):
    form = AbitudineForm(request.POST)
    if form.is_valid():
        abitudine = form.save(commit=False)
        abitudine.proprietario = request.user
        abitudine.save()
        messages.success(request, f"✅ Abitudine '{abitudine.nome}' aggiunta!")
    else:
        messages.error(request, "❌ Nome non valido o già esistente.")
    return redirect('dashboard')

@login_required
@require_POST
def elimina_abitudine(request, abitudine_id):
    abitudine = get_object_or_404(Abitudine, id=abitudine_id, proprietario=request.user)
    nome = abitudine.nome
    abitudine.delete()
    messages.success(request, f"🗑️ '{nome}' eliminata.")
    return redirect('dashboard')


@login_required
def modifica_abitudine(request, abitudine_id):
    abitudine = get_object_or_404(Abitudine, id=abitudine_id, proprietario=request.user)

    if request.method == 'POST':
        form = ModificaAbitudineForm(request.POST, instance=abitudine)
        if form.is_valid():
            form.save()
            messages.success(request, f"✏️ Abitudine rinominata in '{abitudine.nome}'.")
            return redirect('dashboard')
    else:
        form = ModificaAbitudineForm(instance=abitudine)

    return render(request, 'tracker/modifica_abitudine.html', {
        'form': form,
        'abitudine': abitudine,
    })