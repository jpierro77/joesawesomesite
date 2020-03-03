from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import redirect, render
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from .models import MasterItem, MasterList, PersonalList
from .forms import Item, ListDetails
import json
import base64
import tweepy
import os
import sys

# Create your views here.


def index(request):
    return render(request, 'itemranker/index.html')


def twitterpost(request):

    print(request)
    # make sure to get image from post
    if request.method == 'POST':
        try:
            image_data = request.POST['imgBase64']
            format, imgstr = image_data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr))
            fs = FileSystemStorage()
            fs._location = settings.TWITTERPOST_URL
            file = request.user.username+"twitter_image."+ext
            request.session['imgBase64'] = fs.save(file, data)

        except:
            print("Oops!", sys.exc_info()[1], "occured.")
        try:
            image = os.path.join(settings.TWITTERPOST_URL,
                                 request.session['imgBase64'])
            access_token = request.session['access_token']
            auth = tweepy.OAuthHandler(settings.TWITTER_ACCESS_KEY,
                                       settings.TWITTER_ACCESS_SECRET)
            auth.set_access_token(access_token[0], access_token[1])

            api = tweepy.API(auth)

            api.update_with_media(image, "")
            fs = FileSystemStorage()
            fs._location = settings.TWITTERPOST_URL
            fs.delete(os.path.join(settings.TWITTERPOST_URL,
                                   request.session['imgBase64']))
            data = {
                "url_type": "twitter_profile_redirect",
                "url": "https://www.twitter.com/"+api.me().screen_name
            }
            return JsonResponse(data)
        except:
            auth = tweepy.OAuthHandler(settings.TWITTER_ACCESS_KEY,
                                       settings.TWITTER_ACCESS_SECRET,
                                       settings.TWITTER_CALLBACK_URL)
            authorization_url = auth.get_authorization_url()

            request.session['oauth_token'] = auth.request_token['oauth_token']
            request.session['oauth_token_secret'] = auth.request_token['oauth_token_secret']
            data = {
                'url': authorization_url,
                'url_type': 'auth_url_redirect'
            }
            return JsonResponse(data)


# callback update
def callback(request):
    image = os.path.join(settings.TWITTERPOST_URL,
                         request.session['imgBase64'])
    print(image)
    oauth_token = request.GET.get('oauth_token')
    oauth_token_secret = request.session["oauth_token_secret"]
    oauth_verifier = request.GET.get('oauth_verifier')

    auth = tweepy.OAuthHandler(settings.TWITTER_ACCESS_KEY,
                               settings.TWITTER_ACCESS_SECRET)
    print(auth.__str__())

    auth.get_authorization_url()
    auth.request_token['oauth_token'] = oauth_token
    auth.request_token['oauth_token_secret'] = oauth_token_secret

    try:
        request.session['access_token'] = auth.get_access_token(oauth_verifier)
    except tweepy.TweepError:
        print('Error! Failed to get access token.')
        return HttpResponse("<h1>Failed to log in</h1>")

    api = tweepy.API(auth)

    api.update_with_media(image, "")
    fs = FileSystemStorage()
    fs._location = settings.TWITTERPOST_URL
    fs.delete(request.session['imgBase64'])
    print(api.me().screen_name)
    data = {
        "url_type": "twitter_profile_redirect",
        "url": "https://www.twitter.com/" + api.me().screen_name
    }
    return redirect(data['url'])


def savelist(request):
    valid_forms = True
    if request.user.is_authenticated:
        if 'save_data' in request.session:
            list_data = request.session['save_data']
            del request.session['save_data']
        else:
            list_data = (json.loads(request.POST['save_data']))

        list_info_form = ListDetails(
            {'list_title': list_data['list_title'],
             'list_type': list_data['list_type']})

        if not list_info_form.is_valid():
            valid_forms = False

        if valid_forms:
            list_data_array = list_data['list']
            for i in range(0, len(list_data_array)):
                print(list_data_array[i])
                item_form = Item(
                    {'rank': list_data_array[i]['rank'],
                     'item_name': list_data_array[i]['item_name'],
                     'votes': list_data_array[i]['votes']})
                print(item_form.is_valid())
                if not item_form.is_valid():
                    valid_forms = False
                    break
        if valid_forms:
            if list_data["list_type"] == "master":
                rank_list = MasterList()
                rank_list.list_name = list_data['list_title']
                rank_list.user = request.user
                rank_list.save()
                for i in range(0, len(list_data_array)):
                    master_item = MasterItem()
                    master_item.item_name = list_data_array[i]['item_name']
                    master_item.votes = 0
                    master_item.master_list = rank_list
                    master_item.save()

            elif list_data['list_type'] == "personal":
                rank_list = PersonalList()
                rank_list.list_name = list_data['list_title']
                rank_list.user = request.user
                rank_list.list_json = json.dumps(list_data_array)
                rank_list.save()

            print(str(rank_list.list_id))
            data = {
                'was_saved': True,
                'redirect_type': 'list_display',
                'redirect_url': list_data['list_type'] +
                                 "list/" +
                                 str(rank_list.list_id),
                'valid_forms': valid_forms
            }
            return JsonResponse(data)
        else:
            data = {
                'was_saved': False,
                'redirect_type': 'none',
                'redirect_url': '',
                'valid_forms': ''
            }
    else:
        request.session["save_data"] = (json.loads(request.POST['save_data']))
        data = {
            'was_saved': False,
            'redirect_type': 'login',
            'redirect_url': "../users/login",
            'valid_forms': False
        }
        return JsonResponse(data)


def personal_list_display(request, list_id_arg=0):
    if list_id_arg > 0:
        personal_list = PersonalList.objects.filter(list_id=list_id_arg).first()
        if personal_list is not None:
            return render(request, 'itemranker/listbase.html', {
                'list_name': personal_list.list_name,
                'list_type': 'personal',
                'list_author': personal_list.user.username,
                'list': json.loads(personal_list.list_json)
                })
        else:
            raise Http404("List Does Not Exist")
    else:
        return redirect('itemranker')


def master_list_display(request, list_id_arg=0):
    if list_id_arg > 0:
            master_list = MasterList.objects.filter(list_id=list_id_arg).first()
            if master_list is not None:
                master_list_sorted = list(MasterItem.objects.filter(master_list=master_list))
                for i in range(0, len(master_list_sorted)-1):
                    swapped = False
                    for j in range(0, len(master_list_sorted)-i-1):
                        if master_list_sorted[j].votes < master_list_sorted[j+1].votes:
                            swapped = True
                            temp = master_list_sorted[j]
                            master_list_sorted[j] = master_list_sorted[j+1]
                            master_list_sorted[j+1] = temp

                    if not swapped:
                        break
                return render(request, 'itemranker/listbase.html', {
                    'list_type': 'master',
                    'list_name': master_list.list_name,
                    'list_author': master_list.user.username,
                    'list_id': master_list.list_id,
                    'list': master_list_sorted
                })
            else:
                raise Http404("List Does Not Exist")
    else:
        return redirect('itemranker')


def add_vote(request, item_id=0, master_list_id=0):
    if item_id > 0 and master_list_id > 0:
        master_item = MasterItem.objects.filter(id=item_id).first()
        master_item.add_vote()
        master_item.save()
        return redirect('master_list_display', master_list_id)


def add_item(request, master_list_id=0):
    if master_list_id > 0:
        master_list = MasterList.objects.filter(list_id=master_list_id).first()
        item_name = request.POST['item_name']
        item = Item({'item_name': item_name, 'votes': 1})
        if item.is_valid():
            master_item = MasterItem()
            master_item.item_name = item_name
            master_item.master_list = master_list
            master_item.votes = 1
            master_item.save()

    return redirect('master_list_display', master_list_id)


def delete_ranklist(request):
    rank_list_ids = list(request.POST)[1:]
    print(rank_list_ids)
    for rank_list_id in rank_list_ids:
        type_and_id = rank_list_id.split(' ')
        print(type_and_id)
        if type_and_id[0] == "personal":
            PersonalList.objects.filter(list_id=type_and_id[1]).delete()
        elif type_and_id[0] == "master":
            MasterList.objects.filter(list_id=type_and_id[1]).delete()
    return redirect("edit_profile")