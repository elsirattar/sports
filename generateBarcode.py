import code128
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import bidi.algorithm, arabic_reshaper
from encrypted import Connection


class Barcode_generator(Connection):
    def __init__(self):
        self.connector()
        print('code Generator')
        self.insert_new_barcode()
        self.save_image()
        self.execute_editing_image()

    def readCode(self):
        try:
            self.cr.execute('SELECT  bars from barcodes WHERE id=(SELECT MAX(id)FROM barcodes); ')
            sn = self.cr.fetchone()[0]
            return sn

        except:
            """
            if there isn't barcode yet , then insert one to barcodes table and select it after
            """
            self.cr.execute('INSERT INTO barcodes(bars) VALUES(%s)', (1000,))
            self.db.commit()
            print('first barcode added successfully')
            self.cr.execute('SELECT  bars from barcodes WHERE id=(SELECT MAX(id)FROM barcodes); ')
            sn = self.cr.fetchone()[0]
            return sn

    def insert_new_barcode(self):
        self.cr.execute(f'''INSERT INTO barcodes(bars)VALUES ('{int(self.readCode()) + 1}') ''')
        self.db.commit()
        print('barcode inserted')

    def save_image(self):
        print('saved barcode.png')
        code128.image(self.readCode()).save("barcode.png")

    def expand2square(self, pil_img, background_color):
        width, height = pil_img.size
        if width == height:
            return pil_img
        elif width > height:
            result = Image.new(pil_img.mode, (width, width), background_color)
            result.paste(pil_img, (0, (width - height) // 2))
            return result
        else:
            result = Image.new(pil_img.mode, (height, height), background_color)
            result.paste(pil_img, ((height - width) // 2, 0))
            return result

    def execute_editing_image(self):
        im = Image.open('barcode.png')
        im_new = self.expand2square(im, 200).resize((145, 94))
        im_new.save('barcode.png', quality=100)
        print('saved expanded barcode.png')

    def write_on_barcode(self, price, code,name):
        self.cr.execute('SELECT name  FROM info')
        item = self.cr.fetchone()
        reshaper = arabic_reshaper.reshape(item[0])
        name_ = bidi.algorithm.get_display(reshaper)
        print(name_)
        self.price = price
        self.name = name
        self.code = code
        fontFile = "bein-ar-normal_0.ttf"
        font = ImageFont.truetype(fontFile, 12)
        img = Image.open('barcode.png')
        draw = ImageDraw.Draw(img)
        draw.text((5, 5), f' {name_}', font=font)
        draw.text((80, 5), f'{self.price}  L.E', font=font)
        draw.text((50, 62), f'{self.code}', font=font)
        img.save('barcode.png',quality=95)
        img.save(f'barcodes/{self.name}.png',quality=95)
        print('saved last edit of barcode.png and one for barcodes folder')
