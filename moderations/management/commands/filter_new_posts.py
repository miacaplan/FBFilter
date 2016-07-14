import datetime
import dateutil.parser
from django.core.management.base import BaseCommand
from moderations import models
from FB import connect
from django.utils import timezone
import requests
# from multiprocessing import Process
from threading import Thread

# last_checked = timezone.now() - datetime.timedelta(days = 10)

class Command(BaseCommand):
    help = "Collect new posts and filter them"

    def _updated(self, fb_id, message, created_time, group):
        if created_time > group.last_filtered:
            return True
        p = group.postments.filter(fb_id = fb_id)
        if p and models.calc_hash(message) != p[0].hash_val:
            models.Action.add_action(p, models.Action.Type.EDIT_DETECTED, None)
            return True
        return False

    def _suspected(self, fb_id, message, created_time, group):
        if not self._updated(fb_id, message, created_time, group):
            return False
        if any(w for w in group.hate_words_list if w in message):
            return True
        return False

    def _upsert_postment(self, level, parents, parent_edges, group, edge, status):
        # might need to add parent for data integrity
        if level > 0 and not parents[0]:
            parents[0] = self._upsert_postment(level - 1, parents[1:], parent_edges[1:], group, parent_edges[0], models.Postment.Status.PASSED_FILTER)
            print(parents[0])
        return models.Postment.objects.update_or_create(fb_id = edge['id'],
            defaults = {
                'type': models.Postment.Type.POST if level == 0 else models.Postment.Type.COMMENT,
                'fb_id': edge['id'],
                'fb_user_id': edge['from']['id'],
                'message': edge['message'],
                'group': group,
                'posted_at': dateutil.parser.parse(edge['created_time']),
                'nesting_level': level,
                'hash_val': models.calc_hash(edge['message']),
                'num_reactions': edge.get('likes_count', edge.get('reactions', {}).get('summary', {}).get('total_count', 0)),
                'parent': parents[0] if level > 0 else None,
                'status': status,
            })[0]

    def _handle_comments(self, level, parent_postments, parent_edges, group):
        if not parent_edges[0].get('comments'):
            return
        page = parent_edges[0].get('comments')
        while True:
            for comment in page['data']:
                created_time = dateutil.parser.parse(comment['created_time'])
                postment = None
                if self._suspected(comment['id'], comment['message'], created_time, group):
                    # add/update post
                    postment = self._upsert_postment(level, parent_postments, parent_edges, group, comment, models.Postment.Status.PENDING)
                    models.Action.add_action(postment, models.Action.Type.FILTERED, None)
                if level < 2:
                    self._handle_comments(level + 1, [postment] + parent_postments, [comment] + parent_edges, group)
            try:
                page = requests.get(page['paging']['next']).json()
            except KeyError:

                break

    def _update_group(self, group):
        try:
            # o = graph.get_object(group.fb_group_id + '/feed.since(13-06-2016)'), # {})'.format(last_checked),
            start_time = timezone.now()
            graph = connect.connect_with_token(
                    group.administrator.user.social_auth.get(provider='facebook').extra_data['access_token'])
            o = graph.get_object(group.fb_group_id + '/feed',  # {})'.format(last_checked),
                                 fields='id,created_time,shares,status_type,reactions.summary(true),updated_time,message,from, permalink_url,comments.limit(100).fields(message,from, created_time, like_count, comments.limit(100).fields(message,from,created_time, like_count))',
                                 limit=25,
                                 since=group.last_filtered)  # .strftime('%m/%d/%yT%H:%M:%S'))
            page = o
            while True:
                for post in page['data']:
                    # since new comments change the updated_time of the post - should either filter out by created_time, or use checksum to test
                    # if a post has changed
                    # need to also check if any of the pending posts have been edited in the meantime
                    postment = None
                    if self._suspected(post['id'], post.get('message', ''), dateutil.parser.parse(post['created_time']),
                                       group):
                        # add/update post
                        postment = self._upsert_postment(0, [], [], group, post, models.Postment.Status.PENDING)
                        models.Action.add_action(postment, models.Action.Type.FILTERED, None)
                    self._handle_comments(1, [postment], [post], group)

                    # print(post.get('message'))
                    # # if post.get('comments'):
                    # #     for comment in post.get('comments')['data']:
                    # #         print(comment.get('from'))
                    # post['group'] = group
                    # post['reactions'] =
                    # # post['reactions'] = post.get('likes', {}).get('summary', {}).get('total_count', 0)
                    # post['shares'] = post.get('shares', {}).get('count', 0)
                    # post['created_time'] = dateutil.parser.parse(post['created_time'])
                    # post['updated_time'] = dateutil.parser.parse(post['updated_time'])


                    # res = models.upsert(models.posts_collection, o['data'])
                    # print('Inserted {} posts, updated {} posts.'.format(res['inserted'], res['updated']))
                try:
                    page = requests.get(page['paging']['next']).json()
                except KeyError:
                    break
                    # update the group
        except:
            pass  # todo
        else:
            group.last_filtered = start_time
            group.save()

    def handle(self, *args, **options):
        # pool = Pool(5)
        # pool.map(self._update_group, models.FBGroup.objects.all())
        procs = [Thread(target=self._update_group, args=(group,)) for group in models.FBGroup.objects.all()]
        for p in procs:
            p.start()
        for p in procs:
            p.join()
#### android SDK
# get post
# GraphRequest request = GraphRequest.newGraphPathRequest(
#   accessToken,
#   "/953251484750615_1021329741276122",
#   new GraphRequest.Callback() {
#     @Override
#     public void onCompleted(GraphResponse response) {
#       // Insert your code here
#     }
# });
#
# request.executeAsync();

# delete post
# Bundle parameters = new Bundle();
#
# GraphRequest request = new GraphRequest(
#   accessToken,
#   "/953251484750615_1021329741276122",
#   parameters,
#   HttpMethod.DELETE,
#   new GraphRequest.Callback() {
#     @Override
#     public void onCompleted(GraphResponse response) {
#       // Insert your code here
#     }
# });
#
# request.executeAsync();

# comment
# GraphRequest request = GraphRequest.newPostRequest(
#   accessToken,
#   "/953251484750615_1021320597943703/comments",
#   new JSONObject("{\"message\":\"commenting through graph api\"}"),
#   new GraphRequest.Callback() {
#     @Override
#     public void onCompleted(GraphResponse response) {
#       // Insert your code here
#     }
# });
# request.executeAsync();


##### JS

#delete
# FB.api(
#   '/953251484750615_1021329741276122',
#   'DELETE',
#   {},
#   function(response) {
#       // Insert your code here
#   }
# );

# commend
# FB.api(
#   '/953251484750615_1021320597943703/comments',
#   'POST',
#   {"message":"commenting through graph api"},
#   function(response) {
#       // Insert your code here
#   }
# );


#### meesaging
# https://developers.facebook.com/docs/messenger-platform/send-api-reference

#me?fields=admined_groups{unread,feed.include_hidden(true){updated_time}}

#for comments on post - parent is object.message, comment on comment - parent.


