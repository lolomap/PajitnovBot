import sys


def main():
    logpath = sys.argv[1]
    uuid = sys.argv[2]
    file = open(logpath, 'r', encoding='utf-8')
    log = file.read()
    start_id = log.find(uuid)+len(uuid)
    end_id = log.find('UUID', start_id)
    ch_log = log[start_id+1:end_id]
    print(ch_log)


if __name__ == '__main__':
    main()
