#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from slugify import slugify

material_guidelines_url = 'http://www.google.com/design/spec/style/color.html#color-color-palette'
output_file = 'generated/_material-colors.scss'

foreground_color_light = '#ffffff'
foreground_color_dark = '#000000'


def print_scss_map(output_handle, name, keys, values):
    output_handle.write('$' + name + ': (\n')

    longest_key = max(len(key) for key in keys)
    pattern = '    "{key}": {indent}{value},\n'

    for key, value in zip(keys, values):
        output_handle.write(fill_placeholders(pattern, {
            'key': key,
            'value': value,
            'indent': ' ' * (longest_key - len(key))
        }))

    output_handle.write(');\n')


def print_scss_vars(output_handle, names, values):
    indent = max(len(name) for name in names)
    pattern = '${var_name}: {indent}{value};\n'

    for name, value in zip(names, values):
        output_handle.write(fill_placeholders(pattern, {
            'var_name': name,
            'value': value,
            'indent': ' ' * (indent - len(name))
        }))


def has_class(element, classname):
    class_attr = element.get('class')

    if class_attr is None:
        return False

    return classname in class_attr


def fill_placeholders(string, dict):
    for what, with_what in dict.items():
        string = string.replace('{' + what + '}', with_what)

    return string


# Download & parse guidelines HTML
response = urllib.request.urlopen(material_guidelines_url)
data = response.read()
raw_html = data.decode('utf-8')
parsed_html = BeautifulSoup(raw_html, 'html.parser')

# Parse it!
html_palette = parsed_html.body.find('div', attrs={'class': 'color-palette'})
color_groups = html_palette.find_all('section', attrs={'class', 'color-group'})
colors = []

for color_group in color_groups:
    name_span = color_group.find(attrs={'class', 'name'})
    # We skip black + white colors
    if name_span is None:
        continue

    color_name = name_span.text
    color_slug = slugify(color_name)

    # Find each shade
    html_shades = color_group.find_all('li')
    shades = []

    for shade in html_shades:
        if has_class(shade, 'main-color'):
            continue

        shade_name = shade.find(attrs={'class', 'shade'}).text
        hex = shade.find(attrs={'class', 'hex'}).text
        foreground = foreground_color_dark if has_class(shade, 'dark') else foreground_color_light

        shades.append({
            'name': shade_name,
            'hex': hex,
            'foreground': foreground,
        })

    colors.append({
        'name': color_name,
        'slug': color_slug,
        'shades': shades
    })

# Print vars & map definitions to output file
with open(output_file, 'w') as output:
    output.truncate()

    output.writelines('\n'.join([
        "/**",
        " * Material-Colors-SCSS-Variables",
        " * https://github.com/chteuchteu/Material-Colors-SCSS-Variables",
        " */\n\n"
    ]))

    for color in colors:
        color_name = color['name']
        color_slug = color['slug']
        shades = color['shades']

        # Write to file
        output.writelines('\n'.join([
            '//',
            '// ' + color_name,
            '//',
            ''
        ]))

        # Map
        print_scss_map(output, 'color-' + color_slug + '-list',
                        [shade['name'] for shade in shades],
                        [shade['hex'] for shade in shades])

        output.write('\n')

        # Separate colors
        # Main shade
        main_shade = next(shade for shade in shades if shade['name'] == '500')
        print_scss_vars(output, ['color-' + color_slug], [main_shade['hex']])
        output.write('\n')

        # All shades
        print_scss_vars(output,
                        ['color-' + color_slug + '-' + shade['name'] for shade in shades],
                        [shade['hex'] for shade in shades])

        # Foreground color
        output.writelines('\n'.join([
            '',
            '// Foreground',
            ''
        ]))
        print_scss_map(output, 'color-' + color_slug + '-foreground-list',
                        [shade['name'] for shade in shades],
                        [shade['foreground'] for shade in shades])

        output.write('\n')

        # Separate colors
        # Main shade
        main_shade = next(shade for shade in shades if shade['name'] == '500')
        print_scss_vars(output, ['color-' + color_slug + '-foreground'], [main_shade['hex']])
        output.write('\n')

        print_scss_vars(output,
                        ['color-' + color_slug + '-' + shade['name'] + '-foreground' for shade in shades],
                        [shade['hex'] for shade in shades])

        output.write('\n\n')

    # Print a map of all colors
    print_scss_map(output, 'colors',
                   [color['slug'] for color in colors],
                   ['$color-' + color['slug'] + '-list' for color in colors])

colors_count = len(colors)
shades_count = sum([len(color['shades']) for color in colors])
print(output_file + ' created, containing ' + str(colors_count) + ' colors and ' + str(shades_count) + ' shades')
