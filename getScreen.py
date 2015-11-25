#!/usr/bin/env python

from datadog import initialize, api
import json
import sys

def main(board_id):
    #Configure keys in settings.json

    keys = json.load(open("settings.json"))

    #List keys and wait for input:
    case = raw_input("[ " + " ".join(keys.keys()) + " ]: ")

    try:
        options = {
            'api_key': keys[case]['API'],
            'app_key': keys[case]['APP']
        }
    except KeyError:
        print "Invalid key"
        return -1

    initialize(**options)    

    try:
        result = api.Screenboard.get(board_id)
    except:
        print "Invalid board id. Quitting"
        return -1
        
    if 'errors' in result:
        print "\nInvalid board id. Maybe try a different account?\nQuitting..."
        return -1
        
    with open( str(board_id) + '_screen.txt', 'w') as file:
        file.write(json.dumps(result))
    print "Board " + str(board_id) + " saved"

if __name__ == '__main__':
    if len(sys.argv) < 2:
        board_id = raw_input("board ID: ")
    else:
        board_id = sys.argv[1]
    main(board_id)
