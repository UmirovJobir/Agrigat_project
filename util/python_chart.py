# import pygal


# repos = [
#  {
#  'value': 20506,
#  'color': '#3333CC',
#  'xlink': 'http://127.0.0.1:8000/chart/',
#  },
#  20054,
#  12607,
#  11827,
#  ]
# chart = pygal.Bar()
# chart.force_uri_protocol = 'http'
# chart.x_labels = [
#  'django', 'requests', 'scikit-learn',
#  'tornado',
#  ]
# chart.y_title = 'Stars'
# chart.add('Python Repos', repos)
# chart.render_to_file('python_repos.svg')

import json
from urllib.parse import urlencode
from shop.models import Product, Group, User


users = User.objects.all()
user_names = [user.user_name for user in users]
user_ids = [user.user_id for user in users]

config = {
    "type": "bar",
    "data": {
        "labels": user_names,
        "datasets": [{
            "label": "Foo",
            "data": user_ids
        }]
    }
}

params = {
    'chart': json.dumps(config),
    'width': 500,
    'height': 300,
    'backgroundColor': 'white',
}
print('https://quickchart.io/chart?%s' % urlencode(params))
