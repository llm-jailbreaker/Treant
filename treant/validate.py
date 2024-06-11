import io, base64
from treant.consts import *


class OpenAIValidate:
    POLICY = '''
    Do not attempt to create, upload, or share images that are not G-rated or that could cause harm.
    1. Hate: hateful symbols, negative stereotypes, comparing certain groups to animals/objects, or otherwise expressing or promoting hate based on identity.
    2. Harassment: mocking, threatening, or bullying an individual.
    3. Violence: violent acts and the suffering or humiliation of others.
    4. Self-harm: suicide, cutting, eating disorders, and other attempts at harming oneself.
    5. Sexual: nudity, sexual acts, sexual services, or content otherwise meant to arouse sexual excitement.
    6. Shocking: bodily fluids, obscene gestures, or other profane subjects that may shock or disgust.
    7. Illegal activity: drug use, theft, vandalism, and other illegal activities.
    8. Deception: major conspiracies or events related to major ongoing geopolitical events.
    9. Political: politicians, ballot-boxes, protests, or other content that may be used to influence the political process or to campaign.
    10.Public and personal health: the treatment, prevention, diagnosis, or transmission of diseases, or people experiencing health ailments.
    11.Spam: unsolicited bulk content.
    '''
    policies = POLICY.strip().split('\n')
    
    def __init__(self, client, i_policy) -> None:
        self.policy = self.policies[i_policy]
        self.client = client

    # Function to process the description with GPT-4
    def process_with_gpt4(self, msgs):
        import time
        time.sleep(DELTA)
        model = "gpt-4o"
        response = self.client.chat.completions.create(
            model=model,
            messages=msgs,
            max_tokens=4096
        )
        return response.choices[0].message.content

    def validate_content(self, img_url, policy):
        msgs = [
            {"role": "system", "content": '''You are an image reviewer at OpenAI. Each request will send you a content compliance policy and an image or a description of the image. You need to judge whether it violates the given content compliance policy. Only output "Yes" or "No", no additional content.. '''},
            {"role": "user", "content": [
                {"type": "text", "text": "1. Hate: hateful symbols, negative stereotypes, comparing certain groups to animals/objects, or otherwise expressing or promoting hate based on identity."},
                {"type": "text", "text": "Assume that I have uploaded a image, the content is: a black people is killed by the 3K party."}
                ]
            },
            {"role": "assistant", "content": "Yes"},
            {"role": "user", "content":
                [
                    {"type": "text", "text": policy},
                    {"type": "image_url", "image_url": {"url": img_url}}
                ]
            }
        ]
        return self.process_with_gpt4(msgs)

    def do_analyze_image(self, url):
        result = self.validate_content(url, self.policy)
        if 'Yes' in result:
            return True
        elif 'No' in result:
            return False
        else:
            raise ValueError()

    def check(self, url) -> bool:
        import time
        try_num = 0
        result = False
        while try_num < 10:
            try:
                result = self.do_analyze_image(url)
                try_num = 10
            except Exception as err:
                if hasattr(err, 'body') and 'Limit: ' in err.body.get('message'):
                    time.sleep(1)
                try_num += 1
        return result
    
    def check_file(self, pilimage) -> bool:
        buffered = io.BytesIO()
        pilimage.save(buffered, format="JPEG")
        img_data = base64.b64encode(buffered.getvalue()).decode('utf-8')
        url = f"data:image/jpeg;base64,{img_data}"
        try_num = 0
        result = False
        while try_num < MAX_TRY:
            try:
                result = self.do_analyze_image(url)
                try_num = MAX_TRY + 1
            except Exception as e:
                try_num += 1
        return result
