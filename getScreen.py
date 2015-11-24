#!/usr/bin/env python

from datadog import initialize, api
import json
import sys

KEYS = {'prod' : {'API' : 'key1' , 'APP' : 'app1'},
        'personal' : {'API' : 'key2' , 'APP' : 'app2'},
        'staging' : {'API' : 'key3' , 'APP' : 'app3'}
        }

def keys(x):
    return KEYS[x]

def main(board_id):
    # Prompt for keys (don't store them in git)
    print "prod, staging, or personal account? [type name]: "
    case = raw_input()
    try: #New line will raise an exception
        if case not in KEYS.keys():
            main(board_id)
    except AttributeError:
        main(board_id)
    except KeyError:
        pass

    options = {
        'api_key': keys(case)['API'],
        'app_key': keys(case)['APP']
    }
    initialize(**options)    

    try:
        result = api.Screenboard.get(board_id)
    except:
        print "Invalid board id. Quitting"
        return -1
        
    if 'errors' in result:
        print "Invalid board id. Maybe try a different account?\n Quitting..."
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

