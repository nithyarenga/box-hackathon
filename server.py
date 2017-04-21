from bottle import Bottle, route, run
from bottle import request, response
from bottle import post, get, put, delete
from json import dumps, loads
from datetime import datetime
from requests.exceptions import HTTPError
import StringIO
import datetime
import requests
import json
import run_email as email

from boxsdk import Client, OAuth2

app = Bottle()

@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

oauth = OAuth2(
    client_id='jgnm81okjo9lbln71hjf3uotktyujexk',
    client_secret='AuvftWi1yW5HeTiS7uInzGaWEsBk9L8d',
    access_token="hzlEW8nTniFUhFOuEO9Q8sRbnLBV5qXv"
)

client = Client(oauth)

@app.route('/hello')
def hello():
    return "Hello World!"

@app.route('/get_folder_contents')
def get_folder():
   items = client.folder(folder_id='24663101383').get_items(limit=100, offset=0)
   name = {"files": [items[2].name,items[3].name,items[4].name,items[5].name,items[6].name,items[7].name,items[8].name]}
   return name

@app.route('/get_poke')
def get_metadata():
    metadata = client.file(file_id='161846645670').metadata().get()
    final = []
    pokelist = metadata["Poke"]
    pokes = pokelist.split('***')
    for string in pokes:
        pokeitem = string.split("*#")
        print pokeitem
        result = {"who":pokeitem[0],"whom":pokeitem[1],"date":pokeitem[2],"comment":pokeitem[3]}
        final.append(result)
    final_output= {"pokes": final}
    return final_output

@app.route('/get_collab_file')
def get_collab_file():
    collaborators = {0:{"name":"Gopinath Sundaramurthy","url":"https://app.box.com/api/avatar/large/13183168"},1:{"url":"https://app.box.com/api/avatar/large/1514222905", "name": "Nithya Renganathan"},2:{"name":"Sokly Meach","url":"https://app.box.com/api/avatar/large/1510389410"},3:{"name":"Vidhi Shah","url":"https://app.box.com/api/avatar/large/1516779499"},4:{"name":"Ravithej Chikkala","url":"https://app.box.com/api/avatar/large/1506765649"},5:{"name":"Marisa Mace","url":"https://app.box.com/api/avatar/large/1514222905"}}
    return collaborators

@app.route('/get_collab_folder')
def get_collaf_folder():
    #me = client.user(user_id='1510389410').get()
    #print me[avatar_url]
    collaborators = {0:{"name":"Gopinath Sundaramurthy","url":"https://app.box.com/api/avatar/large/13183168"},1:{"url":"https://app.box.com/api/avatar/large/1514222905", "name": "Nithya Renganathan"},2:{"name":"Sokly Meach","url":"https://app.box.com/api/avatar/large/1510389410"},3:{"name":"Vidhi Shah","url":"https://app.box.com/api/avatar/large/1516779499"},4:{"name":"Ravithej Chikkala","url":"https://app.box.com/api/avatar/large/1506765649"},5:{"name":"Marisa Mace","url":"https://app.box.com/api/avatar/large/1514222905"}}
    return collaborators

@app.route('/poke_input' ,method='POST')
def poke_input():
    value = request.body.read()
    v = loads(value)
    print v['receiver']
    output = v['receiver']+"*#"+v['sender']+"*#April 21st 2017"+"*#"+v['comment']+"***"
    print output
    metadata = client.file(file_id='161846645670').metadata()
    update = metadata.start_update()
    data = client.file(file_id='161846645670').metadata().get()
    pokelist = data["Poke"]
    print pokelist + output
    update.add('/Poke', output + pokelist)
    metadata.update(update)
    return dumps({'success':True}, 200, {'ContentType':'application/json'})

@app.route('/get_collab_status')
def roles():
    with open('status.json') as json_data:
      d = json.load(json_data)
    return d

@app.route('/update_status', method='POST')
def update():
    with open('status.json') as json_data:
      d = json.load(json_data)
      print(d)
    value = request.body.read()
    v = loads(value)
    if v['name'] == 'Nithya Renganathan' :
       d["1"]["status"] = "complete"
    if v['name'] == 'Gopinath Sundaramurthy' :
       d["0"]["status"] = "complete"
    if v['name'] == 'Ravithej Chikkala' :
       d["2"]["status"] = "complete"
    if v['name'] == 'Sokly Meach' :
       d["3"]["status"] = "complete"
    if v['name'] == 'Marisa Mace' :
       d["4"]["status"] = "complete"
    if v['name'] == 'Vidhi Shah' :
       d["5"]["status"] = "complete"
    with open('status.json', 'w') as outfile:
       json.dump(d, outfile)
    email.send_email('PokiBox', 'gopinath.sundaramurthy@gmail.com', 'Vidhi has Signed off on Docs', 'This really works!!!')
    return None

run(app, host='184.173.110.13', port=8082, debug=True)
