# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EndoForumsItem(scrapy.Item):
    # To be found from external sites like Google Search
    url = scrapy.Field()
    article_title = scrapy.Field()
    reddit_url = scrapy.Field()

    # To be found from PRAW (Reddit API)
    r_post_title = scrapy.Field()
    r_category_label = scrapy.Field()
    r_post_text_body = scrapy.Field()
    r_post_comments_count = scrapy.Field()
    r_post_upvote_count = scrapy.Field()
    r_post_downvote_count = scrapy.Field()
    r_post_comment_body = scrapy.Field()

    # References for selectors in reddit forums : 
    # Note : t3_1swqul8 is a unique identifier for a reddit post
    
    # reddit_post_title = #post-title-t3_1swqul8
    # reddit_category_label = #t3_1swqul8 > div.mb-2xs.px-md.xs\:px-0 > shreddit-post-flair > a > span > div
    # shreddit_post_text_body = #t3_1swqul8 > shreddit-post-text-body
    # reddit_interaction_stats = rpl-action-bar
    # reddit_comment_content = #comment-tree > shreddit-comment:nth-child(5) > details > div > div:nth-child(3)


