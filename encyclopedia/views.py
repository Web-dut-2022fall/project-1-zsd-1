from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

from . import util
import secrets
import markdown


@csrf_protect
def index(request):

	if request.method == "POST":

		if 'q' in request.POST:
			search = request.POST['q']
			entry = util.get_entry(search)
			custom_result = []
			flag = False

			# If no specific result
			if entry is None:

				# Get all entries
				entries = util.list_entries()

				# Look for substring potential match
				for entry in entries:
					entry_low  = entry.lower()

					index = entry_low.find(search.lower())
					if index != -1:
						custom_result.append(entry)
						flag = True

				# If there's a positive match
				if flag == True:
					return render(request, "encyclopedia/index.html", {
			        "entries": custom_result, "title": "Result(s) for " + search
			    	})

				# If not even a substring match, return zero
				return render(request, "encyclopedia/index.html", {
			        "entry": "This page does not exist.", "title": "No Result for " + search
			    })
			else:
				return render(request, "encyclopedia/single.html", {"entry": entry, "title": search})


		elif 'content' in request.POST:
			title = request.POST['title']
			content = request.POST['content']

			#check if title already exist
			is_existing = util.get_entry(title)

			#If entry does not already exist, create it
			if is_existing is None:
				util.save_entry(title, content)
				messages.add_message(request, messages.SUCCESS, 'Entry created!')
				return render(request, "encyclopedia/index.html", { "entries": util.list_entries(), "title": "All Pages"})
			else:
				#If entry already exists, warn user and show existing page for editing
				messages.add_message(request, messages.WARNING, title + ' Entry already exist!')
				return redirect('view_entry', title = title)
				#return render(request, "encyclopedia/single.html", { "entry": is_existing, "title": title})

	if request.method == "GET":
		return render(request, "encyclopedia/index.html", { "entries": util.list_entries(), "title": "All Pages"})


def view_entry(request, title):
	entry = util.get_entry(title)

	if entry is None:
		return render(request, "encyclopedia/single.html", {"entry": "This page does not exist.", "title": "No result"})
	else:

		md = markdown.Markdown()
		entry = md.convert(entry)
		return render(request, "encyclopedia/single.html", {"entry": entry, "title": title})


@csrf_protect
def create_entry(request):	
	return render(request, "encyclopedia/create_entry.html", {'title': '', 'content': ''})


def edit_entry(request, title):

	if request.method == "GET":
		entry = util.get_entry(title)
		return render(request, "encyclopedia/create_entry.html", {'title': title, 'content': entry})

	if request.method == "POST":

		if 'content' in request.POST:
			title = request.POST['title']
			content = request.POST['content']

			#save the entry
			util.save_entry(title, content)

			messages.add_message(request, messages.SUCCESS, title + ' successfully updated')
			return redirect('view_entry', title = title)
	

def random(request):

	all_entries = util.list_entries()
	random_entry = secrets.choice(all_entries)

	messages.add_message(request, messages.SUCCESS, 'Here\'s a random result.')
	return redirect('view_entry', title = random_entry)
	



