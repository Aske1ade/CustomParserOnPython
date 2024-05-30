import xml.etree.ElementTree as ET

# Парсинг XML файла
tree = ET.parse('edited_xml_file.xml')
root = tree.getroot()

# Удаление префикса ns0 из тегов
for elem in root.iter():
    if '}' in elem.tag:
        elem.tag = elem.tag.split('}', 1)[1]

# Имя пространства имен
namespace = ''

# Список имен для preOrder="6"
special_names = [
    "Аккорд", "Антей", "Бетти", "Блистер", "Бриз", "Вояж",
    "Квин", "Линкольн", "Марокко", "Ривьера", "Рим", "Сенатор",
    "Спинер", "Татьяна", "Фидэль", "Флорида"
]

# Добавление атрибута preOrder="6" в каждый элемент <availability> с соответствующим тегом <model>
for offer in root.findall('.//offer'):
    model = offer.find('.//model').text
    for name in special_names:
        if name in model:
            for availability in offer.findall('.//availability'):
                availability.set('preOrder', '6')
            break

# Запись изменений обратно в файл
tree.write('last.xml', encoding='utf-8', xml_declaration=True)