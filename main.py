import tkinter as tk
import requests
import os
import json

LIMEWIRE_ENDPOINT = "https://api.limewire.com/api/image/generation"

class TextToImageApp(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        # create the tkinter UI basic structure
        self.config(padx=600, pady=300)
        self.columnconfigure(0, weight=2)
        self.columnconfigure(1, weight=5)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        #put widgets on the grid
        self.prompt_label = tk.Label(text="Prompt")
        self.prompt_label.grid(column=0, row=0)
        self.prompt_entry = tk.Entry(width=50)
        self.prompt_entry.grid(column=1, row=0)
        self.generate_button = tk.Button(width=20, height=1, text="Generate Image", command=self.generate_image)
        self.generate_button.grid(column=0, row=1)
        self.image_url_entry = tk.Entry(width=75)
        self.image_url_entry.grid(column=2, row=2)

    def generate_image(self):
        print("generate image")
        # api_key = os.getenv('LIMEWIRE_API_KEY')
        # print(os.environ.get('LIMEWIRE_API_KEY'))  # This should print 'Some Value'

        with open('config.json') as config_file:
            config = json.load(config_file)
            api_key = config['api_key']

        payload = {
            "prompt": "A cute baby sea otter",
            "aspect_ratio": "1:1"
        }
        headers = {
            "Content-Type": "application/json",
            "X-Api-Version": "v1",
            "Accept": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        response = requests.post(LIMEWIRE_ENDPOINT, json=payload, headers=headers)

        data = response.json()
        print(data)
        # image url is asset_url



if __name__ == "__main__":
    window = tk.Tk()
    window.title = "Text to Image Application"
    TextToImageApp(window)
    window.mainloop()
