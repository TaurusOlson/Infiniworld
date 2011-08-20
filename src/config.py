#!/usr/bin/python

"""Key bindings configuration"""

# For now this 'configuration manager' only deals with keys defined by the
# user.

import pygame


def read_config(fname):
    """Read the configuration file and return a dictionary.

    Parameters:
    `fname`: the name of the configuration file

    Returns:
    A dictionary whose keys are the name of the parameters used in the source
    code and values are the custom values defined by the user.

    """
    with open(fname, "r") as f:
        # A bit of pipelining...

        # Filter out comments
        lines = [l for l in f.read().split("\n") if not l.startswith("#")]

        # Lists of parameters and values
        params_vals = [p.split("=") for p in lines if len(p) > 1]

        # Clean up the parameters and the values
        game_params = [x[0].strip() for x in params_vals]
        custom_vals = [x[1].strip().lower() for x in params_vals]

    return dict(zip(game_params, custom_vals))



class KeysConfig(object):
    """This class manages all the keys defined by the user in the configuration
    file
    
    Usage:
    # Create the instance:
    >>> keys = KeysConfig('config.txt')
    # Read the configuration file, convert the keys and attach them to the
    # instance:
    >>> keys.run()

    The config_keys and pygame_keys attribute give respectively access to the
    keys defined by the user and the Pygame keys
    >>> print keys.config_keys
    >>> print keys.pygame_keys
    """

    def __init__(self, config_file):
        object.__init__(self)
        self.config_file = config_file


    def __str__(self):
        return "KeysConfig object converting config_keys to pygame_keys"


    def __repr__(self):
        return "%s" % repr(self)


    def convert_to_pygame_keys(self):
        """docstring for convert_to_pygame_keys"""
        config = read_config(self.config_file)

        # Keep only configuration keys
        self.keys_ = [kb for kb in config if kb.startswith('K_')]

        self.config_keys = {}
        for key_ in self.keys_:
            self.config_keys.__setitem__(key_, config[key_])

        self.pygame_keys = {"backspace":pygame.K_BACKSPACE,
                            "tab":pygame.K_TAB,
                            "return":pygame.K_RETURN,
                            "^[": pygame.K_ESCAPE, "esc":pygame.K_ESCAPE,
                            "escape":pygame.K_ESCAPE,
                            "colon": pygame.K_COLON,  ":":pygame.K_COLON,
                            "hash":pygame.K_HASH, "#":pygame.K_HASH,
                            "caret": pygame.K_CARET, "^":pygame.K_CARET,
                            "period":pygame.K_PERIOD, ".":pygame.K_PERIOD,
                            "space":pygame.K_SPACE,
                            "!":pygame.K_EXCLAIM,
                            "$":pygame.K_DOLLAR,
                            "&":pygame.K_AMPERSAND,
                            "'":pygame.K_QUOTE,
                            "(":pygame.K_LEFTPAREN,
                            ")":pygame.K_RIGHTPAREN,
                            "*":pygame.K_ASTERISK,
                            "+":pygame.K_PLUS,
                            ",":pygame.K_COMMA,
                            "-":pygame.K_MINUS,
                            "/":pygame.K_SLASH,
                            "\\":pygame.K_BACKSLASH,
                            ";":pygame.K_SEMICOLON, "semicolon":pygame.K_SEMICOLON,
                            "<":pygame.K_LESS,
                            "=":pygame.K_EQUALS,
                            ">":pygame.K_GREATER,
                            "?":pygame.K_QUESTION,
                            "@":pygame.K_AT,
                            "[":pygame.K_LEFTBRACKET,
                            "]":pygame.K_RIGHTBRACKET,
                            "_":pygame.K_UNDERSCORE,
                            "`":pygame.K_BACKQUOTE}

        # Let's be lazy
        alphanum = 'abcdefghijklmnopqrstuvwxyz0123456789'
        alphanum_pygame_values = map(lambda x: pygame.__getattribute__("K_%s" %x), alphanum)
        alphanum_pygame_keys   = dict(zip(alphanum, alphanum_pygame_values))
        self.pygame_keys.update(alphanum_pygame_keys)


    def attach_keys(self):
        """Attach the defined keys to the KeysConfig object.

        """
        for k_game, k_custom in self.config_keys.items():
            setattr(self, k_game, self.pygame_keys[k_custom])


    def run(self):
        """Run the convertion and attach the keys to the KeysConfig object"""
        self.convert_to_pygame_keys()
        self.attach_keys()
        return self



if __name__ == '__main__':
    keys = KeysConfig('config.txt').run()
    print "Keys used:" 
    for k,v in keys.config_keys.items():
        print "%24s: %s" % (k, v)
