"""
    domonic.constants
    ====================================

"""

namespaces = {
    'xml': 'http://www.w3.org/XML/1998/namespace', 
    'svg': 'http://www.w3.org/2000/svg',
    'xlink': 'http://www.w3.org/1999/xlink',
    'xmlns': 'http://www.w3.org/2000/xmlns/',
    'xm': 'http://www.w3.org/2001/xml-events',
    'xh': 'http://www.w3.org/1999/xhtml',
    'xsl': 'http://www.w3.org/1999/XSL/Transform',
    'xsd': 'http://www.w3.org/2001/XMLSchema',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance',
    'xhtml': 'http://www.w3.org/1999/xhtml',
    'html': 'http://www.w3.org/1999/xhtml' 
}

doctypes = {
    'HTML5' : '<!DOCTYPE html>',
    # XHTML 1.1	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    # XHTML 1.1 Strict	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    # XHTML 1.1 Transitional	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    # XHTML 1.1 Frameset	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">
    # XHTML 1.0 Strict	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    # XHTML 1.0 Transitional	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    # XHTML_1_0_Frameset = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'
    'HTML4_01_Strict' : '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
    'HTML4_01_Transitional' : '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
    'HTML4_01_Frameset' : '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">',
    'HTML3_2' : '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">',
    'HTML2' : '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">'
}

# sizes = {
#     'small' : 'small',
#     'medium' : 'medium',
#     'large' : 'large',
#     'huge' : 'huge',
# }

# rfc_headers = {
#     'HTTP/1.1' : 'HTTP/1.1 200 OK',
# }

# parsers = {
#     'domonic' : 'regex',
#     'expathack' : 'expathack',
# }

# mimetypes = {
#     'application/xml' : 'xml',
#     'application/xhtml+xml' : 'xhtml',
#     'text/html' : 'html',
#     'text/css' : 'css',
#     'text/plain' : 'txt',
#     'text/javascript' : 'js',
#     'application/javascript' : 'js',
#     'application/x-javascript' : 'js',
# }

# languages = {
#     'en' : 'en-US',
#     'en-gb' : 'en-GB',
#     'en-au' : 'en-AU',
# }

# graphics_extensions = {
#     'svg' : 'svg',
#     'svgz' : 'svgz',
#     'png' : 'png',
#     'jpg' : 'jpg',
#     'jpeg' : 'jpeg',
#     'gif' : 'gif',
#     'pdf' : 'pdf',
#     'ps' : 'ps',
#     'eps' : 'eps',
#     'bmp' : 'bmp',
#     'tiff' : 'tiff',
#     'tif' : 'tif',
#     'tga' : 'tga',
#     'pcx' : 'pcx',
#     'pnm' : 'pnm',
#     'xpm' : 'xpm',
#     'xbm' : 'xbm',
#     'xwd' : 'xwd',
#     'xcf' : 'xcf',
#     'xpm' : 'xpm',
#     'xwd' : 'xwd',
#     'x3f' : 'x3f',
#     'xcf' : 'xcf',
#     'xv' : 'xv',
#     'x' : 'x',
# }

# favicons = {
#     'apple-touch-icon' : 'apple-touch-icon-{size}x{size}-precomposed.png',
#     'apple-touch-icon-precomposed' : 'apple-touch-icon-{size}x{size}-precomposed.png',
#     'apple-touch-icon-57x57' : 'apple-touch-icon-57x57.png',
#     'apple-touch-icon-72x72' : 'apple-touch-icon-72x72.png',
#     'apple-touch-icon-114x114' : 'apple-touch-icon-114x114.png',
#     'apple-touch-icon-144x144' : 'apple-touch-icon-144x144.png',
#     'apple-touch-icon-152x152' : 'apple-touch-icon-152x152.png',
#     'apple-touch-icon-180x180' : 'apple-touch-icon-180x180.png',
#     'apple-touch-icon-precomposed-57x57' : 'apple-touch-icon-57x57-precomposed.png',
#     'apple-touch-icon-precomposed-72x72' : 'apple-touch-icon-72x72-precomposed.png',
#     'apple-touch-icon-precomposed-114x114' : 'apple-touch-icon-114x114-precomposed.png',
#     'apple-touch-icon-precomposed-144x144' : 'apple-touch-icon-144x144-precomposed.png',
#     'apple-touch-icon-precomposed-152x152' : 'apple-touch-icon-152x152-precomposed.png',
#     'apple-touch-icon-precomposed-180x180' : 'apple-touch-icon-180x180-precomposed.png',
#     'apple-touch-icon-precomposed-196x196' : 'apple-touch-icon-196x196-precomposed.png',
#     'apple-touch-icon-precomposed-256x256' : 'apple-touch-icon-256x256-precomposed.png',
# }    

'''
a_tags = {
    'a' : '<a href="{href}" title="{title}">{text}</a>',
    'a:hover' : '<a href="{href}" title="{title}">{text}</a>',
    'a:visited' : '<a href="{href}" title="{title}">{text}</a>',
    'a:link' : '<a href="{href}" title="{title}">{text}</a>',
    'a:active' : '<a href="{href}" title="{title}">{text}</a>',
    'a:hover' : '<a href="{href}" title="{title}">{text}</a>',
    'a:focus' : '<a href="{href}" title="{title}">{text}</a>',
    # 'a:not' : '<a href="{href}" title="{title}">{text}</a>',
}
'''

'''
tag_states = {
    'a' : {
        'hover' : 'a:hover',
        'visited' : 'a:visited',
        'link' : 'a:link',
        'active' : 'a:active',
        'focus' : 'a:focus',
        # 'not' : 'a:not',
    }   
}
'''


# gravitational_constant = 6.67384e-11
# planck_constant = 6.62606957e-34
# speed_of_light = 299792458
# electron_charge = 1.602176565e-19
# electron_mass = 9.10938291e-31
# proton_mass = 1.672621777e-27
# neutron_mass = 1.674927351e-27
# atomic_mass_unit = 1.660539040e-24
# avogadro_constant = 6.02214129e23
# boltzmann_constant = 1.3806488e-23
# gas_constant = 8.3144621

# i love #copilot