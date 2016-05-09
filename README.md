# Material-Colors-SCSS-Variables
Material colors as SCSS variables

The other libraries lacked foreground color information, so I wrote this.

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
