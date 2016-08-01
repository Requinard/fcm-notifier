import json
import argparse
from pyfcm import FCMNotification


def main():
    configs = None

    # Load configs
    try:
        configs = json.load(open("config.json"))
    except FileNotFoundError:
        print("There are no configs yet!")
        return 1

    # Parse args
    args = vars(get_parser().parse_args())

    # see if we have a valid config
    config = [x for x in configs if x["name"] == args["n"]]

    if (len(config) == 0):
        print("There is no such config!")
        return 2
    else:
        config = config[0]
        print("Config found")

    # See if config has the stuff we need
    if "api_key" not in config.keys():
        print("No api key found")
        return 3

    if "topics" not in config.keys():
        print("No topics found")
        return 4

    if args["t"] not in config["topics"]:
        print("topic does not exist!")
        return 5

    print("notifying")
    notify(config["api_key"], args["m"], args["t"], args["ti"])


def get_parser():
    parser = argparse.ArgumentParser(description="Send FCM messages without it eating everything")
    parser.add_argument("-n", metavar="<name>", help="name")
    parser.add_argument("-m", metavar="<message>", help="message")
    parser.add_argument("-t", metavar="topic", help="Topic")
    parser.add_argument("-ti", metavar="title", help="Title to send")

    return parser


def notify(api_key: str, message: str, topic: str, title: str, data: object = {}):
    """
    Notifies a topic
    :param api_key: Api key to send to
    :param message:  Message that should be notified (optional)
    :param topic: Topic that message should be sent to
    :param title: Title of the message
    :param data: Extra data to send (optional)
    """
    push_service = FCMNotification(api_key=api_key)

    if message is not None:
        data['message'] = message

    if title is not None:
        data['title'] = title

    result = push_service.notify_topic_subscribers(topic_name=topic, data_message=data)

    print(result)


if __name__ == "__main__":
    main()
