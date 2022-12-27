from flask import Flask, render_template, request,jsonify
import mysql.connector
import os
import logging

app = Flask(__name__)


def logger (func):
    logging.basicConfig(filename='record.log', level=logging.DEBUG)
    def log():
        app.logger.debug("debug log info")
        app.logger.info("Info log information")
        app.logger.warning("Warning log info")
        app.logger.error("Error log info")
        app.logger.critical("Critical log info")
        return "testing logging levels."


def get_DB(frm,typ):
    conn = mysql.connector.connect(
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PASSWORD'),
        host=os.environ.get('DB_HOST'),
        port=os.environ.get('DB_PORT'),
        database=os.environ.get('DB_NAME')
        )
    res=[]
    cur = conn.cursor()
    if typ == "all":
         cur.execute(
               f"SELECT * FROM {frm} WHERE date > DATE_SUB(DATE_SUB(NOW() ,INTERVAL 24 HOUR),INTERVAL 5 HOUR)")
    elif typ == "current":
         cur.execute(
                f"SELECT * FROM {frm} WHERE date > DATE_SUB(DATE_SUB(NOW() ,INTERVAL 1 HOUR),INTERVAL 5 HOUR)")

 
    if frm == "cpu":
        for date, used in cur:
             dic = {}
             dic['date'] =str(date)
             dic['used'] = used
             res.append(dic)
    else:
        for date, used,available in cur:
             dic = {}
             dic['date'] =str(date)
             dic['used'] = used
             dic['available']=available
             res.append(dic)


    return res


@logger
@app.route('/cpu', methods=['GET'])
def cpu():
    if 'type' in request.args:
        typ = request.args['type']  
    result =  get_DB("cpu",typ)
  
    return jsonify(result)

@logger
@app.route('/disk', methods=['GET'])
def disk():
    if 'type' in request.args:
        typ = request.args['type']
    result =  get_DB("disk",typ)

    return jsonify(result)

@logger
@app.route('/memory', methods=['GET'])
def memory():
    if 'type' in request.args:
        typ = request.args['type']
    result =  get_DB("memory",typ)

    return jsonify(result)









if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
