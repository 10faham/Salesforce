try:

    from ppBackend import app
except ImportError as e:
    print(e)

def _run():
    """ Imports the app and runs it. """
    app.run(debug=True, host="10.1.0.10", port=80)


if __name__ == '__main__':
    _run()
