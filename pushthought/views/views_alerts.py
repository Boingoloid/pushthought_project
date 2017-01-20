from django.contrib import messages

#helper
def show_tweet_success_message(request, tweet_text): #helper
    #send success message
    messages.success(request, 'Tweet sent successfully.')
    # response = JsonResponse({'tweet_text': tweet_text})
    return None