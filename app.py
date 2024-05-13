from ppBackend import app

def _run():
    """ Imports the app and runs it. """
    app.run(debug=True, host="0.0.0.0", port=5000)
    app.logger.debug('This is a debug message')
    app.logger.info('This is an info message')
    app.logger.warning('This is a warning message')
    app.logger.error('This is an error message')
    app.logger.critical('This is a critical message')

if __name__ == '__main__':
    _run()
