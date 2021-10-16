# -*- coding:utf-8 -*-


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Import ( Global Modules )
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
from flask import abort, Flask, jsonify, make_response, render_template, request, send_from_directory, Markup, redirect, url_for
from flask_cors import CORS
from functools import wraps
from os import environ as env
from cerberus import Validator
from pythonjsonlogger import jsonlogger
from pyvirtualdisplay import Display
import urllib.parse
import pdfkit
import logging


class JsonFormatter(jsonlogger.JsonFormatter, object):
    def __init__(self, fmt="%(levelname) %(message)", style='%', *args, **kwargs):
        jsonlogger.JsonFormatter.__init__(self, fmt=fmt, *args, **kwargs)

    def process_log_record(self, log_record):
        log_record['severity'] = log_record['levelname']
        del log_record['levelname']
        return super(JsonFormatter, self).process_log_record(log_record)


# 出力PDFをA4とした場合に必要な仮想ディスプレイのサイズ情報
# ---
A4_WIDTH = 1432
A4_HEIGHT = 2074
PDF_OPTIONS = {
    "page-size": "A4",
    # "orientation": "Portrait",
    # "margin-top": "0.4in",
    # "margin-right": "0.4in",
    # "margin-bottom": "0.4in",
    # "margin-left": "0.4in",
    "orientation": "Landscape",
    "margin-top": "0",
    "margin-right": "0",
    "margin-bottom": "0",
    "margin-left": "0",
    "encoding": "UTF-8",
    "quiet": ""
}
OK_PDF_TEMPLATE = "template_1.html"
NG_PDF_TEMPLATE = "template_2.html"


# Flask本体をインスタンス化
# ---
APP = Flask(__name__, template_folder='template/dist', static_url_path='/')
APP.config["JSON_AS_ASCII"] = False
CORS(APP)
werkzeug_logger_handler = logging.StreamHandler()
werkzeug_logger_handler.setFormatter(JsonFormatter())
werkzeug_logger = logging.getLogger("werkzeug")
werkzeug_logger.setLevel(logging.INFO)
werkzeug_logger.addHandler(werkzeug_logger_handler)
werkzeug_logger.propagate = False


# PDF出力に必要な情報
# ---
__pdf_req_schema = {
    "name": {
        "type": "string",
        "empty": False,
    },
    "ledger": {
        "type": "list",
        "schema": {
            "type": "dict",
            "schema": {
                "id": {
                    "type": "integer",
                },
                "date": {
                    "type": "string",
                    "regex": "^\d{4}/\d{2}/\d{2}$",
                },
                "name": {
                    "type": "string",
                    "required": True,
                    "empty": False,
                },
                "price": {
                    "type": "integer",
                    "required": True,
                    "empty": False,
                },
                "status": {
                    "type": "string",
                    "required": True,
                    "empty": False,
                    "allowed": ["done", "close", "call", "warning"],
                },
            }
        }
    }
}


# Generate PDF bytes from HTML
# ---
def __generatePDFFromHTML(fileName, pdfBuffer):
    response = make_response(pdfBuffer)
    dispostion = "attachment; filename*=UTF-8''"
    escapedFileName = urllib.parse.quote(fileName)
    dispostion += escapedFileName + ".pdf"
    response.headers["Content-Disposition"] = dispostion
    response.mimetype = "application/pdf"
    return response


# Generate Gzip bytes
# ---
def ___gzip(filePath, contentType):
    fp = open(filePath, "rb")
    content = fp.read()
    fp.close()
    res = make_response(content)
    res.headers["Content-Type"] = contentType
    res.headers["Cache-Control"] = 'public,max-age=43200'
    res.headers["Content-Encoding"] = "gzip"
    return res


# Validate JSON Parameter
# ---
def requires_pdf_param(f):
    @wraps(f)
    def validate(*args, **kwargs):
        params = request.get_json()
        v = Validator()
        v.schema = {**__pdf_req_schema}
        if params is None:
            abort(400, "None Parameter")
        v.validate(params)
        if len(v.errors) == 0:
            return f(*args, {**kwargs, **params})
        else:
            abort(400, v.errors)
    return validate


# Utility
# ---
@APP.context_processor
def utility_processor():
    def format_currency(amount):
        return "{:,}".format(amount)
    return dict(format_currency=format_currency)


# 400
# ---
@APP.errorhandler(400)
def handle_bad_request_error(ex):
    try:
        tmpVirtualDisplay = Display(visible=0, size=(A4_WIDTH, A4_HEIGHT))
        tmpVirtualDisplay.start()
        tmpHTML = render_template(NG_PDF_TEMPLATE, MSG=ex)
        pdfBuffer = pdfkit.from_string(tmpHTML, False, options=PDF_OPTIONS)
    except Exception as ex:
        print(ex)
        pdfBuffer = pdfkit.from_string("System Error - 1", False, options=PDF_OPTIONS)
    finally:
        tmpVirtualDisplay.stop()
    return __generatePDFFromHTML("error", pdfBuffer)


# 404
# ---
@APP.errorhandler(404)
def handle_not_found_error(ex):
    return redirect(url_for("send_template_index"))


# Access to "/favicon.ico" [ GET ]
# ---
@APP.route("/favicon.ico")
def send_favicon():
    return send_from_directory("template/src/image", "logo.ico")


# Access to "/health_check" [ GET ]
# ---
@APP.route("/health_check")
def health_check():
    return "Status OK"


# Access to "/css/*" [ GET ]
# ---
@APP.route("/css/<path:path>")
def send_css(path):
    return send_from_directory("template/dist/css", path)


# Access to "/css/papyrus-common.css" [ GET ]
# ---
@APP.route("/css/papyrus-common.css")
def send_gzip_css():
    return ___gzip(
        filePath="template/dist/css/papyrus-common.css.gz",
        contentType="text/css")


# Access to "/js/*" [ GET ]
# ---
@APP.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("template/dist/js", path)


# Access to "/js/papyrus-common.js" [ GET ]
# ---
@APP.route("/js/papyrus-common.js")
def send_gzip_js():
    return ___gzip(
        filePath="template/dist/js/papyrus-common.js.gz",
        contentType="text/javascript")


# Access to "/image/*" [ GET ]
# ---
@APP.route("/image/<path:path>")
def send_image(path):
    return send_from_directory("template/src/image", path)


# Access to "/license" [ GET ]
# ---
@APP.route("/license")
def send_license():
    return send_from_directory("template/dist", "LICENSE.txt")


# Access to "/template" [ GET ]
# ---
@APP.route("/template")
def send_template_index():
    return send_from_directory("template/dist", "index.html")


# Access to "/template/*" [ GET ]
# ---
@APP.route("/template/<path:path>")
def send_template(path):
    templateFile = "template_" + path + ".html"
    LEDGER = [
        {
            "date": "2099/12/28",
            "id": 1,
            "name": "徳川家康",
            "price": 100000,
            "status": "done"
        },
        {
            "date": "2099/12/29",
            "id": 2,
            "name": "徳川秀忠",
            "price": 200000,
            "status": "close"
        },
        {
            "date": "2099/12/30",
            "id": 3,
            "name": "徳川家光",
            "price": 300000,
            "status": "call"
        },
        {
            "date": "2099/12/31",
            "id": 4,
            "name": "徳川家綱",
            "price": 400000,
            "status": "warning"
        }
    ]
    MSG = Markup("Dummy Error Message...<br />Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.")
    try:
        return render_template(templateFile, MSG=MSG, LEDGER=LEDGER)
    except Exception:
        abort(404)


# Access to "/template_*.html" [ GET ]
# ---
@APP.route("/template_<path:path>.html")
def send_node_template(path):
    return redirect(url_for("send_template", path=path))


# Access to "/pdf" [ POST ]
# ---
@APP.route('/pdf', methods=["POST"])
@requires_pdf_param
def pdf(pdfInfo):
    try:
        tmpVirtualDisplay = Display(visible=0, size=(A4_WIDTH, A4_HEIGHT))
        tmpVirtualDisplay.start()
        tmpHTML = render_template(
            OK_PDF_TEMPLATE,
            LEDGER=pdfInfo["ledger"])
        pdfBuffer = pdfkit.from_string(tmpHTML, False, options=PDF_OPTIONS)
    except Exception as ex:
        print(ex)
        pdfBuffer = pdfkit.from_string("System Error - 2", False, options=PDF_OPTIONS)
    finally:
        tmpVirtualDisplay.stop()
    return __generatePDFFromHTML(pdfInfo["name"], pdfBuffer)


if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=env.get("API_DEFAULT_PORT"))
