init = "Запушена процедура инициализации"
started = "Теперь сервер доступен из сети"
program_init = "Запускается обработчик"
program_started = "Обработчик запущен"
callback_wrong = "Процедура обратной связи не поддерживает метод __call__"
restart_server = "Производим перезапуск сервера!"
restart_program = "Производим перезапуск программы!"
program_restarted = "Программа перезапущена"
stop = "Сервер останавливается"
toexit = "Для завершения работы нажмите Ctrl + C"
monitor = "Запущен файловый монитор"
sep = "\n"

errors = {   
    100:    "Continue",
    101:	"Switching Protocols", 	 
    200:	"Action completed successfully",
    201: 	"Created:	Success following a POST command",
    202:	"Accepted:	The request has been accepted for processing, but the processing has not been completed.",
    203:	"Partial Information:	Response to a GET command, indicates that the returned meta information is from a private overlaid web.",
    204:	"No: Content	Server has received the request but there is no information to send back.",
    205:	"Reset Content",
    206:	"Partial Content:	The requested file was partially sent.   Usually caused by stopping or refreshing a web page.",
    300:	"Multiple Choices", 	 
    301:	"Moved Permanently:	Requested a directory instead of a specific file.   The web server added the filename index.html, index.htm, home.html, or home.htm to the URL.",
    302:	"Moved Temporarily",
    303:	"See Other",
    304:	"Not Modified:	The cached version of the requested file is the same as the file to be sent.",
    305:	"Use Proxy",
    400:	"Bad Request:	The request had bad syntax or was impossible to be satisified.",
    401:	"Unauthorized:	User failed to provide a valid user name / password required for access to file / directory.",
    402:	"Payment Required",
    403:	"Forbidden:	The request does not specify the file name. Or the directory or the file does not have the permission that allows the pages to be viewed from the web.",
    404:	"Not Found:	The requested file was not found.",
    405:	"Method Not Allowed",
    406:	"Not Acceptable",
    407:	"Proxy Authentication Required",
    408:	"Request Time-Out", 	 
    409:	"Conflict",
    410:	"Gone",
    411:	"Length Required",
    412:	"Precondition Failed",
    413:	"Request Entity Too Large",
    414:	"Request-URL Too Large",
    415:	"Unsupported Media Type",
    500:	"Server Error:	In most cases, this error is a result of a problem with the code or program you are calling rather than with the web server itself.",
    501:	"Not Implemented:	The server does not support the facility required.",
    502:	"Bad Gateway",
    503:	"Out of Resources:	The server cannot process the request due to a system overload.  This should be a temporary condition.",
    504:	"Gateway Time-Out:	The service did not respond within the time frame that the gateway was willing to wait.",
    505:	"HTTP Version not supported"
}	

msgs = dir() 

class logPrototype():
    
    def __init__(self): pass
    def __getattr__(self, name):
        if name in msgs:
            msg = eval(name)
            print(msg)
            return (msg)
    def __call__(self, *args):
        print(*args)
        
log = logPrototype()
            
