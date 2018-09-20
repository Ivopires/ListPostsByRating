# ListPostsByRating
App developed in Python, using the Django framework.

# List Posts By Rating

## How to run

### Setup Django (version 1.11.15):
  1. Install pip (if you have not installed already): [Guide](https://packaging.python.org/tutorials/installing-packages/)
  2. Install Django (version 1.11.15):
    ```
      pip install Django==1.11.15
    ```

### Load db scheme
```
python manage.py migrate
```

### Populate db with Posts

```
python manage.py shell

>>>from list_posts.models import Posts
>>>post = Post(post_text='Example text')
>>>post.save()
```

### Run tests

```
python manage.py test list_posts
```

### Run the project
To run project you must follow the following steps:

  1. Start the server: 
  
  ```
    python manage.py runserver
  ```
  
  2. Go to the following link - [127.0.0.1:8000](http://127.0.0.1:8000)

There are four available endpoints:
```
/
/upvote/:post_id
/downvote/:post_id
/posts/
```

The first endpoint is responsible to list the latest 10 posts, ordered by posting date, if by accident 'future' posts are added to the database, these will not show on the page. The second and third endpoints are responsible to give the up/down votes, respectively, to the post with the <post_id>. Finally, the last endpoint, will show all the available posts, ordered by 'score', being the top-scored posts on the top and the less-scored posts on the bottom.

To achieve a post score that would allow to order different posts with the same up/down votes ratio, as mentioned on the challenge's README, a Wilson-score Interval metric was used, which value depends solely on the number of up/down votes, total number of votes of the post and on the __z__ value used by the normal distribution (which depends on the degree of confidence used).
