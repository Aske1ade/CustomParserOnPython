if __name__ == "__main__":
    data = [['Apple iPhone 14 Pro Max 512Gb фиолетовый', 'Apple iPhone 14 256Gb голубой', 'Apple iPhone 15 256Gb голубой', 'Apple iPhone 11 128Gb Slim Box черный', 'Apple iPhone 15 128Gb черный', 'Apple iPhone 14 Pro 512Gb фиолетовый', 'Apple iPhone 14 128Gb черный', 'Apple iPhone 14 Pro Max 128Gb фиолетовый', 'Apple iPhone 15 256Gb черный', 'Apple iPhone 14 128Gb голубой', 'Apple iPhone 15 Pro Max 1Tb белый', 'Apple iPhone 14 Pro Max 256Gb фиолетовый', 'Apple iPhone 14 Pro Max 512Gb черный', 'Apple Watch Series 8 45 мм Aluminum золотистый', 'Apple Watch Series 8 45 мм Aluminum черный', 'Apple iPhone 14 256Gb черный', 'Apple iPhone 11 128Gb Slim Box белый', 'Apple iPhone 15 128Gb голубой', 'Apple iPhone 15 Pro 256Gb черный', 'Apple iPhone 15 Pro Max 512Gb серый'], ['https://kaspi.kz/shop/p/apple-iphone-14-pro-max-512gb-fioletovyi-106363344/', 'https://kaspi.kz/shop/p/apple-iphone-14-256gb-goluboi-106363155/', 'https://kaspi.kz/shop/p/apple-iphone-15-256gb-goluboi-113137931/', 'https://kaspi.kz/shop/p/apple-iphone-11-128gb-slim-box-chernyi-100692388/', 'https://kaspi.kz/shop/p/apple-iphone-15-128gb-chernyi-113137790/', 'https://kaspi.kz/shop/p/apple-iphone-14-pro-512gb-fioletovyi-106363322/', 'https://kaspi.kz/shop/p/apple-iphone-14-128gb-chernyi-106363023/', 'https://kaspi.kz/shop/p/apple-iphone-14-pro-max-128gb-fioletovyi-106363303/', 'https://kaspi.kz/shop/p/apple-iphone-15-256gb-chernyi-113137897/', 'https://kaspi.kz/shop/p/apple-iphone-14-128gb-goluboi-106363150/', 'https://kaspi.kz/shop/p/apple-iphone-15-pro-max-1tb-belyi-113138629/', 'https://kaspi.kz/shop/p/apple-iphone-14-pro-max-256gb-fioletovyi-106363342/', 'https://kaspi.kz/shop/p/apple-iphone-14-pro-max-512gb-chernyi-106363293/', 'https://kaspi.kz/shop/p/apple-watch-series-8-45-mm-aluminum-zolotistyi-106585021/', 'https://kaspi.kz/shop/p/apple-watch-series-8-45-mm-aluminum-chernyi-106362847/', 'https://kaspi.kz/shop/p/apple-iphone-14-256gb-chernyi-106363112/', 'https://kaspi.kz/shop/p/apple-iphone-11-128gb-slim-box-belyi-100692385/', 'https://kaspi.kz/shop/p/apple-iphone-15-128gb-goluboi-113137929/', 'https://kaspi.kz/shop/p/apple-iphone-15-pro-256gb-chernyi-113138191/', 'https://kaspi.kz/shop/p/apple-iphone-15-pro-max-512gb-seryi-113138461/'], ['106363344_560676', '106363155_433942', '113137931_236384', '100692388_525820', '113137790_547931', '106363322_493494', '106363023_142310', '106363303_467856', '113137897_749019', '106363150_721723', '113138629_687978', '106363342_763641', '106363293_730593', '106585021_558719', '106362847_869637', '106363112_544996', '100692385_613957', '113137929_607941', '113138191_980611', '113138461_778497'], ['PP5, PP4', 'PP5, PP4', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5', 'PP5'], '250000,145120', '222222,333333', '250000', '209080', '400000', '223323', '401010', '650020', '89000', '90000', '1000000', '146365', '899980', '917000', '235000', '699445', '998808', '960000', '750000', '876865']


    # Разделение данных на отдельные списки
    new_data = []

    for i in range(len(data[0])):
        item = []
        for j in range(len(data)):
            if i < len(data[j]):
                if isinstance(data[j][i], str) and ',' in data[j][i]:
                    item.extend(data[j][i].split(','))
                else:
                    item.append(data[j][i])
        new_data.append(item)

    for item in new_data:
        print(item)

        """
        Аккорд, Антей, Бетти, Блистер, Бриз, Вояж, Квин, Линкольн, Марокко, Ривьера, Рим, Сенатор, Спинер, Татьяна, Фидэль, Флорида
        """
