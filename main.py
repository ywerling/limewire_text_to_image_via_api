import tkinter as tk
import requests
# import os
import json
import webbrowser

LIMEWIRE_ENDPOINT = "https://api.limewire.com/api/image/generation"
LIMEWIRE_SUCCESS = 'COMPLETED'

class TextToImageApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # create the tkinter UI basic structure
        self.config(padx=600, pady=300)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)

        #put widgets on the grid
        self.prompt_label = tk.Label(text="Prompt")
        self.prompt_label.grid(column=0, row=0)
        self.prompt_entry = tk.Entry(width=50)
        self.prompt_entry.grid(column=1, row=0)
        self.generate_button = tk.Button(width=20, height=1, text="Generate Image", command=self.generate_image)
        self.generate_button.grid(column=0, row=1)
        self.open_browser_button = tk.Button(width=20, height=1, text="Open Image in Browser", command=self.open_browser)
        self.open_browser_button.grid(column=1, row=2)
        self.image_url_entry = tk.Entry(width=75)
        self.image_url_entry.grid(column=2, row=2)

        response_labels_text = ['status','failure_code','failure_reason','credits_used','credits_remaining']
        for i, resp in enumerate(response_labels_text):
            tk.Label(self.parent, text=resp).grid(row=i, column=3)

    def generate_image(self):
        print("generate image")
        # api_key = os.getenv('LIMEWIRE_API_KEY')

        with open('config.json') as config_file:
            config = json.load(config_file)
            api_key = config['api_key']

        prompt_text = self.prompt_entry.get()

        # prepare payload for API request
        payload = {
            "prompt": prompt_text,
            "aspect_ratio": "1:1"
        }
        headers = {
            "Content-Type": "application/json",
            "X-Api-Version": "v1",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # post API request
        response = requests.post(LIMEWIRE_ENDPOINT, json=payload, headers=headers)
        data = response.json()
        print(data)

        # image url is asset_url

        # sample response used to test without using API credits
        # data = {'id': '6286bc48-f936-4663-951b-2f3bd3a42d56',
        #  'self': 'https://api.limewire.com/api/request/6286bc48-f936-4663-951b-2f3bd3a42d56', 'status': 'COMPLETED',
        #  'failure_code': None, 'failure_reason': None, 'credits_used': 0.99, 'credits_remaining': 8.0199995, 'data': [
        #     {'asset_id': 'f03b36ed-c9de-480e-b2dc-290c6608533e',
        #      'self': 'https://api.limewire.com/api/assets/f03b36ed-c9de-480e-b2dc-290c6608533e',
        #      'asset_url': 'https://ai-studio-assets.limewire.media/u/9ff0ef66-17d0-4ef0-9b96-cf1cea9e1709/image/11ef0397-8c2f-4136-99d9-35c3c98a8f4b?Expires=1716026695&Signature=LAoEc7UXVpgWYgHYRDmWKaFDvnM1XzB-BEvG1eQWD9xvZnT0-Ag75nL4Xv~vjs~8MAF~rvIE1QhmhFb87bCa8bZfyAf-Vr7rc1Q7ENF1sMivkINGTYITmXSKnnT6IvV93CPveTlsYjWjbPjofO7Mdz537mw1GBkVk94hsLjZI3w4NrWuWZfH74BASh2osW~ShfIeE0uVGbDrF8DrVF5z37uTCIBXhZaYX48eacvn6hIWPpqBzWGz57PBO1OtWkrmetK~O1rgrL4jwlEDlcJ21WyL3VzUuJon~j-1X1VqqqPsol4Eh7UjVtYVyBSibhnl2kc0XGIER2hXYY35~K2obg__&Key-Pair-Id=K1U52DHN9E92VT',
        #      'type': 'image/jpeg', 'width': 1024, 'height': 1024}]}
        # print(data)
        # print(data['data'][0]['asset_url'])

        if ( data['status'] == LIMEWIRE_SUCCESS ):
            self.image_url_entry.insert(0,data['data'][0]['asset_url'])
            webbrowser.open(data['data'][0]['asset_url'])
            print(f"Credits used: {data['credits_used']}")
            print(f"Credits remaining: {data['credits_remaining']}")
        else:
            print(f"Failure code: {data['failure_code']}")
            print(f"Failure reason: {data['failure_reason']}")

    def open_browser(self):
        print("open image in browser")
        image_url = self.image_url_entry.get()
        print(f'image url: {image_url}')


if __name__ == "__main__":
    window = tk.Tk()
    window.title = "Text to Image Application"
    TextToImageApp(window)
    window.mainloop()

    # success example
    # {'id': 'fa244ebe-fdd6-45de-a075-6c2da75cab65',
    #  'self': 'https://api.limewire.com/api/request/fa244ebe-fdd6-45de-a075-6c2da75cab65', 'status': 'COMPLETED',
    #  'failure_code': None, 'failure_reason': None, 'credits_used': 0.99, 'credits_remaining': 10.0, 'data': [
    #     {'asset_id': 'fbf6c25b-df89-4326-a9fc-5c6570158dec',
    #      'self': 'https://api.limewire.com/api/assets/fbf6c25b-df89-4326-a9fc-5c6570158dec',
    #      'asset_url': 'https://ai-studio-assets.limewire.media/u/9ff0ef66-17d0-4ef0-9b96-cf1cea9e1709/image/82d3290b-0e88-4777-add2-02c886d84e53?Expires=1716113300&Signature=AdzAQGxzzkcMS2AoaRzFAssdTyxI48Zgpc-qE9eU0YRH23iWzhkcw~6SNPXC1f13SqEbF1iLtP8S1F5Vbh1BZYm~5-GAu1WcCUjMDarQF5116KutHN5aBmafc1IhI3EzOJ3tRFZQXf0uJIgKZVM2fX0Wzk2LnbxuLLJgWLJ-yS8GV3La3a13M1XGyXB6AyVgIY77cZQtu5NaBwD7bv6jnswmLnxhawktZU3eO2Pxg5E3nIwmB1grm-8-uhDs9HjlN2BERcwtMrV7PFmKkT6QGPvDu6IqUG9KQzfte7v-0BgxucBXSOyD4DKVYeUKIq~wvcFZIxENqqs1nr-oYAPoxg__&Key-Pair-Id=K1U52DHN9E92VT',
    #      'type': 'image/jpeg', 'width': 1024, 'height': 1024}]}

