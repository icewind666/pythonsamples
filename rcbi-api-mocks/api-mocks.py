#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import Response, request
from flask import app
from flask_restful import Api
import json

app = Flask(__name__)
api = Api(app)
app.debug = False


@app.route('/GetInstallationsSummary', methods=['GET'])
def getInstallationsSummary():

    result = []

    inst_values = []
    inst_values.append({'name':'income_measured', 'value':'123'})
    inst_values.append({'name': 'income_balanced', 'value': '666'})
    inst_values.append({'name': 'given_measured', 'value': '123'})
    inst_values.append({'name': 'given_balanced', 'value': '666'})

    installation = dict(name='Установка1', reference='/installation1', values=inst_values)


    inst_values2 = []
    inst_values2.append({'name':'income_measured', 'value':'333'})
    inst_values2.append({'name': 'income_balanced', 'value': '777'})
    inst_values2.append({'name': 'given_measured', 'value': '13'})
    inst_values2.append({'name': 'given_balanced', 'value': '66'})
    installation2 = dict(name='Установка2', reference='/installation2', values=inst_values2)

    inst_values3 = []
    inst_values3.append({'name':'income_measured', 'value':'3345'})
    inst_values3.append({'name': 'income_balanced', 'value': '876'})
    inst_values3.append({'name': 'given_measured', 'value': '93'})
    inst_values3.append({'name': 'given_balanced', 'value': '67'})
    installation3 = dict(name='Установка3', reference='/installation3', values=inst_values3)

    result.append(installation)
    result.append(installation2)
    result.append(installation3)
    return Response(response=json.dumps(result), content_type='application/json')

@app.route('/GetIncomingOperations', methods=['POST'])
def getIncomingOperations():
    postedData = json.loads(request.data)
    instID = postedData['installationReference']
    #print 'id={}'.format(instID)
    print instID
    result = []

    if instID == '/installation1':
        item = {'source': {'name': 'Источник1', 'reference': '/path/to/source1/in/registry'},
                'target': {'name': 'Приемник1', 'reference': '/path/to/target1/in/registry'},
                'product': {'name': 'АИ-95', 'reference': '/path/to/product/in/registry'},
                'measured':22,
                'balanced': 24,
                'error':0.23
                }
        item2 = {'source': {'name': 'Источник2', 'reference': '/path/to/source2/in/registry'},
                'target': {'name': 'Приемник1', 'reference': '/path/to/target2/in/registry'},
                'product': {'name': 'АИ-92', 'reference': '/path/to/product2/in/registry'},
                'measured':22,
                'balanced': 24,
                'error':0.23
                }
        result.append(item)
        result.append(item2)

    if instID == '/installation2':
        item = {'source': {'name': 'Источник2', 'reference': '/path/to/source2/in/registry'},
                'target': {'name': 'Приемник2', 'reference': '/path/to/target3/in/registry'},
                'product': {'name': 'Нефть', 'reference': '/path/to/product3/in/registry'},
                'measured':45,
                'balanced': 78,
                'error':0
                }
        item2 = {'source': {'name': 'Источник3', 'reference': '/path/to/source3/in/registry'},
                'target': {'name': 'Приемник2', 'reference': '/path/to/target2/in/registry'},
                'product': {'name': 'АИ-92', 'reference': '/path/to/product2/in/registry'},
                'measured':11,
                'balanced': 13,
                'error':0
                }
        result.append(item)
        result.append(item2)

    if instID == '/installation3':
        item = {'source': {'name': 'Источник22', 'reference': '/path/to/source2/in/registry'},
                'target': {'name': 'Приемник22', 'reference': '/path/to/target3/in/registry'},
                'product': {'name': 'Нефть', 'reference': '/path/to/product3/in/registry'},
                'measured': 45,
                'balanced': 78,
                'error': 0
                }
        item3 = {'source': {'name': 'Источник222', 'reference': '/path/to/source4/in/registry'},
                'target': {'name': 'Приемник222', 'reference': '/path/to/target4/in/registry'},
                'product': {'name': 'Изобутен', 'reference': '/path/to/product4/in/registry'},
                'measured': 45,
                'balanced': 78,
                'error': 0
                }
        item2 = {'source': {'name': 'Источник6', 'reference': '/path/to/source6/in/registry'},
                 'target': {'name': 'Приемник6', 'reference': '/path/to/target6/in/registry'},
                 'product': {'name': 'Пропилен', 'reference': '/path/to/product5/in/registry'},
                 'measured': 17,
                 'balanced': 12,
                 'error': 2
                 }
        result.append(item)
        result.append(item2)
        result.append(item3)

    return Response(response=json.dumps(result), content_type='application/json')


@app.route('/GetOutgoingOperations', methods=['POST'])
def getOutgoingOperations():
    postedData = json.loads(request.data)
    instID = postedData['installationReference']
    print instID
    result = []

    if instID == '/installation1':
        item = {'source': {'name': 'Источник19', 'reference': '/path/to/source19/in/registry'},
                'target': {'name': 'Приемник19', 'reference': '/path/to/target19/in/registry'},
                'product': {'name': 'АИ-95', 'reference': '/path/to/product/in/registry'},
                'measured':100,
                'balanced': 150,
                'error':0.9
                }
        item2 = {'source': {'name': 'Источник29', 'reference': '/path/to/source29/in/registry'},
                'target': {'name': 'Приемник19', 'reference': '/path/to/target29/in/registry'},
                'product': {'name': 'АИ-92', 'reference': '/path/to/product2/in/registry'},
                'measured':220,
                'balanced': 240,
                'error':0.54
                }
        result.append(item)
        result.append(item2)

    if instID == '/installation2':
        item = {'source': {'name': 'Источник23', 'reference': '/path/to/source23/in/registry'},
                'target': {'name': 'Приемник23', 'reference': '/path/to/target33/in/registry'},
                'product': {'name': 'Нефть', 'reference': '/path/to/product3/in/registry'},
                'measured':11,
                'balanced': 22,
                'error':0
                }
        item2 = {'source': {'name': 'Источник35', 'reference': '/path/to/source35/in/registry'},
                'target': {'name': 'Приемник25', 'reference': '/path/to/target25/in/registry'},
                'product': {'name': 'АИ-92', 'reference': '/path/to/product2/in/registry'},
                'measured':110,
                'balanced': 130,
                'error':50
                }
        item3 = {'source': {'name': 'Источник232', 'reference': '/path/to/source232/in/registry'},
                'target': {'name': 'Приемник232', 'reference': '/path/to/target332/in/registry'},
                'product': {'name': 'Нефть', 'reference': '/path/to/product3/in/registry'},
                'measured':115,
                'balanced': 22,
                'error':70
                }
        result.append(item)
        result.append(item2)
        result.append(item3)

    if instID == '/installation3':
        item = {'source': {'name': 'Источник2_2', 'reference': '/path/to/source2_2/in/registry'},
                'target': {'name': 'Приемник2_2', 'reference': '/path/to/target3_3/in/registry'},
                'product': {'name': 'Нефть', 'reference': '/path/to/product3/in/registry'},
                'measured': 450,
                'balanced': 780,
                'error': 100
                }
        item3 = {'source': {'name': 'Источник222', 'reference': '/path/to/source4/in/registry'},
                'target': {'name': 'Приемник222', 'reference': '/path/to/target4/in/registry'},
                'product': {'name': 'Изобутен', 'reference': '/path/to/product4/in/registry'},
                'measured': 55,
                'balanced': 66,
                'error': 0
                }
        item2 = {'source': {'name': 'Источник61', 'reference': '/path/to/source61/in/registry'},
                 'target': {'name': 'Приемник61', 'reference': '/path/to/target61/in/registry'},
                 'product': {'name': 'Пропилен', 'reference': '/path/to/product5/in/registry'},
                 'measured': 178,
                 'balanced': 122,
                 'error': 2
                 }
        result.append(item)
        result.append(item2)
        result.append(item3)

    return Response(response=json.dumps(result), content_type='application/json')


@app.route('/GetModels', methods=['GET'])
def getModels():
    result = []
    result.append({'name': 'Завод1', 'reference': '/facility1'})
    result.append({'name': 'Завод2', 'reference': '/facility2'})
    result.append({'name': 'МегаЗавод', 'reference': '/facilityMega'})
    result.append({'name': 'ЗаводнойЗавод', 'reference': '/facilityFacility'})

    return Response(response=json.dumps(result), content_type='application/json')

@app.route('/GetAnalysisInstances', methods=['GET'])
def getAnalysisInstances():
    result = []
    result.append({'name': 'АнализПервичный_1',
                   'reference': '/analysis_1',
                   'type': 'primary',
                   'period_from': '2017-01-01T00:00:00',
                   'period_to': '2017-01-02T00:00:00',
                   })
    result.append({'name': 'АнализПервичный_2',
                   'reference': '/analysis_2',
                   'type': 'primary',
                   'period_from': '2017-01-04T00:00:00',
                   'period_to': '2017-01-07T10:00:00',
                   })
    result.append({'name': 'АнализЭкономический',
                   'reference': '/analysis_3',
                   'type': 'economical',
                   'period_from': '2017-01-05T00:00:00',
                   'period_to': '2017-01-15T00:00:00',
                   })
    return Response(response=json.dumps(result), content_type='application/json')

@app.route('/GetAnalysisTypes', methods=['GET'])
def getAnalysisTypes():
    result = []
    result.append({'name': 'Первичный', 'id': 'primary'})
    result.append({'name': 'Экономический', 'id': 'economical'})
    return Response(response=json.dumps(result), content_type='application/json')



app.run(host="192.168.150.225", port=8080)




