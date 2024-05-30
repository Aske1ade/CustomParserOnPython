import xml.etree.ElementTree as ET

# Парсинг XML файла
tree = ET.parse('XML.xml')
root = tree.getroot()

# Имя пространства имен
namespace = '{kaspiShopping}'

# Добавление строки в каждый элемент <availabilities>
for offer in root.findall('.//{}offer'.format(namespace)):
    # Добавление строки в текущий элемент <availabilities> в предложении
    availabilities = offer.find('.//{}availabilities'.format(namespace))
    new_availability = ET.Element(namespace + 'availability')
    new_availability.set('available', 'yes')
    new_availability.set('storeId', 'PP27')
    availabilities.append(new_availability)

# Получение значения для cityprice
for offer in root.findall('.//{}offer'.format(namespace)):
    # Получение значения для cityprice в текущем предложении
    cityprice_value = offer.find('.//{}cityprice[@cityId="750000000"]'.format(namespace)).text

    # Добавление строки в текущий элемент <cityprices> в предложении
    cityprices = offer.find('.//{}cityprices'.format(namespace))
    new_cityprice = ET.Element(namespace + 'cityprice')
    new_cityprice.set('cityId', '552210000')
    new_cityprice.text = cityprice_value
    cityprices.append(new_cityprice)

# Запись изменений обратно в файл
tree.write('blya.xml', encoding='utf-8', xml_declaration=True)