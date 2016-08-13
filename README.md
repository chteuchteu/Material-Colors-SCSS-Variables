# Material Colors as SCSS Variables
The other libraries lacked foreground (text) color information, so I wrote this.
The `generate.py` downloads & parses Material Design guidelines's color palette
in order to generate [`dist/_material-colors.scss`](https://github.com/chteuchteu/Material-Colors-SCSS-Variables/blob/master/dist/_material-colors.scss).

# How to use this

```scss
$color-primary: $color-blue-700;

.notice.danger {
    background-color: $color-red-700;
    color: $color-red-700-foreground;
}
```

### Using bower
1. Add bower depency

    ```bash
    bower install --save material-scss-colors
    ```

2. Reference SCSS part file using relative path

    ```scss
    /* style.scss */
    @import '../../../bower_components/material-scss-colors/dist/material-colors';
    ```

### Manually
1. Copy [`dist/_material-colors.scss`](https://github.com/chteuchteu/Material-Colors-SCSS-Variables/blob/master/dist/_material-colors.scss)
into your project

2. Import it into your SCSS file(s)

    ```scss
    /* style.scss */
    @import 'material-colors';
    ```

# How to update this

> Note: you usually don't want to do that, except if some colors are missing from the generated file.

We're using BeautifulSoup & python-slugify to parse Google Material Guidelines:

```bash
pip install beautifulsoup4
pip install python-slugify
```

Once these dependencies are installed, you can run `generate.py`:

```bash
> python generate.py

# generated/_material-colors.scss created, containing 19 colors and 254 shades
```
