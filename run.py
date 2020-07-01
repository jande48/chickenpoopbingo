from ChickenShitBingo import app


# This means that if we run this program with python, debug will be true, but in a prod server it will be false
if __name__ == '__main__':
    app.run(debug=True)


