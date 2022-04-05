import json
with open('/home/lopuma/Compliance/.conf/clientes.json') as op:
    data = json.load(op)
    print(data)
    for clt in data['AFB']:
        print(clt['politica'])
        # for pol in clt['politica']:
        #     print("politica, en linea : ", pol.keys())
            # for sis_pol in pol:
            #     print("Sis : ", sis_pol)
            #     for politica in pol[sis_pol]:
            #         lista = list(politica.keys())
            #         print("lista : ", lista[0])
            #         for icconno in clt['politica'][0]:
            #             print("icconno : ", icconno.values())