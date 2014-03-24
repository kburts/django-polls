from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.utils import timezone
from django.views import generic
from django.views.generic.edit import CreateView
from django.forms.formsets import formset_factory

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from polls.models import Choice, Poll
from polls.forms import MakePoll, UserForm, UserProfileForm, MakeChoices, ChoiceForm


class About(generic.TemplateView):
    template_name = 'polls/about.html'

    def get_context_data(self, **kwargs):
        context = super(About, self).get_context_data(**kwargs)
        return context

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_poll_list'

    def get_queryset(self):
        """Return the last five published polls."""
        return Poll.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

def UserView(request, user):
    context = RequestContext(request)
    context_dict = {'user': user}

    # why does only user__username work?? NO IDEA but it took me an hour to figure it out.
    user_polls_list = Poll.objects.filter(user__username = user).order_by('-pub_date')[:5]
    #user_polls_list = Poll.objects.values_list('id', flat=True)
    context_dict['polls'] = user_polls_list

    return render_to_response('polls/user.html', context_dict, context)

#class UserView(generic.ListView):
#    template_name = 'polls/user.html'
#    context_object_name = 'latest_user_poll_list'

#    def get_queryset(self):
#        """Return the last five published polls."""
#        return Poll.objects.filter(
#            pub_date__lte=timezone.now(),
#        ).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Poll
    template_name = 'polls/detail.html'
    def get_queryset(self):
        """
        Excludes any polls that aren't published yet.
        """
        return Poll.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Poll
    template_name = 'polls/results.html'
   
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))

def MakePollView(request):
    if request.method == 'POST': # If the form has been submitted...
        form = MakePoll(request.POST) # A form bound to the POST data
        #choiceform = ChoiceForm(request.POST)
        MakeChoicesFormSet = formset_factory(ChoiceForm,extra=2)

        choiceformset = MakeChoicesFormSet()
	#choiceformset = formset(MakeChoices, extra=2)
	if (form.is_valid):# and choiceformset.is_valid()):
            #print form.cleaned_data
            new_instance = form.save(commit=False)
            if request.user.is_authenticated():
                new_instance.user = request.user
	
	    #choiceformset.errors          
	    print choiceformset.is_valid()
	    choiceformset.errors
	    print 'passed section with possible errors'
	    choices = []
	    for choice in choiceformset:
	        print choice.save(commit=False)
		print 'SAVED A CHOICE'
		choices.append(choice)
	    print choices
	    for c in choices:
		print c.choice_text
#	    for question in choiceformset:
#		print question
	    new_instance.save()

            #choice0 = Choice.objects.create(poll = Poll.objects.get(id = new_instance.id), choice_text = form.cleaned_data.get('choice'))

            #choice0.save()

            return HttpResponseRedirect('/polls/') # Redirect after POST
    else:
        form = MakePoll() # An unbound form
        choiceformset = formset_factory(ChoiceForm, extra=2)
 
    return render(request, 'polls/makepoll.html', {
        'form': form,
        'choiceformset': choiceformset,
        }
    )
'''
def MakeChoicesView(request, poll_id):
    if request.method == 'POST':
        form = MakeChoices(request.POST, poll_id)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/polls/') # Redirect after POST
    else:
        form = MakeChoices() # An unbound form

    return render(request, 'polls/makepoll.html', {
        'form': form,
    })
'''
def register(request):
    # Like before, get the request's context.
    context = RequestContext(request)

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            'polls/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

def user_login(request):
    # Like before, obtain the context for the user's request.
    context = RequestContext(request)

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
        username = request.POST['username']
        password = request.POST['password']

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user is not None:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/polls/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render_to_response('polls/login.html', {}, context)

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/polls/')

@login_required
def restricted(request):
    return render_to_response('polls/restricted.html')
