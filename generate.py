#!/usr/bin/python3
# -*- coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from slugify import slugify

material_guidelines_url = 'http://www.google.com/design/spec/style/color.html#color-color-palette'
output_file = 'generated/_material-colors.scss'

foreground_color_light = '#ffffff'
foreground_color_dark = '#000000'


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

# Open output file
with open(output_file, 'w') as output:
    output.truncate()

    output.writelines('\n'.join([
        "/**",
        " * Material-Colors-SCSS-Variables",
        " * https://github.com/chteuchteu/Material-Colors-SCSS-Variables",
        " */\n\n"
    ]))

    # Parse it!
    html_palette = parsed_html.body.find('div', attrs={'class': 'color-palette'})
    color_groups = html_palette.find_all('section', attrs={'class', 'color-group'})

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

        # Write to file
        output.writelines('\n'.join([
            '//',
            '// ' + color_name,
            '//',
            ''
        ]))
        longest_key = max(len(shade['name']) for shade in shades)  # Pretty indentation

        # List
        pattern_list_item = '    "{shade_name}": {indent}{hex},\n'
        list_name = '$color-' + color_slug + '-list'
        output.write(list_name + ': (\n')

        for shade in shades:
            output.write(fill_placeholders(pattern_list_item, {
                'shade_name': shade['name'],
                'indent': ' ' * (longest_key - len(shade['name'])),
                'hex': shade['hex']
            }))

        output.write(');\n\n')

        # Separate colors
        pattern_variable = '$color-{var_name}: {indent}map-get({color_list_name}, "{shade_name}");\n'

        # Main shade
        main_shade = next((shade for shade in shades if shade['name'] == '500'))
        output.write(fill_placeholders(pattern_variable, {
            'var_name': color_slug,
            'shade_name': main_shade['name'],
            'indent': ' ' * (longest_key + 1),
            'color_list_name': list_name
        }))
        output.write('\n')

        for shade in shades:
            output.write(fill_placeholders(pattern_variable, {
                'var_name': color_slug + '-' + shade['name'],
                'shade_name': shade['name'],
                'indent': ' ' * (longest_key - len(shade['name'])),
                'color_list_name': list_name
            }))

        # Foreground color
        foreground_color_list_name = list_name + '-foreground'
        output.writelines('\n'.join([
            '',
            '// Foreground',
            foreground_color_list_name + ': (\n'
        ]))

        for shade in shades:
            output.write(fill_placeholders(pattern_list_item, {
                'shade_name': shade['name'],
                'indent': ' ' * (longest_key - len(shade['name'])),
                'hex': shade['foreground']
            }))

        output.write(');\n\n')

        # Separate colors
        pattern_variable_foreground = '$color-{var_name}-foreground: {indent}map-get({foreground_color_list_name}, "{shade_name}");\n'

        # Main shade
        output.write(fill_placeholders(pattern_variable_foreground, {
            'var_name': color_slug,
            'shade_name': main_shade['name'],
            'indent': ' ' * (longest_key + 1),
            'foreground_color_list_name': foreground_color_list_name
        }))
        output.write('\n')

        for shade in shades:
            output.write(fill_placeholders(pattern_variable_foreground, {
                'var_name': color_slug + '-' + shade['name'],
                'shade_name': shade['name'],
                'indent': ' ' * (longest_key - len(shade['name'])),
                'foreground_color_list_name': foreground_color_list_name
            }))

        output.write('\n\n')
