# file --filesystem.py--
import os


def load_receivers():
    if not os.path.isfile("Destinataires.txt"):
        open("Destinataires.txt", "x", encoding="utf-8").close()
    return open("Destinataires.txt", "r", encoding="utf-8").read()


def load_message():
    if not os.path.isfile("Message.txt"):
        msg_config = open("Message.txt", "x", encoding="utf-8")
        msg_config.write("[Sujet]\n\n[Message]\n")
        msg_config.close()
    msg_config = [line.rstrip('\n') for line in open("Message.txt", "r", encoding="utf-8")]
    title_index = msg_config.index("[Sujet]")
    message_index = msg_config.index("[Message]")
    title = msg_config[title_index + 1:message_index][0]
    message = "\n".join(msg_config[message_index + 1:])
    return title, message


def save_receivers(names_list):
    open("Destinataires.txt", "w", encoding="utf-8").write(names_list)


def save_message(title, message):
    open("Message.txt", "w", encoding="utf-8").write(
        "[Sujet]\n" + title + "\n[Message]\n" + message.replace("\r", ""))