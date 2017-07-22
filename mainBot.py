import requests
import urllib
import sys
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
from termcolor import colored


# Global lists with all the default values
APP_ACCESS_TOKEN = '5760389131.2fa8e0f.b6ce40a40a64496198a65301d27fb6d4'
BASE_URL = 'https://api.instagram.com/v1/'
SANDBOX_USERS = ['_aeesha12', 'anisha_lamichhane', 'annie.one', 'jerry_jay97','_poppy9090', 'aakankshat01']
BUSINESS_KEYWORDS = ['Makeup', 'Lipstick', 'Kohl', 'Eyeliner', 'Nailpolish', 'Foundation', 'Sunscreen']
BRAND_NAMES = ['Lakme', 'Maybelline', 'Faces', 'Revlon', 'Lotus']
LOCATION_NAMES = ['Delhi', 'Dehradun','Dehra Dun', 'Jaipur']

'''
Function declaration to get your own info 
'''
def self_info():
    request_url = (BASE_URL + 'users/self/?access_token=%s') % APP_ACCESS_TOKEN
    user_details = requests.get(request_url).json()
    if user_details['meta']['code'] == 200:
        if len(user_details['data']):
            print 'Username: %s' % (user_details['data']['username'])
            print 'No. of followers: %s' % (user_details['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_details['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_details['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'

'''
Function declaration to get some other user's information
'''

def user_info(username):
    user_id = get_user_id(username)
    if user_id is not None:
        request_url = (BASE_URL + 'users/%s/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        user_details = requests.get(request_url).json()
        if user_details['meta']['code'] == 200:
            if len(user_details['data']):
                print 'Username: %s' % (user_details['data']['username'])
                print 'No. of followers: %s' % (user_details['data']['counts']['followed_by'])
                print 'No. of people you are following: %s' % (user_details['data']['counts']['follows'])
                print 'No. of posts: %s' % (user_details['data']['counts']['media'])
            else:
                print 'User does not exist!'
        else:
            print 'Status code other than 200 received! Cannot proceed further'


'''
Function to obtain the user id of a user
'''

def get_user_id(username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (username, APP_ACCESS_TOKEN)
    user_details = requests.get(request_url).json()
    if user_details['meta']['code'] == 200:
        if len(user_details['data']):
            return user_details['data'][0]['id']
        else:
            print "\nSorry but the user you're searching could not be found.\n"
            return None
    else:
        print 'Status code other than 200 received! Cannot proceed further'

'''
Function user to download self's recent post
'''
def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % APP_ACCESS_TOKEN
    own_media = requests.get(request_url).json()
    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            download_post(own_media['data'][0]['id'], own_media['data'])
            print "The post was downloaded successfully!"
        else:
            print 'Post does not exist!'
    else:
        print 'Status code other than 200 received!'


'''
Function to download the recent media liked by the user
'''
def get_recent_media_liked():
    request_url = (BASE_URL + 'users/self/media/liked?access_%s') % (APP_ACCESS_TOKEN)
    media_info = requests.get(request_url).json()
    if media_info['meta']['code'] == 200:
        if len(media_info['data']):
            print "Recent media liked by the user: "
            print "Caption: %s" % (media_info['data'][0]['caption']['text'])
            print "Total likes: %s" % (media_info['data'][0]['likes']['count'])
            print "Total comments: %s" % (media_info['data'][0]['comments']['count'])
            download_post(media_info['data'][0]['id'], media_info['data'])
            print "The post was downloaded successfully!"
    else:
        print "Post does not exist!"

'''
Function to obtain the media id of a post
'''
def get_media_id(ig_username):
    user_id = get_user_id(ig_username)
    if user_id is not None:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        media_info = requests.get(request_url).json()
        if media_info['meta']['code'] == 200:
            if len(media_info['data']):
                return media_info['data'][0]['id']
        else:
            print "Status code other than 200 received!"
            return None
    else:
        return None

'''
Function to like the recent post of given user
'''
def generate_like(username):
    media_id = get_media_id(username)
    if media_id is not None:
        request_url = (BASE_URL + 'media/%s/likes') % (media_id)
        payload = {'access_token': APP_ACCESS_TOKEN}
        like_generated = requests.post(request_url, payload).json()
        if like_generated['meta']['code'] == 200:
            print "You've successfully liked the post!"
        else:
            print "Sorry! There was an error liking the post."
    else:
        return


'''
Function used to obtain the list of comments on the recent post of a user
'''
def extract_comment_list(username):
    media_id = get_media_id(username)
    if media_id is not None:
        request_url = (BASE_URL + 'media/%s/comments?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
        print request_url
        comments_info = requests.get(request_url).json()
        if comments_info['meta']['code'] == 200:
            if len(comments_info['data']):
                comments_list = []
                for index in range(len(comments_info['data'])):
                    comment_dict = {comments_info['data'][index]['id']: comments_info['data'][index]['text']}
                    comments_list.append(comment_dict)
                return comments_list
            else:
                print "There are no comments!"
        else:
            print "Status code other than 200 received"
    else:
        return

'''
Function used to comment of the recengt post of a user. It takes variable number of arguements
In case of promoting business, the text to comment is obtained from another function
'''
def post_comment(**kwargs):
    media_id = get_media_id(kwargs['ig_username'])
    if media_id is not None:
        request_url = (BASE_URL + 'media/%s/comments') % media_id
        if len(kwargs) == 1:
            comment_text = raw_input("Enter your comment: ")
        else:
            comment_text = kwargs['text']

        payload = {'access_token': APP_ACCESS_TOKEN, 'text': comment_text}
        spawn_comment = requests.post(request_url, payload).json()
        if spawn_comment['meta']['code'] == 200:
            print "Your comment was posted successfully! "
        else:
            print "Sorry, your comment couldn't be posted."
    else:
        "There was an error posting your comment.. Returning to main menu"

'''
This function is used to check if the post is valid for business commenting
It returns a dictionary containing the business keyword to be focused on
'''
def is_valid_post(ig_user):
    user_id = get_user_id(ig_user)
    if user_id is not None:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        user_post = requests.get(request_url).json()
        if user_post['meta']['code'] == 200 and (len(user_post['data'])):
            caption__word_list = user_post['data'][0]['caption']['text'].split()
            for word in caption__word_list:
                if word in BUSINESS_KEYWORDS or word in BRAND_NAMES:
                    return {'captionWord': word.title()}
                elif word in LOCATION_NAMES:
                    return {'location': word.title()}
                else:
                    continue

            if user_post['data'][0]['location'] is not None:
                location_name_list = user_post['data'][0]['location']['name'].split(',')
                for place in location_name_list:
                    if place in LOCATION_NAMES:
                        return {'location': place.title()}

            if len(user_post['data'][0]['tags']):
                tags_list = user_post['data'][0]['tags']
                for tag in tags_list:
                    tag = tag.title()
                    if tag in BUSINESS_KEYWORDS or tag in BRAND_NAMES:
                        return {'tag': tag}
                    elif tag in LOCATION_NAMES:
                        return {'location': tag}
                    else:
                        return {}
            else:
                return {}
        else:
            return None


'''
This function is used to choose the best comment to be posted on a business relevant post
'''
def post_comment_by_criteria(post_response_dict):
    message = ''
    for key in post_response_dict:
        if key == 'captionWord':
            if post_response_dict['captionWord'] in BUSINESS_KEYWORDS:
                message = "We are glad to find another makeup-enthusiast!" \
                          "Don't forget to check out our online store for a vast and colorful variety of products!"
            elif post_response_dict['captionWord'] in BRAND_NAMES:
                message = "Amazing choice! Get the latest %s products only on GLOW-QUEEN" \
                          % (post_response_dict['captionWord'])
        elif key == 'location':
            if post_response_dict['location'] == 'Delhi':
                message = "We hope you enjoy your stay at Delhi! GLOW-QUEEN would love to have you over" \
                          "in our makeup infested store located in The Ambience Mall, Vasant Kunj\"" \
                          ":) Hope to see you there! "
            elif post_response_dict['location'] == 'Dehradun' or post_response_dict['location'] == 'Dehra Dun':
                message = "Beautiful city, Doon! :) GLOW-QUEEN welcomes you to the beauty-store in Rajpur Road!" \
                          " Hope to see you there!"
            elif post_response_dict['location'] == 'Jaipur':
                message = "Beat the humidity in Jaipur with the best beauty products available at" \
                          "GLOW-QUEEN in Pink Square Mall"
        elif key == 'tag':
            if post_response_dict['tag'] in BUSINESS_KEYWORDS:
                message = "Find the best beauty products at GLOW-QUEEN with exciting discounts. "
            elif post_response_dict['tag'] in BRAND_NAMES:
                message = "Offer exclusively for you! Get minimum 40 percent off on purchase of %s products from" \
                          " GLOW-QUEEN, our online beauty store. " % post_response_dict['tag']
        return message

'''
Function used to create the final comment to be posted
'''
def promote_to_user(user, site_url):
    post_response_dict = is_valid_post(user)
    if post_response_dict is None:
        print "Sorry, user %s 's account is either private or there are no posts shared" % user
        return
    if len(post_response_dict) == 0:
        print "Your customer %s has no valid post to promote your business on." % (user)
        return
    else:
        comment_text = post_comment_by_criteria(post_response_dict)
        final_comment = comment_text + " Link: %s" % site_url
        print "Your final comment to be posted is: %s" % final_comment
        post_comment(ig_username=user, text=final_comment)


'''
This function takes gthe site url of the business and calls other functions
to perform valid commenting
'''
def promote_business():
    valid_choices = [1, 2]
    while True:
        user_choice = raw_input("Would you like to promote your business to\n" \
                                "1. All your contacts\n2. Only one contact\nYour choice: ")
        if len(user_choice) == 0:
            print "Invalid"
        else:
            user_choice = int(user_choice)
            if user_choice in valid_choices:
                break
            else:
                print "Invalid"
                continue

    while True:
        site_url = raw_input("Enter the valid url of your website: ")
        if len(site_url) == 0:
            print "Invalid"
        else:
            break

    if  user_choice == 1:
        for user in SANDBOX_USERS:
            promote_to_user(user, site_url)
        return
    elif user_choice == 2:
        user = raw_input("Enter the name of the user to whom you want to promote your business: ")
        promote_to_user(user, site_url)
        return

'''
Function used to input the username 
'''

def input_username():
    return raw_input("Enter the username: ")


'''
Function used to download any media be it image or video
'''
def download_post(media_id, user_posts):
    for e in user_posts:
        if media_id == e['id']:
            if e['type'] == 'image' or e['type'] == 'carousel':
                name = e['id'] + '.jpeg'
                url = e['images']['standard_resolution']['url']
                urllib.urlretrieve(url, name)
            elif e['type'] == 'video':
                name = e['id'] + '.mp4'
                url = e['videos']['standard_resolution']['url']
                urllib.urlretrieve(url, name)


'''
function used to obtain a user's post (download it) 
the user can choose certain criteria to do so
'''
def get_user_post():
    valid_choices = list(range(5))
    print "How would you like to choose the post to download?"
    print "1. Most recent post\n2. Minimum number of likes\n3. Maximum number of likes\n4. Posts with certain tag\n"
    user_choice = raw_input("Enter your choice: ")
    if len(user_choice) == 0 or int(user_choice) not in valid_choices:
        print "Invalid choice... Returning to main menu"
        return
    user_id = get_user_id(input_username())
    if user_id is not None:
        request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
        user_media = requests.get(request_url).json()
        if user_media['meta']['code'] == 200:
            if len(user_media) == 0:
                print "User does't have enough posts"
                return
            else:
                user_choice = int(user_choice)
                if user_choice in valid_choices:
                    media_id = []
                    m_id = 000
                    if user_choice == 1:
                        media_id.append(user_media['data'][0]['id'])
                    elif user_choice == 2:
                        min_likes = user_media['data'][0]['likes']['count']
                        for e in user_media['data']:
                            if min_likes > e['likes']['count']:
                                min_likes = e['likes']['count']
                                m_id = e['id']
                        media_id.append(m_id)
                    elif user_choice == 3:
                        max_likes = user_media['data'][0]['likes']['count']
                        for e in user_media['data']:
                            if max_likes < e['likes']['count']:
                                max_likes = e['likes']['count']
                                m_id = e['id']
                        media_id.append(m_id)
                    elif user_choice == 4:
                        tag = raw_input("Enter the tag you want to search: ")
                        for e in user_media['data']:
                            if tag in e['tags']:
                                media_id.append(e['id'])
                    else:
                        print "Wrong choice. Returning to main menu..."
                        return
                    if len(media_id):
                        for m_id in media_id:
                            print "Downloading post with id %s " % m_id
                            download_post(m_id, user_media['data'])
                            print "The post was downloaded successfully!"
                    else:
                        print "Sorry no relevant posts found"
        else:
            print "Status code other than 200 received. Returning to main menu..."

'''
Main functioning is happening here
'''
valid_options = list(range(9))
print colored("WELCOME TO I-BOT", 'blue')
menu = "MAIN MENU:\n------------------------------------------------------\n"
menu_options = "1. Show self details\n2. Download self recent post\n3. Show details of other user\n" \
               "4. Download post of other user\n5. Like the recent post of a user\n" \
               "6. Comment on the recent post of a user\n" \
               "7. Post comments for promotion of your business\n8. Exit\n"
while True:
    choice = raw_input(menu + menu_options + "\nYour choice: ")
    if len(choice) == 0:
        print "Invalid."
        continue
    else:
        choice = int(choice)
    if choice in valid_options:
        if choice == 1:
            self_info()
        elif choice == 2:
            get_own_post()
        elif choice == 3:
            user_info(input_username())
        elif choice == 4:
            get_user_post()
        elif choice == 5:
            generate_like(input_username())
        elif choice == 6:
            post_comment(ig_username=input_username())
        elif choice == 7:
            promote_business()
        elif choice == 8:
            print colored("THANK YOU FOR USING I-BOT", 'blue')
            sys.exit()
    else:
        print "Invalid choice"
