# This file contains usefull functions used by clients and wizard programs.
# It is necessary module of gui_client.py and gui_wizard.py and should not be run directly.


def receive(client, nickname):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "!NICK":
                client.send(nickname.encode("utf-8"))
            else:
                return message
        except:
            print("An error occurred!")
            client.close()
            return "!SOCKET CLOSED!"


def write(client, nickname, msg, sent_by_wizard=False, is_command=False):
    if is_command:
        message = msg
    elif sent_by_wizard:
        message = f"!WIZARD{nickname}: {msg}"
    else:
        message = f"{nickname}: {msg}"
    client.send(message.encode("utf-8"))


def run(server_ip="127.0.0.1", port=55556):
    import socket

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((server_ip, port))
    return client


def natural_sort(list_to_sort):
    import re

    def atof(text):
        try:
            retval = float(text)
        except ValueError:
            retval = text
        return retval

    def natural_keys(text):
        """
        alist.sort(key=natural_keys) sorts in human order
        http://nedbatchelder.com/blog/200712/human_sorting.html
        (See Toothy's implementation in the comments)
        float regex comes from https://stackoverflow.com/a/12643073/190597
        """
        return [
            atof(c) for c in re.split(r"[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)", text)
        ]

    # Sort inplace given list using natural sort
    list_to_sort.sort(key=natural_keys)

    return list_to_sort


def send_command(client, nickname, command):
    write(client=client, nickname=nickname, msg=command, is_command=True)


def validate_entered_values(ip, port, nick):
    error_message = False
    # Try to convert string to integer
    try:
        port = int(port)
    except:
        error_message = "Server port must be an integer value!"
        return ip, port, nick, error_message
    # Check if other values are not empty
    if not ip:
        error_message = "Please enter ENDIACC II server IP address!"
        return ip, port, nick, error_message
    elif not nick:
        error_message = "Please enter your nickname!"
        return ip, port, nick, error_message
    elif ":" in nick:
        error_message = "Your nicknamecannot contain ':' character!"
        return ip, port, nick, error_message
    # If everything is allrigt return values
    return ip, port, nick, error_message


def save_backup(content):
    file_name = f"{current_time()}_backup"
    save_file(file_name=file_name, content=content)
    return file_name


def current_time():
    from datetime import datetime

    # Get current time
    current_time = datetime.now()
    # Format time
    current_time = current_time.strftime("%H-%M-%S_%d-%m-%Y")
    return current_time


def save_file(file_name, content):
    file_name = file_name + ".txt"
    with open(file_name, "w", encoding="utf8") as txt_file:
        txt_file.write(content)


def clear_dialogue(dialogue_raw, wizard_name):
    from datetime import datetime

    # Convert string into the list
    dialogue_list = dialogue_raw.split("\n")
    # Find beginning and end of the experiment
    start_index = None
    finish_index = None
    for index, line in enumerate(dialogue_list):
        if line == ">>EXPERIMENT STARTED.":
            start_index = index + 1
        if line == ">>EXPERIMENT FINISHED.":
            finish_index = index
    # Handle possible errors
    if not start_index:
        return None
    if not finish_index:
        finish_index = len(dialogue_list)
    # Remove not experiment related messages
    dialogue_list = dialogue_list[start_index:finish_index]
    # Remove possible server messagaes starting with ">>" and wizard's messages
    dialogue_list[:] = [
        x
        for x in dialogue_list
        if (not x[:2] == ">>") and (not f"{wizard_name}: " in x)
    ]
    # Determine users' nicks
    asking_user = dialogue_list[0].split(":")[0]
    answering_user = dialogue_list[1].split(":")[0]
    # Create clean dialogue list
    ## Determine time of the experiment
    exp_date = datetime.now()  # get current time
    exp_date = exp_date.strftime("%d-%m-%Y")  # format date
    ## Create file header with experiment informations
    clean_dialogue_list = [
        f"Experiment date: {exp_date}",
        f"Experimenter: {wizard_name}",
        f"Information seeker: {asking_user}",
        f"Information provider: {answering_user}",
        "",
    ]
    ## Add dialogue with numbers of question/answer sets
    question_number = 1.0
    for line in dialogue_list:
        line = line[line.index(":") + 1 :]
        clean_dialogue_list.append(f"{int(question_number)}:{line}")
        question_number += 0.5
    # Convert list to string
    clean_dialogue = "\n".join([str(x) for x in clean_dialogue_list])
    # Return clean dialogue
    return clean_dialogue


def save_dialogue_file(dialogue_raw, wizard_name):
    from datetime import datetime

    # Get formatted current time
    time = current_time()
    # Save full conversation to file (messages + server infos)
    raw_file_name = f"{time}_dialogue_raw"
    save_file(file_name=raw_file_name, content=dialogue_raw)
    # Clear dialogue and save only experimental part
    clean_dialogue = clear_dialogue(dialogue_raw, wizard_name)
    if clean_dialogue:
        clean_file_name = f"{time}_dialogue"
        save_file(file_name=clean_file_name, content=clean_dialogue)
        # return saved files' names
        return [raw_file_name, clean_file_name]
    # if experiment session was not conducted return only name of raw file
    return [raw_file_name]


if __name__ == "__main__":
    import sys

    # Execute when the module is run directly.
    print(
        "This file is necessary module of gui_client.py and gui_wizard.py and should not be run directly.\nRun gui_client.py or gui_wizard.py instead."
    )
    sys.exit()
