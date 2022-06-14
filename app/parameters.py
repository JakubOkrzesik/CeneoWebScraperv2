selectors = {
    'author' : ['span.user-post__author-name'],
    'recommendation': ['span.user-post__author-recomendation > em'],
    'stars' : ['span.user-post__score-count'],
    'useful' : ['button.vote-yes > span'],
    'useless' : ['button.vote-no > span'],
    'publish_date' : ['span.user-post__published > time:nth-child(2)', 'datetime'],
    'purchase_date' : ['span.user-post__published > time:nth-child(2)', 'datetime'],
    'pros' : ['div.review-feature__title--positives ~ div.review-feature__item', None, True],
    'cons' : ['div.review-feature__title--negatives ~ div.review-feature__item', None, True]
}