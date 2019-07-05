import sys
import json
import argparse
from random import choice, randint


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--news',
                        default=10,
                        help='news count',
                        type=int,
                        )
    parser.add_argument('-c', '--comments',
                        default=25,
                        help='comments count',
                        type=int,
                        )

    return parser


def gen_news(count):
    news = {}
    news['news'] = []
    news_dates = ["2019-01-01T20:56:35",
                  "2018-01-01T20:56:36",
                  "2020-01-01T20:56:36",
                  "2018-01-01T21:56:36",
                  "2018-01-02T20:56:36",
                  "2018-10-01T20:56:36",
                  "2033-01-01T20:56:36",
                  "2018-01-01T20:56:36",
                  "2018-01-11T20:56:36",
                  "2021-01-01T20:56:36",
                  "2018-01-01T20:56:36",
                  "2017-01-01T20:56:36",
                  ]
    news_bodies = ["Hello world",
                   "The news",
                   "Bla bla bla",
                   "London is a capital of Great Britain",
                   "Aiohttp",
                   "Jokes",
                   "Good Idea",
                   "cactus",
                   "ACAB - all cats are beautiful",
                   "amazing news: Duck - bird",
                   ]
    for i in range(1, count+1):
        news_item = {}
        news_item['id'] = i
        news_item['title'] = 'news_%g' % i
        news_item['date'] = choice(news_dates)
        news_item['body'] = choice(news_bodies)
        news_item['deleted'] = choice([True, False, False, False])
        news['news'].append(news_item)
    return news


def gen_comments(count, news):
    comments = {}
    comments['comments'] = []
    news = news['news']
    for i in range(1, count+1):
        news_id = randint(1, len(news))
        comment_item = {}
        comment_item['id'] = i
        comment_item['title'] = 'title_%g' % i
        comment_item['news_id'] = news_id
        comment_item['date'] = list(filter(lambda k: k['id'] == news_id, news))[0].get('date')
        comment_item['comment'] = 'Comment %g for news %g' % (i, news_id)
        comments['comments'].append(comment_item)
    return comments


if __name__ == '__main__':
    parser = create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    news = gen_news(namespace.news)
    comments = gen_comments(namespace.comments, news)

    with open('news.json', 'w') as f:
        json.dump(news, f)
    with open('comments.json', 'w') as f:
        json.dump(comments, f)
