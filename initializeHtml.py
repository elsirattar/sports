from encrypted import Connection


class ShowHtml(Connection):
    def __init__(self):
        self.connector()
        print('html')
        self.setup()
        self.last_html_barcode()

    def setup(self):
        self.cr.execute('SELECT  name ,code FROM item ')
        barcodes = self.cr.fetchall()

        file = open('barcode.html', 'w')
        message = '''<!DOCTYPE html>
                <html lang='ar'>
                <meta http-equiv="Content-Type" ;charset=UTF-8">
                <link rel="stylesheet" href="bootstrap.min.css">
                <head>
                </head>
                <div class= "row">
                '''
        for barcode in barcodes:
            name = barcode[0]
            barcode_ = barcode[1]
            message = message + f'''
                    <div class="card" style="width: 16rem;" >
                        <p class="text-primary text-center">{name}</p>
                        <img src="barcodes/{name}.png" class="card-img-top" alt="{barcode_}">
                    </div>
                    
                </body>
                </html>
            '''
        file.write(message)

    def last_html_barcode(self):
        file = open(f'last.html', 'w')
        heading = '''<!DOCTYPE html>
            <html lang='ar'>
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
            <meta http-equiv="Content-Language" content="fa" />
            <head>
                <title>Bar code</title>
            </head>
            <body>
        '''

        heading = heading + f'''
        <div style="width:38mm;height:25mm" onLoad='window.print()'>   
            <img 
                src="barcode.png"
                alt="barcode" />
        </div>
        </body>
        </html>
        '''

        file.write(heading)
# a = ShowHtml()