import configparser

config = configparser.ConfigParser()
# config.read('settings.ini')
config.add_section('Language')
config.set('Language', 'Current', 'English')
config.add_section('Shortcut')
config.set('Shortcut', 'Shortcut1', 'P')
config.set('Shortcut', 'Shortcut2', 'Q')
with open('settings.ini', 'w') as f:
    config.write(f)
