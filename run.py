from lib import run
from config import Conf
import router

run(host=Conf.HOST, port=Conf.PORT, debug=Conf.DEBUG, reloader=Conf.RELOAD)