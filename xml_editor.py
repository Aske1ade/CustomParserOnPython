import xml.etree.ElementTree as ET

# Парсинг XML файла
tree = ET.parse('blya.xml')
root = tree.getroot()

# Имя пространства имен
namespace = '{kaspiShopping}'

# Добавление атрибута preOrder="15" в каждый элемент <availability>
for availabilities in root.findall('.//{}availabilities'.format(namespace)):
    for availability in availabilities.findall('.//{}availability'.format(namespace)):
        availability.set('preOrder', '20')

# Запись изменений обратно в файл
tree.write('edited_xml_file.xml', encoding='utf-8', xml_declaration=True)