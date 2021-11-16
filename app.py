try:

    from ppBackend import app
except ImportError as e:
    print(e)

def _run():
    """ Imports the app and runs it. """
    app.run(debug=True, host="0.0.0.0", port=5000)


if __name__ == '__main__':
    _run()
