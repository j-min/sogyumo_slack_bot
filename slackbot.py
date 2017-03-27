from slacker import Slacker
import websocket
import json
import logging

joined_text = '자기소개 sheet입니다 들어가셔서 본인 이름이랑 관심분야, 키워드 등 빈칸 좀 채워주세요.\
    https://docs.google.com/spreadsheets/d/1BL5pV9IPvrpSyGN_GKsCGKQy5O2nuVgawTtNnxw47RI/edit?usp=sharing'

invitation = '새로 오신 분들은 invitation 채널 가셔서 초대해달라고 하시면 디스커스에 초대됩니다.'


class slackbot:
    def __init__(self, token):
        self._token = token
        self.slack = Slacker(token)

        response = self.slack.rtm.start()
        endpoint = response.body['url']
        self.socket = websocket.create_connection(endpoint)

    def recv(self):
        data = self.socket.recv()
        return json.loads(data)

    def send(self, message):
        attachments_dict = dict()
        attachments_dict['pretext'] = ""
        attachments_dict['title'] = ""
        attachments_dict['title_link'] = ""
        attachments_dict['fallback'] = ""
        attachments_dict['text'] = message
        attachments_dict['mrkdwn_in'] = []
        attachments = [attachments_dict]

        self.slack.chat.post_message(channel='#general', text=None, attachments=attachments, as_user=True)



if __name__ == '__main__':
    token = open('./token').read()[:-1]
    logging.basicConfig(filename='./log',level=logging.DEBUG)

    bot = slackbot(token)
    bot.send('소규모 논문 봇 실행\nhttps://github.com/FuZer/sogyumo_slack_bot')

    while True:
        data = bot.recv()
        logging.info(data)

        if data['type'] == 'member_joined_channel'and data['channel'] == 'C3R7L8SKT':
            bot.send('환영합니다!')
            bot.send(joined_text)
            bot.send(invitation)
