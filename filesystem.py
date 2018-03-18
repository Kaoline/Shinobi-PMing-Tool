# file --filesystem.py--
import os

import constants


def load_receivers():
    if not os.path.isfile("Destinataires.txt"):
        open(constants.default_receivers_file, "x", encoding="utf-8").close()
    return open(constants.default_receivers_file, "r", encoding="utf-8").read()


def load_message():
    if not os.path.isfile(constants.default_message_file):
        msg_config = open(constants.default_message_file, "x", encoding="utf-8")
        msg_config.write("[Sujet]\n\n[Message]\n")
        msg_config.close()
    msg_config = [line.rstrip('\n') for line in open(constants.default_message_file, "r", encoding="utf-8")]
    title_index = msg_config.index("[Sujet]")
    message_index = msg_config.index("[Message]")
    title = msg_config[title_index + 1:message_index][0]
    message = "\n".join(msg_config[message_index + 1:])
    return title, message


def save_receivers(names_list):
    open(constants.default_receivers_file, "w", encoding="utf-8").write(names_list)


def save_message(title, message):
    open(constants.default_message_file, "w", encoding="utf-8").write(
        "[Sujet]\n" + title + "\n[Message]\n" + message.replace("\r", ""))