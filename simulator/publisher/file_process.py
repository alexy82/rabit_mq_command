# coding=utf-8
import json
import xmltodict


class BaseJsonProcessing(object):
    func_process = None

    def __init__(self, func_process=None):
        if func_process is None:
            self.func_process = self.process_json
        else:
            self.func_process = func_process

    def process_json(self, path):
        result = []
        with open(path) as f:
            data = json.load(f)
        if 'messages' not in data or 'exchanges' not in data:
            raise Exception("File incorrect")
        for content in data['messages']:
            if 'properties' in content and 'body' in content:
                content['body'] = json.dumps(content['body'])
                content['exchanges'] = data['exchanges']
                result.append(content)
        return result


class BaseXmlProcessing(object):
    func_process = None

    def __init__(self, func_process=None):
        if func_process is None:
            self.func_process = self.process_xml
        else:
            self.func_process = func_process

    def process_xml(self, path):
        f = open(path, 'r')
        txt = f.read().replace('\n', '')
        data = xmltodict.parse(txt)
        result = []
        message = []
        if isinstance(data['root']['messages'], list):
            message = data['root']['messages']
        else:
            message.append(data['root']['message'])

        for content in message:
            if 'properties' in content and 'body' in content:
                content['body'] = json.dumps(content['body'])
                content['exchanges'] = data['root']['exchanges']

                result.append(content)
        return result


class JsonProcessing(BaseJsonProcessing):
    pass


class XmlProcessing(BaseXmlProcessing):
    pass
