default_token = "6610941656:AAHrCB_BSZsxnV-rouK8Zh0X4e3LSG8-FOo"
default_output = "."


def help() -> None:
    print ("Use: python main.py -h -o=<output dir> -t=<telegram token>")


if __name__ == "__main__":
    from bot import Bot, Downloader
    import queue
    import getopt, sys, os
    import logging
    from pathlib import Path

    logging.basicConfig(stream=sys.stdout, encoding='utf-8', format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    # Get full command-line arguments
    full_cmd_arguments = sys.argv
    argument_list = full_cmd_arguments[1:]

    short_options = "ho:t:"
    long_options = ["help", "output=", "token="]

    try:
        arguments, values = getopt.getopt(argument_list, short_options, long_options)
    except getopt.error as err:
        # Output error, and return with an error code
        print(str(err))
        sys.exit(2)

    token = None
    output = None

    for current_argument, current_value in arguments:
        if current_argument in ("-h", "--help"):
            help()
            sys.exit(1)

        if current_argument in ("-o", "--output"):
            output = current_value

        if current_argument in ("-t", "--token"):
            token = current_value

    if token is None:
        logging.info("Token is not defined, default value is used")
        token = default_token

    if output is None:
        logging.info("Output is not defined, default value is used")
        data_path = Path.cwd().joinpath("data")
        output = data_path
    else:
        output = Path(output)

    bot = Bot(token=token, output=output)
    q:queue = bot.queue()
    Downloader(q, bot).start()
    Downloader(q, bot).start()
    Downloader(q, bot).start()
    bot.run()