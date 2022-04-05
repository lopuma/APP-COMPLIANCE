import json

with open('/home/esy9d7l1/Compliance/.conf/clientes.json') as op:
    data = json.load(op)

politicas = {
    tipo : { k : { "icon": v[0]["icon"], "scripts": v[1]["scripts"] }
           for pol in pols[0]["policy"]
           for k,v in pol.items() }
    for tipo, pols in data.items()
}
icons = [ x["icon"] for pol in politicas.values() for x in pol.values() ]
scripts = [ x["scripts"] for pol in politicas.values() for x in pol.values() ]

print(icons)
