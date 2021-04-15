from flask import Blueprint, make_response, jsonify
import requests

bp = Blueprint('news', __name__, url_prefix='/api/news')


@bp.route('', methods=['GET'])
def get_news():
    return "pong", 200


@bp.route('/moex', methods=['GET'])
def get_top_moex_news():
    url = 'http://iss.moex.com/iss/sitenews.json'
    r = requests.get(url)

    if r.status_code != 200:
        return "error", r.status_code
    news = r.json()
    top_news = news['sitenews']['data'][:5]
    result = { 
        'news': []
    }
    for n in top_news:
        d = {
            'id': n[0],
            'title': n[2],
            'published_at': n[3]
        }
        result['news'].append(d)
        
    resp = make_response(
        jsonify(result), 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp


@bp.route('/moex/<int:id>', methods=['GET'])
def get_moex_news_by_id(id):
    url = 'http://iss.moex.com/iss/sitenews/{0}.json'.format(id)
    r = requests.get(url)

    if r.status_code != 200:
        return "error", 400
    
    article = r.json()
    d = {
        'id': article['content']['data'][0][0],
        'title': article['content']['data'][0][1],
        'published_at': article['content']['data'][0][2],
        'body': article['content']['data'][0][3]
    }
    resp = make_response(
        jsonify({'result': d}), 200
    )
    resp.headers['Content-Type'] = 'application/json; charset=utf-8'
    return resp