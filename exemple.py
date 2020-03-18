from flask import Flask, request, make_response, Response
import os
import json

from slackclient import SlackClient

SLACK_BOT_TOKEN = os.environ["xoxb-79246075239-806774446849-dfs4awvpcbUGQdHEgwTeVAJS"]
SLACK_VERIFICATION_TOKEN = os.environ["SLACK_VERIFICATION_TOKEN"]

# Slack client for WEB API requests
slack_client = SlackClient("xoxb-79246075239-806774446849-dfs4awvpcbUGQdHEgwTeVAJS")

app = Flask("API Service")

COFFEE_ORDERS = {}

user_id = "LeonardoLima"
order_dm = slack_client.api_call("chat.postMessage",
                                 as_user=True,
                                 channel = user_id,
                                 text = "Sou seu Coffeebot::robot_face:: Eu\' estou aqui para te ajudar a se refrescar com um pouco de café :coffee:",
                                 attachments=[{
                                     "text":"",
                                     "callback_id": user_id + "coffee_order_form",
                                     "color": "#3AA3E3",
                                     "actions":[{
                                         "name": "coffee_order",
                                         "text": ":coffee: Order Coffee",
                                         "type": "button",
                                         "value": "coffee_order"
                                     }]
                                 }]
                                 )
COFFEE_ORDERS[user_id]={
    "order_channel": order_dm["channel"],
    "message_ts": "Acorda",
    "order": {}
}

@app.route("/slack/message_actions", methods=["POST"])
def message_actions():
    # Parse the request payload
    message_action = json.loads(request.form["payload"])
    user_id = message_action["user"]["id"]

    if message_action["type"] == "interactive_message":
        # Add the message_ts to the user's order info
        COFFEE_ORDERS[user_id]["message_ts"] = message_action["message_ts"]

        # Show the ordering dialog to the user
        open_dialog = slack_client.api_call(
            "dialog.open",
            trigger_id=message_action["trigger_id"],
            dialog={
                "title": "Request a coffee",
                "submit_label": "Submit",
                "callback_id": user_id + "coffee_order_form",
                "elements": [
                    {
                        "label": "Coffee Type",
                        "type": "select",
                        "name": "meal_preferences",
                        "placeholder": "Select a drink",
                        "options": [
                            {
                                "label": "Cappuccino",
                                "value": "cappuccino"
                            },
                            {
                                "label": "Latte",
                                "value": "latte"
                            },
                            {
                                "label": "Pour Over",
                                "value": "pour_over"
                            },
                            {
                                "label": "Cold Brew",
                                "value": "cold_brew"
                            }
                        ]
                    }
                ]
            }
        )

        print(open_dialog)

        # Update the message to show that we're in the process of taking their order
        slack_client.api_call(
            "chat.update",
            channel=COFFEE_ORDERS[user_id]["order_channel"],
            ts=message_action["message_ts"],
            text=":pencil: Taking your order...",
            attachments=[]
        )

    elif message_action["type"] == "dialog_submission":
        coffee_order = COFFEE_ORDERS[user_id]

        # Update the message to show that we're in the process of taking their order
        slack_client.api_call(
            "chat.update",
            channel=COFFEE_ORDERS[user_id]["order_channel"],
            ts=coffee_order["message_ts"],
            text=":white_check_mark: Order received!",
            attachments=[]
        )

    return make_response("", 200)


if __name__ == "__main__":
    app.run()
