import xml.etree.ElementTree as ET

# Парсинг XML файла
tree = ET.parse('last.xml')
root = tree.getroot()

# Имя пространства имен
namespace = '{kaspiShopping}'
i=0
# Добавление строки во все элементы <cityprices>
for cityprices in root.findall('.//{}cityprices'.format(namespace)):

    print(i)
    # Получение значения для cityprice
    cityprice_value = root.find('.//{}cityprice[@cityId="750000000"]'.format(namespace)).text

    # Добавление строки в текущий элемент <cityprices>
    new_cityprice = ET.Element(namespace + 'cityprice')
    new_cityprice.set('cityId', '552210000')
    new_cityprice.text = cityprice_value
    cityprices.append(new_cityprice)
    i= i+1

# Запись изменений обратно в файл
tree.write('FINAL.xml', encoding='utf-8', xml_declaration=True)
