# Material Colors as SCSS Variables
The other libraries lacked foreground (text) color information, so I wrote this.
The `generate.py` downloads & parses Material Design guidelines's color palette
in order to generate [`generated/_material-colors.scss`](https://github.com/chteuchteu/Material-Colors-SCSS-Variables/blob/master/generated/_material-colors.scss).

# How to use this
Copy [`generated/_material-colors.scss`](https://github.com/chteuchteu/Material-Colors-SCSS-Variables/blob/master/generated/_material-colors.scss)
into your project, and import it into your scss file:

    # style.scss
    
    # Import colors
    @import 'material-colors.scss';
    
    .button {
        background-color: $color-blue;
        color: $color-blue-foreground;
    }

# How to update this
We're using BeautifulSoup & python-slugify to parse Google Material Guidelines:

    pip install beautifulsoup4
    pip install python-slugify

Once these dependencies are installed, you can run `generate.py`:

    > python generate.py
    
    # generated/_material-colors.scss created, containing 19 colors and 254 shades
