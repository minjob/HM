import logging
from spyne import Application
from spyne import rpc
from spyne import ServiceBase
from spyne import Iterable, Integer, Unicode, Array, util, AnyDict, ModelBase
from spyne.protocol.soap import Soap11
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from suds.client import Client
from spyne import Application
from wsgiref.simple_server import make_server

from schedul_backend.interface_manage import WMS_Interface

soap_app = Application([WMS_Interface], 'WMS_Interface', in_protocol=Soap11(validator='lxml'),
                       out_protocol=Soap11())
wsgi_app = WsgiApplication(soap_app)
if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://192.168.7.100:5001/")
    logging.info("wsdl is at: http://192.168.7.100:5001/?wsdl")

    server = make_server('192.168.7.100', 5001, wsgi_app)
    server.serve_forever()

