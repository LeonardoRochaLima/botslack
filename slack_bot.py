from slacker import Slacker
import slack

def test():

    slack = Slacker('xoxb-79246075239-806774446849-dfs4awvpcbUGQdHEgwTeVAJS')

    #Enviando mensagem para o grupo #pautriste
    message = "olá , eu sou o Goku"
    slack.chat.post_message('#testingchatbot', message)

    slack_token = ["SLACK_API_TOKEN"]
    client = slack.WebClient(slack_token)

    client.conversations_member(channel="#testingchatbot")

if __name__ == "__main__":
    test()



